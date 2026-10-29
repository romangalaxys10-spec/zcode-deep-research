#!/usr/bin/env python3
"""citation_check.py: gate a deep-research brief for uncited claims and orphan markers.

Checks a markdown brief produced by the deep-research skill.

1. Bare claims. Every sentence in the body (the lines before the
   "## Sources" heading) must contain at least one [n] citation marker.
   Sentences without one are listed as violations with their line number
   and text. Exempt lines: headings, blank lines, lines that start with
   "Confidence:", and bullets whose whole content is "none" or
   "none found".
2. Orphan markers. Every [n] used in the body must match an entry in the
   "## Sources" section that starts with "[n] ".
3. Malformed source entries. Non-blank, non-heading lines inside the
   Sources section must start with "[n] ".

Unused source entries (defined but never cited) are reported as
warnings, not failures. Use --strict to make them failures too.

Exits:
  0  no violations (warnings may be printed)
  1  one or more violations, each printed on its own line
  2  usage or file error (missing path, unreadable file)

Python 3 stdlib only. Cross-OS.
"""
import argparse
import re
import sys
from pathlib import Path

CITE_RE = re.compile(r"\[(\d+)\]")
SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
EXEMPT_BULLETS = {"none", "none found", "no contradictions found", "empty"}


def split_sections(lines):
    """Return (body_lines, sources_lines, sources_start_lineno).

    The body is everything before the first heading that matches
    'Sources' (any level). If no such heading exists the whole file is
    the body and sources is empty.
    """
    idx = None
    for i, line in enumerate(lines):
        m = re.match(r"^(#{1,6})\s*Sources\b", line.strip(), re.IGNORECASE)
        if m:
            idx = i
            break
    if idx is None:
        return lines, [], None
    return lines[:idx], lines[idx + 1:], idx + 1


def check_body(body, body_offset):
    """Yield (line_number, text) for every bare-claim sentence."""
    for lineno, raw in enumerate(body, start=1 + body_offset):
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        if re.match(r"^Confidence:", stripped, re.IGNORECASE):
            continue
        content = re.sub(r"^[-*]\s*", "", stripped)
        if content.lower() in EXEMPT_BULLETS:
            continue
        # A blockquote or list marker may wrap the sentence; strip it.
        content = re.sub(r"^>\s*", "", content)
        for sentence in SENT_SPLIT_RE.split(content):
            s = sentence.strip()
            if not s:
                continue
            if not CITE_RE.search(s):
                yield lineno, s


def check_sources(sources, sources_offset):
    """Return (defined_numbers, malformed_lines)."""
    defined = []
    malformed = []
    for lineno, raw in enumerate(sources, start=1 + sources_offset):
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        m = re.match(r"^\[(\d+)\]\s", stripped)
        if m:
            defined.append(int(m.group(1)))
        else:
            malformed.append((lineno, stripped))
    return defined, malformed


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="citation_check.py",
        description="Validate that a deep-research brief cites every claim "
        "and that every citation maps to a source entry.",
    )
    parser.add_argument("brief", help="path to the markdown brief to check")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat unused source entries as failures (default: warning)",
    )
    args = parser.parse_args(argv)

    path = Path(args.brief)
    if not path.is_file():
        print(f"error: not a file: {path}", file=sys.stderr)
        return 2
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        print(f"error: cannot read {path}: {e}", file=sys.stderr)
        return 2

    lines = text.splitlines()
    body, sources, src_off = split_sections(lines)
    body_off = 0

    violations = []
    warnings = []

    for lineno, sentence in check_body(body, body_off):
        violations.append(f"bare claim (line {lineno}): {sentence}")

    cited = [int(n) for line in body for n in CITE_RE.findall(line)]
    defined, malformed = check_sources(sources, src_off)
    for lineno, entry in malformed:
        violations.append(f"malformed source entry (line {lineno}): {entry[:80]}")
    for n in sorted(set(cited)):
        if n not in defined:
            violations.append(f"orphan citation: [{n}] is used but not in the Sources section")
    for n in sorted(set(defined)):
        if n not in set(cited):
            msg = f"unused source entry: [{n}] is never cited"
            if args.strict:
                violations.append(msg)
            else:
                warnings.append(msg)

    for w in warnings:
        print(f"WARNING: {w}")
    for v in violations:
        print(f"VIOLATION: {v}")
    if violations:
        print(f"\nFAILED: {len(violations)} violation(s), {len(warnings)} warning(s)")
        return 1
    print(f"OK: {len(set(cited))} cited marker(s), {len(defined)} source entr"
          + ("y" if len(defined) == 1 else "ies") + f", {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
