# Deep Research

A multi-source research run that ends in a cited, gate-checked one-page brief.

## Why

You ask one question and chase seven tabs, and the answer you save to
memory is a hodgepodge with no dates and no way to see where source A and
source B disagreed. Deep Research splits the question into sub-questions,
fans them out to subagents, and forces every claim in the brief to carry an
inline citation. The gate script refuses to let the brief through while a
sentence has no source or a citation points at nothing.

## How it works

| Step | What happens |
| --- | --- |
| SCOPE | Question becomes 3 to 6 sub-questions, each naming what a good answer looks like |
| GATHER | One subagent per sub-question over WebSearch and WebFetch; claims get URL, date, and source tier |
| TRIANGULATE | Findings merge; agreements and contradictions are both written out, never averaged |
| BRIEF | Verdict-first one-page markdown, every sentence cited `[n]`, source list at the end |
| SAVE | `research/<date>-<slug>.md`, then `citation_check.py` must exit 0 |

## Install

Option A: self-installable marketplace

1. Download or clone this repo into a folder.
2. In ZCode, open Plugin Marketplace, then Add, then Add Plugin Marketplace.
3. Paste the folder path, wait for it to load, then Install `deep-research`.

Option B: manual copy

Copy the `deep-research` folder into your workspace `plugins/` directory,
then restart ZCode.

## Try it

```
/deep-research which database handles time-series writes better, TimescaleDB or QuestDB, and what would you pick for a 50-node fleet?
```

Expected: a session that lists the sub-questions, runs the subagents, and
ends with `research/2026-10-29-timescaledb-vs-questdb.md` whose
`citation_check.py` run prints `OK`.

## Requirements

Python 3 (stdlib only). WebSearch and WebFetch tools in the session.
Network access for the subagents to fetch public pages.

---

<p align="center">
  <a href="https://z.ai/subscribe?ic=R0K78RJKNW"><img alt="z.ai coding plans - 10% OFF coupon" src="https://img.shields.io/badge/z.ai%20coding%20plans-10%25%20OFF%20coupon-blueviolet" /></a>
  <a href="https://zcode.z.ai/invite/ALWM9JUA"><img alt="Try ZCode free" src="https://img.shields.io/badge/Try%20ZCode-free%20invite-0969da" /></a>
</p>

## License

MIT
