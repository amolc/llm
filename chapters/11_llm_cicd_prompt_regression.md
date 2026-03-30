# Chapter 11: LLM CI/CD & Prompt Regression Testing

---

## Objectives
- Make LLM systems reproducible and safe to change.
- Track prompts, models, and datasets as versioned artifacts.
- Detect regressions in behavior with automated tests.

---

## CI/CD Pipeline Stages
1. Lint and static checks for code and prompt syntax.
2. Unit tests for prompt functions and tool bindings.
3. Golden‑set evaluation with scoring.
4. Threshold gates for accuracy, cost, latency, and safety.
5. Artifact tracking and deployment to staging/production.

---

## Prompt Registry
- Store prompts as files with IDs and metadata.
- Use templating engines with explicit variables.
- Record model version, temperature, and decoding params.

Example prompt file:
```text
id: summarize_earnings_v1
model: gemini-1.5-flash
temperature: 0.2
template: |
  Summarize the following earnings text in 5 bullets:
  {text}
```

---

## Golden Tests
- Curate a small but representative set of inputs with expected qualities.
- Score with rule‑based checks and LLM‑as‑a‑judge.

Minimal Python runner:
```python
import json, time
from typing import List, Dict

def call_model(prompt): ...

def judge(q, a):
    return int(q["expected"].lower() in a.lower())

def run(golden_path):
    g = [json.loads(l) for l in open(golden_path)]
    t0 = time.time()
    ok = 0
    for q in g:
        a = call_model(q["input"])
        ok += judge(q, a)
    acc = ok / len(g)
    lat = (time.time() - t0) / len(g)
    return {"accuracy": acc, "latency": lat}
```

---

## Gates and Budgets
- Accuracy ≥ target on golden set.
- Groundedness and safety ≥ thresholds.
- Token cost and latency within budgets.

---

## GitHub Actions Skeleton
```yaml
name: llm-ci
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python scripts/run_golden.py --golden data/golden.jsonl --out ci_report.json
      - run: python scripts/check_thresholds.py --report ci_report.json --min-acc 0.85 --max-ttft 1.0
```

---

## Rollout Strategy
- Shadow deploy and compare to baseline.
- Canary percentage with automatic rollback on regression.
- Maintain changelog linking prompt, model, and dataset versions.

---

## Best Practices
- Seed every run and log decoding parameters.
- Separate evaluation data from training and prompt crafting.
- Automate periodic re‑evaluation as upstream models update.
