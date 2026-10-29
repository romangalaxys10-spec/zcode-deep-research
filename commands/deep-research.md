---
description: Run a multi-source research question into a cited one-page brief
allowed-tools: Agent, WebSearch, WebFetch, Read, Write, Bash
argument-hint: <research question>
---
Invoke the `deep-research` skill with this input: **$ARGUMENTS**

If no question is given, ask for one in a single line and stop.
The run always ends with `citation_check.py` passing on the saved brief;
report the saved path and the gate result, and state any open questions.
