#!/usr/bin/env python3
"""Explainable ATS-style resume/JD keyword coverage heuristic. No network access."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

WEIGHTS = {
    "required_skills": 0.50,
    "preferred_skills": 0.20,
    "responsibilities": 0.20,
    "role_terms": 0.10,
}

TECH_TERMS = [
    "python", "java", "javascript", "typescript", "sql", "nosql", "mongodb",
    "postgresql", "mysql", "aws", "azure", "gcp", "docker", "kubernetes",
    "terraform", "ci/cd", "git", "linux", "rest api", "graphql",
    "machine learning", "deep learning", "generative ai", "genai",
    "large language models", "llm", "rag", "retrieval augmented generation",
    "vector database", "embeddings", "langchain", "langgraph", "llamaindex",
    "agentic ai", "ai agents", "prompt engineering", "fine-tuning",
    "model evaluation", "mlops", "pytorch", "tensorflow", "scikit-learn",
    "pandas", "numpy", "fastapi", "flask", "microservices", "system design",
    "data engineering", "feature engineering", "data pipelines",
    "communication", "stakeholder management", "leadership", "agile",
    "problem solving", "security", "monitoring", "observability",
]

REQUIRED_HEADERS = re.compile(
    r"\b(required|must[- ]have|minimum qualifications|basic qualifications|"
    r"you have|what you bring|requirements)\b", re.I
)
PREFERRED_HEADERS = re.compile(
    r"\b(preferred|good to have|nice to have|bonus|desired|additional qualifications)\b", re.I
)
RESP_HEADERS = re.compile(
    r"\b(responsibilities|what you will do|what you'll do|key duties|"
    r"your role|accountabilities)\b", re.I
)

def read_document(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md", ".rst"}:
        return path.read_text(encoding="utf-8", errors="replace")
    if suffix == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise RuntimeError("PDF support requires: pip install pypdf") from exc
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if suffix == ".docx":
        try:
            from docx import Document
        except ImportError as exc:
            raise RuntimeError("DOCX support requires: pip install python-docx") from exc
        doc = Document(str(path))
        chunks = [p.text for p in doc.paragraphs]
        for table in doc.tables:
            for row in table.rows:
                chunks.append(" ".join(cell.text for cell in row.cells))
        return "\n".join(chunks)
    raise RuntimeError(f"Unsupported file type: {suffix}. Use PDF, DOCX, TXT, or MD.")

def normalize(text: str) -> str:
    text = text.lower().replace("&", " and ")
    text = re.sub(r"[\u2010-\u2015]", "-", text)
    text = re.sub(r"[^a-z0-9+#./ -]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def extract_terms(text: str) -> List[str]:
    norm = normalize(text)
    found = []
    for term in TECH_TERMS:
        pattern = r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])"
        if re.search(pattern, norm):
            found.append(term)
    # Include meaningful capitalized/technical phrases only when explicit in text.
    for line in text.splitlines():
        line = line.strip(" \t-*•")
        if len(line) < 3 or len(line) > 180:
            continue
        if re.search(r"\b(must|required|preferred|experience|proficient|knowledge|"
                     r"responsible|build|develop|design|manage|lead|implement)\b", line, re.I):
            candidate = normalize(line)
            if 2 <= len(candidate.split()) <= 12 and candidate not in found:
                found.append(candidate)
    return list(dict.fromkeys(found))

def section_lines(jd: str) -> Dict[str, List[str]]:
    sections = {k: [] for k in WEIGHTS}
    current = "role_terms"
    for raw in jd.splitlines():
        line = raw.strip()
        if not line:
            continue
        if PREFERRED_HEADERS.search(line):
            current = "preferred_skills"
            continue
        if REQUIRED_HEADERS.search(line):
            current = "required_skills"
            continue
        if RESP_HEADERS.search(line):
            current = "responsibilities"
            continue
        if re.match(r"^(#{1,4}\s*)?(about us|about the role|the opportunity|job summary)\b", line, re.I):
            current = "role_terms"
            continue
        if line.startswith(("-", "*", "•", "·")) or re.match(r"^\d+[.)]\s", line):
            sections[current].append(line)
    return sections

def score(resume: str, jd: str) -> dict:
    sections = section_lines(jd)
    resume_norm = normalize(resume)
    results = {}
    weighted_total = 0.0

    for key, weight in WEIGHTS.items():
        source = "\n".join(sections[key])
        if not source.strip():
            # Fall back to the full JD's detected terms if section headings are absent.
            if key == "required_skills":
                terms = extract_terms(jd)
            else:
                terms = []
        else:
            terms = extract_terms(source)

        matched, missing = [], []
        for term in terms:
            term_norm = normalize(term)
            pattern = r"(?<![a-z0-9])" + re.escape(term_norm) + r"(?![a-z0-9])"
            (matched if re.search(pattern, resume_norm) else missing).append(term)

        coverage = (len(matched) / len(terms) * 100) if terms else None
        points = (coverage * weight) if coverage is not None else None
        if points is not None:
            weighted_total += points
        results[key] = {
            "weight": weight,
            "term_count": len(terms),
            "matched_count": len(matched),
            "coverage_percent": round(coverage, 1) if coverage is not None else None,
            "weighted_points": round(points, 2) if points is not None else None,
            "matched_terms": matched,
            "missing_terms": missing,
        }

    available_weight = sum(v["weight"] for v in results.values() if v["coverage_percent"] is not None)
    total = round(weighted_total / available_weight) if available_weight else None
    return {
        "score": total,
        "score_type": "heuristic_keyword_coverage",
        "disclaimer": (
            "Not a proprietary ATS score, hiring probability, or guarantee. "
            "Keyword presence does not prove proficiency; manually verify evidence."
        ),
        "dimensions": results,
        "resume_word_count": len(resume.split()),
        "jd_word_count": len(jd.split()),
    }

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resume", required=True, type=Path)
    parser.add_argument("--jd", required=True, type=Path)
    parser.add_argument("--out", type=Path, help="Optional JSON output path")
    args = parser.parse_args()

    try:
        resume = read_document(args.resume)
        jd = read_document(args.jd)
        result = score(resume, jd)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    rendered = json.dumps(result, indent=2, ensure_ascii=False)
    if args.out:
        args.out.write_text(rendered + "\n", encoding="utf-8")
        print(f"Report written to: {args.out}")
    print(f"ATS-style keyword coverage: {result['score']}/100" if result["score"] is not None
          else "ATS-style keyword coverage: insufficient JD structure to score")
    print("Disclaimer:", result["disclaimer"])
    print(rendered)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
