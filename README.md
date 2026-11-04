# 🚀 Interview Reviewer — AI Hiring Manager Skill

A reusable, cross-platform Agent Skill that reviews a resume against a job description and produces an evidence-based hiring report.

> **One skill. Multiple AI platforms. Transparent evaluation.**

## What it does

- Explainable ATS-style keyword coverage score (0–100)
- Required vs. preferred qualification analysis
- Resume/JD alignment and evidence mapping
- Missing skills and experience gaps
- Resume bullet rewrites that never invent metrics or achievements
- Five role-specific interview questions
- Three-day focused upskilling plan
- Hiring-manager-style summary with strengths, risks, and next steps

## Important scoring disclaimer

The score is a transparent heuristic calculated from extracted resume/JD text. It is **not** a proprietary ATS score, a guarantee of passing an ATS, a probability of getting hired, or a substitute for human judgment. Different employers configure screening systems differently.

The tool does not infer or score protected characteristics. It must not use age, gender, race, religion, disability, nationality, marital status, photographs, or other protected/personal characteristics in candidate evaluation.

## Repository layout

```text
interview-reviewer/
├── SKILL.md
├── README.md
├── LICENSE
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── .claude/skills/interview-reviewer/SKILL.md
├── .agents/skills/interview-reviewer/SKILL.md
├── .github/skills/interview-reviewer/SKILL.md
├── agents/openai.yaml
├── scripts/
│   └── ats_score.py
├── references/
│   └── scoring-methodology.md
├── templates/
│   └── hiring-report-template.md
└── tests/
    └── test_ats_score.py
```

## Quick start

### 1. Give the skill your inputs

Provide:
- Your resume (`.pdf`, `.docx`, `.txt`, or `.md`)
- The target job description (`.pdf`, `.docx`, `.txt`, or `.md`)

You can also paste both documents into the chat.

### 2. Ask for a review

```text
Use the Interview Reviewer skill.
Review my resume against the attached job description.
Generate the complete hiring report and a prioritized improvement plan.
```

### 3. Optional deterministic ATS-style analysis

Python 3.9+ is required. For PDF/DOCX support install optional parsers:

```bash
python -m pip install pypdf python-docx
```

Run:

```bash
python scripts/ats_score.py --resume resume.pdf --jd job_description.docx --out hiring-report.json
```

The script also prints a concise summary. It can read `.txt` and `.md` without optional packages.

## Install by platform

### Claude Code — plugin marketplace

From Claude Code, run:

```text
/plugin marketplace add YOUR_GITHUB_OWNER/claude-interview-reviewer
/plugin install interview-reviewer@interview-reviewer
```

Replace `YOUR_GITHUB_OWNER` with the GitHub account or organization that hosts this repository. Restart/reload Claude Code if the skill does not appear.

Alternatively, copy `.claude/skills/interview-reviewer/` into your project's `.claude/skills/` directory.

### Claude.ai

1. Download the repository ZIP from GitHub (`Code` → `Download ZIP`).
2. Create a ZIP containing the `interview-reviewer/` skill folder with `SKILL.md` at its root.
3. In Claude, open Settings → Capabilities/Skills (the exact label can vary).
4. Upload/enable the custom skill, if your plan and workspace support it.

The root `SKILL.md` is provided for this upload path.

### ChatGPT Skills

If Skills are enabled for your ChatGPT workspace:

1. Download the repository ZIP.
2. Upload the skill ZIP from the Skills area using **Create → Upload from your computer**.
3. Enable the skill and invoke it with `@Interview Reviewer` or ask ChatGPT to use it.

Alternatively, use `@skill-creator` and provide the GitHub repository URL as source material, then review and install the generated skill.

**Availability note:** ChatGPT Skills are currently limited to eligible workspace plans and depend on workspace settings. A GitHub URL by itself is not a universal one-click installer in every ChatGPT account. The skill instructions can still be pasted or uploaded where custom skills are unavailable.

### OpenAI Codex

Install from the skill directory URL (after publishing the repository):

```text
$skill-installer install https://github.com/YOUR_GITHUB_OWNER/claude-interview-reviewer/tree/main/.agents/skills/interview-reviewer
```

Restart Codex if required.

### GitHub Copilot

For repository-scoped use, keep the skill under `.github/skills/interview-reviewer/`. Copilot's supported skill locations and availability depend on the Copilot surface and repository context.

## Example output

The skill generates a report with:

1. Executive summary
2. ATS-style keyword coverage and score explanation
3. Must-have qualification matrix
4. Preferred qualification matrix
5. Evidence-backed strengths
6. Missing or weak evidence
7. Resume bullet rewrites
8. Five tailored interview questions
9. Three-day learning plan
10. Final recommendations and caveats

## Privacy and security

- Prefer running the local scoring script on your own machine.
- Do not upload confidential, regulated, or third-party personal data unless you are authorized and understand the platform's data handling terms.
- The script does not send resume or job-description content over the network.
- Review skill instructions and scripts before installing third-party repositories.
- Remove personal contact details from sample resumes before committing them to GitHub.

## Development

Run tests:

```bash
python -m unittest discover -s tests -v
```

## License

MIT. See [LICENSE](LICENSE).
