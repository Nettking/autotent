#!/usr/bin/env python3
"""Offline real-image pilot. Never contacts cameras, brokers, Drive, or actuators.

A uses a hash-verified archived function slice, not an application reimplementation.
B is a separately identified binary-union measurement variant. Reference labels are
AI-assisted and unreviewed; all reported scores are provisional point agreement.
"""
from __future__ import annotations
import argparse, ast, csv, hashlib, json, platform, sys, time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import cv2
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ARCHIVE_SHA = '35b9d8ad2c2835f356d277adaf972bf28d78b7f9'
# These are literal archived HSV bounds, NOT corrected RGB/HSV thresholds.
RWY = {'white':((220,220,220),(255,255,255)),
       'yellow':((255,160,0),(255,255,100)),
       'red':((255,0,0),(255,75,30))}
FIELD_MAP = {'light_green_pixel_count':'Light_green Total Pixel Count',
             'green_pixel_count':'Medium_green Total Pixel Count',
             'dark_green_pixel_count':'Dark_green Total Pixel Count'}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_archived() -> dict:
    """Execute only verified functions; skip interactive input, loops and plotting."""
    src = HERE/'archived/grid_count.py'
    raw = src.read_bytes()
    blob = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    if blob != ARCHIVE_SHA:
        raise ValueError('Archived function source differs from pinned Git blob')
    tree = ast.parse(raw.decode('utf-8'))
    names = {'crop_image','apply_morphological_operations','find_and_draw_contours',
             'count_leaves','get_color_code'}
    funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    ranges = next(ast.literal_eval(n.value) for n in tree.body
                  if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name)
                  and n.targets[0].id == 'hsv_ranges')
    env = {'cv2':cv2, 'np':np, 'Image':Image, 'hsv_ranges':ranges, 'area_threshold':100.0}
    exec(compile(ast.Module(body=funcs,type_ignores=[]),str(src),'exec'), env)
    return env


def confusion(ref: list[str], pred: list[bool]) -> dict:
    out = dict(TP=0, FP=0, FN=0, TN=0, U=0)
    for r,q in zip(ref,pred,strict=True):
        if r == 'U': out['U'] += 1
        elif r == 'F': out['TP' if q else 'FN'] += 1
        elif r == 'B': out['FP' if q else 'TN'] += 1
        else: raise ValueError(f'Unknown reference {r!r}')
    return out


def metrics(c: dict) -> dict:
    tp,fp,fn,tn = (c[k] for k in ('TP','FP','FN','TN'))
    safe = lambda a,b: a/b if b else None
    return {**c, 'precision':safe(tp,tp+fp), 'recall':safe(tp,tp+fn),
            'f1':safe(2*tp,2*tp+fp+fn), 'accuracy':safe(tp+tn,tp+fp+fn+tn),
            'balanced_accuracy': ((tp/(tp+fn)+tn/(tn+fp))/2 if (tp+fn)*(tn+fp) else None)}


def strict_observations(row: dict, image: str, capture_date: str, digest: str) -> list[dict]:
    """New strict CSV mapping. Context envelope is not an archived ThingML message."""
    obs=[]
    for feature, source in FIELD_MAP.items():
        if source not in row: raise ValueError(f'Missing measurement: {source}')
        value=float(row[source])
        if not np.isfinite(value) or value < 0: raise ValueError(f'Invalid measurement: {source}')
        obs.append({'image':image, 'capture_date':capture_date, 'sha256':digest,
                    'msg_type':feature, 'value':value, 'units':'sum_external_contour_area_px2',
                    'scope':'whole_cropped_frame', 'model_delivery':'not_executed'})
    return obs


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows: raise ValueError(f'No rows for {path}')
    with path.open('w',newline='') as f:
        writer=csv.DictWriter(f, fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)


