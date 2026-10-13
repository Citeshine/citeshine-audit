import json, tempfile, unittest
from pathlib import Path
from citeshine_audit import cli, providers
from citeshine_audit.analyze import analyze_answer

class T(unittest.TestCase):
    def test_analyze(self):
        a = analyze_answer("1. Profound\n2. 引耀 Citeshine\n", ["https://www.citeshine.com/x"],
                           {"name": "Citeshine", "aliases": ["引耀"]}, [{"name": "Profound"}], "citeshine.com")
        self.assertTrue(a["brand_mentioned"]); self.assertEqual(a["brand_order"], 2)
        self.assertEqual(a["brand_list_rank"], 2); self.assertTrue(a["brand_domain_cited"])
    def test_pipeline_fake(self):
        cfg = cli.load("configs/citeshine.json")
        with tempfile.TemporaryDirectory() as d:
            raw = cli.run(cfg, ["fake"], 2, Path(d))
            self.assertEqual(len(raw.read_text().splitlines()), 2 * len(cfg["prompts"]))
            md = cli.report(cfg, raw, Path(d)).read_text()
            self.assertIn("Brand mentioned", md); self.assertTrue((Path(d)/"report.html").exists())
unittest.main() if __name__ == "__main__" else None
