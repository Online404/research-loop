# Contributing

Research Loop welcomes improvements to research decisions, source grounding, portability and recovery from interrupted work.

1. Describe the real workflow problem and the behavior that should change.
2. Include a small synthetic or openly licensed example, with provenance.
3. Keep the main skill concise; place conditional detail in a linked reference.
4. Keep user-specific hardware, credentials, data, manuscripts and unpublished results out of contributions.
5. Add a behavioral test for meaningful helper changes. Run `python -m unittest discover -s tests -v`.

Do not report a workflow as effective merely because its formatting checks pass. Distinguish structural tests, agent behavior evaluations, and observed scientific outcomes.

For upstream-inspired changes, record the exact project, revision and relevant paths in `docs/PROVENANCE.md`. Prefer explicit optional integrations and original instructions. If adding third-party material, include its license and attribution and identify modifications.

Pull requests should explain the problem, resulting behavior, validation and remaining practical limits. Never include live credentials in an issue or example.