def run(images: Path, output: Path) -> dict:
    output.mkdir(parents=True,exist_ok=True)
    manifest=list(csv.DictReader((HERE/'manifest.csv').read_text().splitlines()))
    refs=list(csv.DictReader((HERE/'reference_points.csv').read_text().splitlines()))
    freeze=json.loads((HERE/'reference_freeze.json').read_text())
    if sha256(HERE/'reference_points.csv') != freeze['sha256']:
        raise ValueError('Reference labels changed since recorded freeze')
    env=load_archived(); cv2.setNumThreads(1)
    byimage=defaultdict(list)
    for r in refs: byimage[r['image']].append(r)
    points_out=[];frames=[];obs_out=[];native_equal=0
    for m in sorted(manifest,key=lambda d:d['date']):
        src=images/m['image']
        if not src.is_file(): raise FileNotFoundError(src)
        if sha256(src) != m['sha256']: raise ValueError(f'Wrong image bytes: {src.name}')
        t0=time.perf_counter()
        # Independently execute the archived count_leaves function as preserved.
        env['area_threshold']=100.0
        native_counts,native_areas=env['count_leaves'](str(src))
        with Image.open(src) as decoded:
            rgb=np.array(decoded.convert('RGB'))
        bgr=cv2.cvtColor(env['crop_image'](rgb,100),cv2.COLOR_RGBA2BGR)
        hsv=cv2.cvtColor(bgr,cv2.COLOR_BGR2HSV)
        npx=hsv.shape[0]*hsv.shape[1]
        channels={}; raw_union=np.zeros(hsv.shape[:2],np.uint8)
        for name,(lo,hi) in env['hsv_ranges'].items():
            raw=cv2.inRange(hsv,np.array(lo),np.array(hi))
            raw_union |= raw
            opened=env['apply_morphological_operations'](raw)
            channels[name]=opened
        masks={}; areas_by_tau={};counts_by_tau={}
        for tau in (0,100,1000):
            union=np.zeros(hsv.shape[:2],np.uint8);areas=[];counts=[];summed_filled=0
            for name,opened in channels.items():
                _,contours,area=env['find_and_draw_contours'](bgr,opened,env['get_color_code'](name),tau,name)
                mask=np.zeros_like(union)
                cv2.drawContours(mask,contours,-1,255,cv2.FILLED)
                union |= mask;summed_filled+=int(np.count_nonzero(mask))
                areas.append(float(area));counts.append(len(contours))
            masks[f'A{tau}']=union
            areas_by_tau[tau]=areas;counts_by_tau[tau]=counts
            if tau==100:
                overlap_pixels=summed_filled-int(np.count_nonzero(union))
        # B: union ranges BEFORE morphology, preserve foreground pixels and holes;
        # no component-area filtering. This is a measurement variant, not a new trained model.
        masks['B']=env['apply_morphological_operations'](raw_union)
        if native_counts!=counts_by_tau[100] or not np.allclose(native_areas,areas_by_tau[100],rtol=0,atol=0):
            raise AssertionError(f'Archived function/harness disagreement in {src.name}')
        native_equal+=1
        rwy_pixels={name:int(np.count_nonzero(cv2.inRange(hsv,np.array(lo),np.array(hi)))) for name,(lo,hi) in RWY.items()}
        labels=byimage[m['image']]
        if len(labels)!=36: raise ValueError('Expected 36 frozen reference points')
        for r in labels:
            x,y=int(r['x']),int(r['y'])
            points_out.append({'image':m['image'],'group':m['group'],'point':r['point'],
                'reference':r['reference'],**{name:int(mask[y,x]>0) for name,mask in masks.items()},'all_background':0})
        exportrow={key:float(val) for key,val in zip(FIELD_MAP.values(),native_areas,strict=True)}
        mapped=strict_observations(exportrow,m['image'],datetime.strptime(m['date'],'%Y%m%d').date().isoformat(),m['sha256'])
        obs_out.extend(mapped)
        original_sender=[int(exportrow.get(key,0)) for key in FIELD_MAP]
        frames.append({'image':m['image'],'date':m['date'],'group':m['group'],
          'crop_width':hsv.shape[1],'height':hsv.shape[0],
          **{name+'_contour_area':float(area) for name,area in zip(channels,native_areas,strict=True)},
          **{name+'_contour_count':count for name,count in zip(channels,native_counts,strict=True)},
          'summed_channel_area':sum(native_areas),
          **{name+'_foreground_pixels':int(np.count_nonzero(mask)) for name,mask in masks.items()},
          'A100_overlap_pixels':overlap_pixels,
          'A100_foreground_fraction':float(np.count_nonzero(masks['A100'])/npx),
          'B_foreground_fraction':float(np.count_nonzero(masks['B'])/npx),
          **{name+'_archived_hsv_pixels':n for name,n in rwy_pixels.items()},
          'nonzero_export_fields':sum(v>0 for v in native_areas),
          'unmapped_sender_nonzero_fields':sum(v>0 for v in original_sender),
          'strict_adapter_equal_fields':sum(o['value']==v for o,v in zip(mapped,native_areas,strict=True)),
          'processing_seconds':time.perf_counter()-t0})
    results={}
    for group in ('all','spread','sequence'):
        subset=points_out if group=='all' else [r for r in points_out if r['group']==group]
        results[group]={}
        for method in ('A0','A100','A1000','B','all_background'):
            c=confusion([r['reference'] for r in subset],[bool(r[method]) for r in subset])
            out=metrics(c)
            # Conservative sensitivity: assign every uncertain point against or in favour
            # of each prediction. These are bounds, not alternative annotation decisions.
            ups=sum(r['reference']=='U' and r[method]==1 for r in subset)
            uns=sum(r['reference']=='U' and r[method]==0 for r in subset)
            out['uncertainty_f1_worst']=metrics({**c,'FP':c['FP']+ups,'FN':c['FN']+uns,'U':0})['f1']
            out['uncertainty_f1_best']=metrics({**c,'TP':c['TP']+ups,'TN':c['TN']+uns,'U':0})['f1']
            results[group][method]=out
    perframe=[]
    for f in frames:
        subset=[r for r in points_out if r['image']==f['image']]
        for method in ('A100','B'):
            perframe.append({'image':f['image'],'group':f['group'],'method':method,**metrics(confusion([r['reference'] for r in subset],[bool(r[method]) for r in subset]))})
    summary={'run_at_utc':datetime.now(timezone.utc).isoformat(),
       'status':'executed_image_component_pilot; AI references unreviewed; no native ThingML integration',
       'n_images':len(frames),'n_points':len(points_out),
       'reference_counts':dict(Counter(r['reference'] for r in points_out)),
       'reference_sha256':sha256(HERE/'reference_points.csv'),
       'scene_reference_sha256':sha256(HERE/'reference_scenes.csv'),
       'manifest_sha256':sha256(HERE/'manifest.csv'),
       'archived_function_git_blob':ARCHIVE_SHA,
       'archived_function_area_and_contour_count_exact_matches':native_equal,
       'rwy_zero_frames':sum(all(f[name+'_archived_hsv_pixels']==0 for name in RWY) for f in frames),
       'nonzero_export_fields':sum(f['nonzero_export_fields'] for f in frames),
       'unmapped_sender_nonzero_fields':sum(f['unmapped_sender_nonzero_fields'] for f in frames),
       'strict_adapter_equal_fields':sum(f['strict_adapter_equal_fields'] for f in frames),
       'environment':{'python':sys.version.split()[0],'opencv':cv2.__version__,'numpy':np.__version__,'pillow':Image.__version__,'platform':platform.platform()},
       'scores':results,
       'native_thingml':{'executed':False,'reason':'Native binary not available in this runtime: GitHub decoded-blob read rejected binary UTF-8, native binary materialization unsupported, direct container retrieval failed DNS. Base64 content can be viewed but no reliable file transfer was established. No substitute runtime or state-model port is presented as native execution.'}}
    scenes=list(csv.DictReader((HERE/'reference_scenes.csv').read_text().splitlines()))
    summary['scene_observations']={'visible_flower_witness_frames':sum(s['flowers']=='present' for s in scenes),'visible_red_fruit_witness_frames':sum(s['red_fruit']=='present' for s in scenes),'human_reviewed':False,'absence_not_scored':True}
    write_csv(output/'frames.csv',frames);write_csv(output/'points_scored.csv',points_out);write_csv(output/'per_frame_scores.csv',perframe)
    (output/'observations.jsonl').write_text(''.join(json.dumps(o,sort_keys=True)+'\n' for o in obs_out))
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    return summary

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--images',required=True,type=Path)
    parser.add_argument('--output',type=Path,default=HERE/'results')
    args=parser.parse_args()
    print(json.dumps(run(args.images,args.output),indent=2))
