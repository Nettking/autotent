"""Regression checks for the paper's four constructed examples, not plant labels."""
import re
import unittest
from pathlib import Path
from check_archived_operations import run_checks


class PaperChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = run_checks()

    def test_green_overlap(self):
        self.assertTrue(self.report["checks"]["green_range_overlap"]["confirmed"])

    def test_rwy_domain(self):
        self.assertTrue(self.report["checks"]["unreachable_rwy_hue"]["confirmed"])

    def test_csv_keys(self):
        self.assertTrue(self.report["checks"]["csv_header_default_zero"]["confirmed"])

    def test_temporal_plot(self):
        self.assertTrue(self.report["checks"]["per_channel_zero_removal"]["confirmed"])

    def test_citations_resolve(self):
        root = Path(__file__).resolve().parents[1]
        tex = (root / "main.tex").read_text(encoding="utf-8")
        bib = (root / "references.bib").read_text(encoding="utf-8")
        keys = set(re.findall(r"@\w+\s*\{\s*([^,]+),", bib))
        used = set()
        for group in re.findall(r"\\cite(?:\[[^\]]*\])*\{([^}]+)\}", tex):
            used.update(key.strip() for key in group.split(","))
        self.assertTrue(used)
        self.assertEqual(used - keys, set())


if __name__ == "__main__":
    unittest.main()
