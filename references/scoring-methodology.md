# Scoring methodology

## Purpose

This is a transparent keyword and evidence coverage heuristic to help candidates identify resume/JD alignment. It is not a replica of a commercial ATS and is not a hiring probability.

## Weighted dimensions

| Dimension | Weight |
|---|---:|
| Must-have / required skills | 50% |
| Preferred / good-to-have skills | 20% |
| Responsibilities and domain evidence | 20% |
| Role-specific terminology | 10% |

Each dimension is calculated as matched unique terms divided by extracted unique terms in that dimension, multiplied by its weight. The total is rounded to the nearest integer.

## Extraction

The script:
- extracts explicit bullet-like requirement lines and skill phrases from the JD;
- identifies common technical terms and multiword phrases;
- normalizes case and punctuation;
- checks whole-word / phrase presence in the resume;
- avoids counting repeated mentions more than once.

## Limitations

- Natural-language parsing is imperfect.
- A term appearing in a resume does not prove proficiency.
- Equivalent terms and context may require human review.
- The script may miss requirements expressed indirectly.
- A keyword match is not proof of real-world experience.
- A score of 80 is not equivalent to an 80% chance of interview or hire.
- Different ATS vendors and employers use different parsing, knockout, ranking, and workflow rules.

Use the skill's evidence matrix to validate every important match.
