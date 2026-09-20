# Fleet Repair Protocol

## 1. Inventory and classify

Record repository, visibility, default branch, languages, build files, test commands,
deployment targets, data sensitivity, owners, and current check status. Unknown repositories
remain read-only.

## 2. Reproduce before repairing

Capture the failing command, environment, dependency versions, exit code, minimal reproduction,
logs, and evidence hash. An AI explanation without a reproducible symptom is a hypothesis.

## 3. Diagnose independently

Separate observed symptoms from suspected causes. Check recent changes, dependencies,
configuration drift, permissions, flaky tests, and external-service failures. Preserve
competing hypotheses when evidence does not distinguish them.

## 4. Produce the smallest reversible patch

Use a dedicated branch. Change only files required by the evidence. Do not mix upgrades,
refactors, formatting, and bug repair unless separately justified.

## 5. Validate

Run the reproducer, affected tests, full configured suite, static checks, security checks, and
a regression test that would have caught the defect. Compare performance and artifacts with
the baseline.

## 6. Review and rollback

Open a draft pull request containing evidence, root-cause confidence, changed files, tests,
residual risks, rollback instructions, and owner approval state. Never merge automatically.

## 7. Monitor and learn

After an approved merge, monitor the defined success metric and rollback trigger. Record both
successful and failed repairs in the outcome ledger. Promote recurring verified repairs into
versioned playbooks; retire playbooks that regress outcomes.

## Non-claim

The fleet can continuously reduce known defects and recovery time. It cannot guarantee that
all repositories are permanently error-free.
