# Transparent Resolution Evidence

A defect is not erased from history. It moves from open to a verified candidate only when its
original reproducer failed before the repair, passed after the repair, the configured test
suite passed, rollback and monitoring are documented, commits are distinct, and the owner
approved the result.

The evidence generator produces JSON for machines and Markdown for people. It calculates a
SHA-256 digest over the canonical input record so later changes are detectable. Evidence
includes failed checks and residual risk rather than presenting only successes.

## Required proof

- Repository and finding identity
- Before and after commit
- Reproducer before and after
- All relevant tests
- Rollback procedure
- Monitoring plan and recurrence window
- Owner approval
- Residual risks and exclusions

A verified candidate means the documented defect passed its defined gates. It never means that
every unknown error, vulnerability, environmental failure, or future regression was eliminated.
