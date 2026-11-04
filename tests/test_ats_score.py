import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "ats_score.py"
spec = importlib.util.spec_from_file_location("ats_score", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class ScoringTests(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(module.normalize("Python & RAG!"), "python and rag")

    def test_score_reports_matches_and_missing(self):
        jd = """
        Required qualifications
        - Python
        - LangChain
        Preferred qualifications
        - Kubernetes
        Responsibilities
        - Build machine learning systems
        """
        resume = "Built Python applications and used LangChain."
        result = module.score(resume, jd)
        self.assertIsNotNone(result["score"])
        self.assertIn("python", result["dimensions"]["required_skills"]["matched_terms"])
        self.assertIn("kubernetes", result["dimensions"]["preferred_skills"]["missing_terms"])
        self.assertIn("disclaimer", result)

    def test_empty_jd_does_not_make_up_score(self):
        result = module.score("Python developer", "")
        self.assertIsNone(result["score"])

if __name__ == "__main__":
    unittest.main()
