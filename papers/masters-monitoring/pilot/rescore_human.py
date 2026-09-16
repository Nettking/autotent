#!/usr/bin/env python3
"""Rescore frozen pilot predictions against a separate human label set.

No image processing, threshold tuning, networking, or AI label substitution occurs.
CSV input must match every original image/point/coordinate. The compact JSON input
stores answers in original point order and is bound to the frozen reference hash.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import zipfile
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
METHODS = ('A0', 'A100', 'A1000', 'B', 'all_background')
KEY = lambda r: (r['image'], int(r['point']))
SHA = lambda b: hashlib.sha256(b).hexdigest()


def csv_rows(raw: bytes) -> list[dict]:
    return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))


def unique(rows: list[dict]) -> dict:
    out = {KEY(r): r for r in rows}
    if len(out) != len(rows):
        raise ValueError('Duplicate image/point identity')
    return out


def validate(human: list[dict], refs: list[dict]) -> list[dict]:
    h, ref = unique(human), unique(refs)
    if h.keys() != ref.keys():
        raise ValueError('Human labels do not cover exactly the original sample identities')
    for k, r in h.items():
        if (int(r['x']), int(r['y'])) != (int(ref[k]['x']), int(ref[k]['y'])):
            raise ValueError(f'Coordinate mismatch at {k}')
        if r['reference'] not in ('', 'F', 'B', 'U'):
            raise ValueError(f'Invalid reference category at {k}')
        if r['human_reviewed'] not in ('true', 'false'):
            raise ValueError(f'Invalid review flag at {k}')
        if (r['human_reviewed'] == 'true') != bool(r['reference']):
            raise ValueError(f'Label/review flag mismatch at {k}')
    return [h[KEY(r)] for r in refs]


def metrics(rows: list[dict], method: str) -> dict:
    c = dict.fromkeys(('TP', 'FP', 'FN', 'TN', 'uncertain', 'unreviewed'), 0)
    for r in rows:
        if r['human_reviewed'] == 'false':
            c['unreviewed'] += 1
        elif r['reference'] == 'U':
            c['uncertain'] += 1
        elif r['reference'] == 'F':
            c['TP' if r[method] else 'FN'] += 1
        elif r['reference'] == 'B':
            c['FP' if r[method] else 'TN'] += 1
    tp, fp, fn, tn = (c[k] for k in ('TP', 'FP', 'FN', 'TN'))
    ratio = lambda a, b: a / b if b else None
    return c | {'assessed': tp+fp+fn+tn, 'foliage': tp+fn, 'background': tn+fp,
                'precision': ratio(tp, tp+fp), 'recall': ratio(tp, tp+fn),
                'f1': ratio(2*tp, 2*tp+fp+fn), 'accuracy': ratio(tp+tn, tp+fp+fn+tn)}


def read_human(path: Path, refs: list[dict], ref_hash: str) -> list[dict]:
    if path.suffix.lower() == '.csv':
        return validate(csv_rows(path.read_bytes()), refs)
    bundle = json.loads(path.read_text())
    if bundle['schema'] != 'autotent.human-point-reference.v1':
        raise ValueError('Unsupported human-reference schema')
    if bundle['reference_points_sha256'] != ref_hash:
        raise ValueError('Wrong original point set')
    imap = {r['image']: r['answers'] for r in bundle['images']}
    if len(imap) != len(bundle['images']) or set(imap) != {r['image'] for r in refs}:
        raise ValueError('Wrong or duplicate image identities')
    if any(len(s) != 36 or any(c not in '.FBU' for c in s) for s in imap.values()):
        raise ValueError('Wrong point-answer encoding')
    human=[]
    for r in refs:
        a=imap[r['image']][int(r['point'])-1]
        human.append({**r, 'reference': '' if a=='.' else a,
                      'annotator':bundle['reviewer_id'], 'human_reviewed':'false' if a=='.' else 'true'})
    return validate(human, refs)


def score(labels: Path, records: Path = HERE/'records.zip') -> tuple[dict, list[dict]]:
    with zipfile.ZipFile(records) as z:
        ref_bytes=z.read('reference_points.csv')
        pred_bytes=z.read('results/points_scored.csv')
        refs=csv_rows(ref_bytes); pred=unique(csv_rows(pred_bytes))
    refmap=unique(refs)
    if pred.keys()!=refmap.keys():
        raise ValueError('Prediction/sample identities differ')
    human=read_human(labels,refs,SHA(ref_bytes))
    merged=[]
    for h in human:
        k=KEY(h); p=pred[k]
        if any(p[m] not in ('0','1') for m in METHODS):
            raise ValueError(f'Invalid prediction at {k}')
        merged.append({k:h[k] for k in ('image','point','x','y','reference','human_reviewed')} |
                      {'ai_reference':refmap[k]['reference'], 'group':p['group']} |
                      {m:int(p[m]) for m in METHODS})
    groups={'all':merged, 'spread':[r for r in merged if r['group']=='spread'],
            'sequence':[r for r in merged if r['group']=='sequence']}
    # This is only a post-hoc restriction of previously sampled points.
    # No new crop is processed, and there is no new grid or new experiment.
    groups['posthoc_roi_existing_points']=[r for r in merged if 1640<=int(r['x'])<3280 and 246<=int(r['y'])<2218]
    transitions=Counter((r['ai_reference'], r['reference']) for r in merged if r['human_reviewed']=='true')
    perframe=[]
    for name in dict.fromkeys(r['image'] for r in merged):
        rr=[r for r in merged if r['image']==name]
        perframe.append({'image':name, 'group':rr[0]['group'], **metrics(rr,'A100')})
    summary={'schema':'autotent.human-rescore.v1', 'labels_sha256':SHA(labels.read_bytes()),
             'reference_points_sha256':SHA(ref_bytes), 'frozen_predictions_sha256':SHA(pred_bytes),
             'rows':len(merged), 'images':len(perframe),
             'reviewed':sum(r['human_reviewed']=='true' for r in merged),
             'label_counts':dict(Counter(r['reference'] or 'blank' for r in merged)),
             'scores':{g:{m:metrics(rs,m) for m in METHODS} for g,rs in groups.items()},
             'missing_points':[{k:r[k] for k in ('image','point','x','y')} for r in merged if r['human_reviewed']=='false'],
             'ai_to_human_label_counts':{f'{a}->{b}':n for (a,b),n in sorted(transitions.items())},
             'per_frame':perframe,
             'scope':'One system-developer annotator; frozen predictions; no changed labels or tuned thresholds; point-level evaluation only.',
             'roi_scope':'Post-hoc subset of old points only; not a cropped-image rerun or independent validation.'}
    return summary, merged


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--labels',type=Path,required=True)
    p.add_argument('--records',type=Path,default=HERE/'records.zip')
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args(); summary,rows=score(args.labels,args.records)
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    for name,rs in [('points_scored.csv',rows),('per_frame_scores.csv',summary['per_frame'])]:
        with (args.output/name).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=rs[0].keys());w.writeheader();w.writerows(rs)
    print(json.dumps({k:summary[k] for k in ('rows','images','reviewed','label_counts')} | {'A100':summary['scores']['all']['A100']},indent=2))

if __name__=='__main__':
    main()
