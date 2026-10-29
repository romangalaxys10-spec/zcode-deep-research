# Changelog

## 0.1.0 - 2026-10-29

- Initial release: sub-question scoping, subagent fan-out for gathering,
  contradiction-preserving triangulation, and a verdict-first one-page brief.
- Inline `[n]` citations with a numbered source list, paywalled and
  unreachable sources kept visible, open-questions section, per-section
  confidence notes.
- `citation_check.py` gate: lists bare-claim sentences, orphan citation
  markers, and malformed source entries; exits 1 on any violation.
- Briefs save to `research/<date>-<slug>.md` and must pass the gate before
  the run is reported complete.
