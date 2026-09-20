# Anti-Bug Patch Construction

A patch is built from preserved defect evidence. It must not begin with an AI guess and end
with a weakened test.

The patch planner creates a deterministic repair identifier, isolated branch name, suspected
file boundary, required gates, prohibited actions, and rollback expectation. It does not edit
the target repository.

## Patch quality rules

- Reproduce before changing code.
- Add a regression test that fails for the original defect.
- Prefer the smallest justified change.
- Keep refactoring and dependency upgrades separate unless required by root cause.
- Run the original reproducer and the complete configured suite.
- Never weaken or delete a test merely to produce green CI.
- Generate resolution evidence.
- Open a draft pull request.
- Require owner approval before merge or deployment.

A repair becomes reusable only after monitoring shows reduced recurrence without new
regressions. Until then it remains one tested patch for one documented defect.
