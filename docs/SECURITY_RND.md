# Governed Security Research and Development

The R&D layer tests improvements in isolation before fleet rollout. Its backlog includes
repository posture scoring, fuzzing, property testing, mutation testing, SBOMs, artifact
attestations, SLSA gap analysis, VEX/reachability, recovery drills, canaries, detector
benchmarking, and playbook retirement.

Every experiment requires a hypothesis, baseline, metric, time and cost limits, stop condition,
rollback, data classification, and owner approval. Production chaos, live malware, private-data
uploads, unbounded fuzzing, automatic release, and unreviewed security claims are prohibited.

Coverage reports measure whether catalog items were adopted. They do not prove effectiveness.
Effectiveness requires defect discovery, false-positive, recurrence, recovery-time, regression,
cost, and operational outcome evidence.
