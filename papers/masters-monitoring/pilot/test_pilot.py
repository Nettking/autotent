"""Artifact/regression checks; passing does not validate botanical classifications."""
import csv
import hashlib
import json
import unittest
from pathlib import Path
from run_pilot import HERE, FIELD_MAP, confusion, metrics, load_archived, strict_observations

class PilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.points = list(csv.DictReader((HERE/'results/points_scored.csv').read_text().splitlines()))
        cls.frames = list(csv.DictReader((HERE/'results/frames.csv').read_text().splitlines()))
        cls.summary = json.loads((HERE/'results/summary.json').read_text())

    def test_archived_source_identity(self):
        self.assertIn('count_leaves',load_archived())

    def test_reference_freezes(self):
        for filename,freeze in [('reference_points.csv','reference_freeze.json'),('reference_scenes.csv','scene_reference_freeze.json')]:
            self.assertEqual(hashlib.sha256((HERE/filename).read_bytes()).hexdigest(),json.loads((HERE/freeze).read_text())['sha256'])

    def test_sample_size_and_exclusions(self):
        self.assertEqual(len(self.frames),24)
        self.assertEqual(len(self.points),864)
        self.assertEqual(self.summary['reference_counts'],{'F':41,'B':806,'U':17})
        self.assertEqual(len({x['image'] for x in self.frames}),24)

    def test_metrics_recompute_for_all_methods_and_groups(self):
        for group in ('all','spread','sequence'):
            rows=self.points if group=='all' else [p for p in self.points if p['group']==group]
            for method in ('A0','A100','A1000','B','all_background'):
                actual=metrics(confusion([p['reference'] for p in rows],[bool(int(p[method])) for p in rows]))
                expected=self.summary['scores'][group][method]
                for key,value in actual.items():
                    self.assertEqual(value,expected[key],(group,method,key))

    def test_primary_counts(self):
        score=self.summary['scores']['all']['A100']
        self.assertEqual([score[k] for k in ('TP','FP','FN','TN','U')],[35,0,6,806,17])
        self.assertAlmostEqual(score['f1'],70/76)

    def test_strict_adapter_retains_float(self):
        row=dict(zip(FIELD_MAP.values(),[10.5,0,20.25]))
        obs=strict_observations(row,'test.jpg','2023-01-01','0'*64)
        self.assertEqual([x['value'] for x in obs],[10.5,0,20.25])
        self.assertTrue(all(x['model_delivery']=='not_executed' for x in obs))

    def test_strict_adapter_rejects_missing_and_invalid(self):
        base=dict(zip(FIELD_MAP.values(),[1,2,3]))
        with self.assertRaises(ValueError): strict_observations({},'x','x','x')
        for invalid in [float('nan'),float('inf'),-1]:
            row={**base,next(iter(FIELD_MAP.values())):invalid}
            with self.assertRaises(ValueError): strict_observations(row,'x','x','x')

    def test_real_hand_off_and_zero_flower_channels(self):
        self.assertEqual(sum(int(x['strict_adapter_equal_fields']) for x in self.frames),72)
        self.assertEqual(sum(int(x['nonzero_export_fields']) for x in self.frames),71)
        self.assertEqual(sum(int(x['unmapped_sender_nonzero_fields']) for x in self.frames),0)
        self.assertTrue(all(int(x[c+'_archived_hsv_pixels'])==0 for x in self.frames for c in ('red','yellow','white')))

    def test_uncertainty_and_native_status_not_promoted(self):
        self.assertFalse(self.summary['native_thingml']['executed'])
        self.assertFalse(self.summary['scene_observations']['human_reviewed'])
        refs=list(csv.DictReader((HERE/'reference_points.csv').read_text().splitlines()))
        self.assertTrue(all(x['human_reviewed']=='false' for x in refs))
        self.assertEqual(self.summary['scene_observations']['visible_flower_witness_frames'],11)

if __name__=='__main__':
    unittest.main()
