"""Regression checks on label ingestion and scoring, not biological validation."""
import copy
import json
import unittest
import zipfile
from rescore_human import HERE, csv_rows, score, validate

class HumanRescoreTests(unittest.TestCase):
    def setUp(self):
        self.summary,self.rows=score(HERE/'human_review/labels.json')
        with zipfile.ZipFile(HERE/'records.zip') as z:
            self.refs=csv_rows(z.read('reference_points.csv'))
    def test_received_counts(self):
        self.assertEqual((self.summary['rows'],self.summary['reviewed']),(864,859))
        self.assertEqual(self.summary['label_counts'],{'blank':5,'F':64,'B':795})
    def test_primary_metrics(self):
        m=self.summary['scores']['all']['A100']
        self.assertEqual([m[k] for k in ('TP','FP','FN','TN')],[36,1,28,794])
        self.assertAlmostEqual(m['precision'],36/37)
        self.assertAlmostEqual(m['recall'],36/64)
        self.assertAlmostEqual(m['f1'],72/101)
    def test_posthoc_subset_is_explicit(self):
        m=self.summary['scores']['posthoc_roi_existing_points']['A100']
        self.assertEqual([m[k] for k in ('TP','FP','FN','TN')],[34,1,27,226])
        self.assertEqual(m['assessed'],288)
        self.assertIn('not a cropped-image rerun',self.summary['roi_scope'])
    def test_blanks_preserved(self):
        missing=self.summary['missing_points']
        self.assertEqual([int(r['point']) for r in missing],[1,2,3,4,5])
        self.assertTrue(all(r['image']=='top_20230705.png.jpg' for r in missing))
    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):validate(self.rows+[self.rows[0]],self.refs)
    def test_wrong_coordinates_rejected(self):
        rows=copy.deepcopy(self.rows);rows[0]['x']=999
        with self.assertRaises(ValueError):validate(rows,self.refs)
    def test_review_flags_validated(self):
        rows=copy.deepcopy(self.rows);rows[0]['human_reviewed']='true'
        with self.assertRaises(ValueError):validate(rows,self.refs)
    def test_committed_summary_reproduced(self):
        expected=json.loads((HERE/'human_review/results/summary.json').read_text())
        self.assertEqual(self.summary,expected)

if __name__=='__main__':unittest.main()
