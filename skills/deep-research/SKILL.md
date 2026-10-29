# Deep Research

Multi-source research that ends in a cited one-page brief. Use when the answer
needs more than one source, needs a verdict under contradictions, or needs to
be saved and re-read later. Skip it for single-fact lookups; a direct
WebSearch is enough there.

## Inputs

- The question (required). If empty, ask for it in one line and stop.
- A date horizon (optional, default: last 12 months unless the question is
  historical).
- A scope hint (optional: which regions, companies, or versions matter).

## Steps

### 1. SCOPE

Turn the question into 3 to 6 sub-questions. Each sub-question must be
answerable in one WebSearch pass and name its source type (vendor docs,
regulator filing, benchmark, press). Write down what a good answer looks like
for each: a number, a date, a named party, a behavior.

Output (to the session, not the brief):

```
Q: <original question>
Q1: <sub-question> | needs: <number | date | name | behavior>
Q2: ...
```

If a sub-question cannot be answered by public sources, say so now and mark it
out of scope instead of dragging it into GATHER.

### 2. GATHER

Fan out one subagent per sub-question using the Agent tool. Each subagent:

- Searches with WebSearch, fetches the top 2 to 4 results with WebFetch.
- Returns findings as: claim, exact URL, publication or retrieval date,
  source tier (primary disclosure, vendor doc, press, UGC).
- Marks secondhand claims: if the source is reporting what a third party said,
  the finding says "per <original party>, as reported by <source>".
- Notes reachability. If a source is paywalled or unreachable, record the
  title and URL with a `[paywalled]` or `[unreachable]` marker. Do not
  fabricate what is behind it.

Give each subagent this exact return format:

```
Qn findings:
- claim: <text>
  url: <exact>
  date: <YYYY-MM-DD or "unknown">
  tier: <primary | vendor | press | ugc>
  secondhand: yes|no
- ...
```

### 3. TRIANGULATE

Merge all findings in the session.

- Group claims that address the same sub-question.
- Where two sources agree, note: "A and B agree on X".
- Where they contradict, keep both, written as: "Source A (url, date) says
  X; source B (url, date) says Y." Never average, never pick the prettier
  one, never silently drop one.
- Downgrade any claim that exists only in UGC or is secondhand and uncorroborated.

### 4. BRIEF

Write a one-page markdown brief. Structure:

```markdown
# <question>

Verdict: <2-3 sentences, the direct answer or "undecided, because ...">

## Findings
<2-5 short sections; every factual sentence ends with a [n] marker>
Confidence: <high | medium | low> + one clause on why.

## Contradictions
<each pair of disagreeing sources, both named with dates; "none found" is a
valid entry>

## Open questions
<what the sources could not resolve; empty list is fine, "none" is not>

## Confidence note
<which sections rest on primary sources vs press vs uncorroborated claims>

## Sources
[1] <title> - <publisher> - <date> - <url>
[2] ...
```

Rules:

- No claim without a source. A sentence with no `[n]` is not allowed; if the
  fact is yours (an inference), write it as an inference and cite the inputs.
- Both sides of a contradiction appear in Findings and in Contradictions.
- Paywalled and unreachable sources appear in Sources with their marker.
- The whole brief fits one page. Cut detail, not citations.

### 5. SAVE

- Path: `research/<YYYY-MM-DD>-<slug>.md` under the workspace root. Slug is
  the question's core nouns, hyphenated, lowercase.
- Run the gate:

```
python3 skills/deep-research/scripts/citation_check.py research/<YYYY-MM-DD>-<slug>.md
```

- Exit 0 means the brief is clean. On exit 1, fix the listed bare claims or
  orphan markers and re-run until clean.
- Report the saved path to the user. Do not claim the brief is complete while
  the gate is failing.

## Limits

- This plugin cannot verify that a fetched page was not edited after fetch.
- Dates on the web are approximate; a source dated 2026 may describe a
  2024 event.
- Contradictions are reported, not resolved. The user picks the side.
- WebFetch fails on login-gated and region-blocked URLs; those end up in the
  `[paywalled]` / `[unreachable]` column, which is honest, not a gap.
