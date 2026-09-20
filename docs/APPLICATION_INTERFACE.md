# Application Interface

Install the review branch in an isolated Python environment:

```bash
python -m pip install -e .
jarvis-fleet validate
jarvis-fleet readiness
```

Available application commands:

- `jarvis-fleet triage findings.json`
- `jarvis-fleet plan-patch issue.json`
- `jarvis-fleet prove-resolution record.json --output artifacts/resolution`
- `jarvis-fleet coverage evidence.json`

These commands analyze evidence and generate plans or documentation. They do not modify target
repositories. Repository write adapters must remain separate, scoped, approval-gated, and
tested against one pilot repository before fleet rollout.

The AI patcher council separates reproduction, diagnosis, authorship, adversarial review,
regression verification, security review, recovery verification, and owner approval. No AI
role may approve its own work or impersonate the owner.
