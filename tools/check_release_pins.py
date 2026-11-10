#!/usr/bin/env python3
"""Release-pin truth check (CR-CATALOG-STRUCT-13).

Every `ref:` this repository advertises for its own toolchain -- the
catalog-repo template's CI fetch, the kit generator's emitted pins
(`metaframework_pin:` dependency-manifest note, the emitted workflow's
metaframework checkout, the README dependency table) -- must resolve to
a release tag that EXISTS on origin. A pin merged ahead of its release
is a distributed outage: every consumer that re-syncs onto it 404s at
checkout (observed 2026-11-11: a consumer pinned v2.8.0 the day the
release was not yet cut, and its catalog-conformance went red
org-visibly). The ordering rule this gate enforces:

    land the change -> cut the release -> bump the pins (own PR)

a pin bump and the release cut are separate steps, and this gate fails
the bump if run while the tag is missing.

Scope: only *metaframework* pins are checked. Root-model pins
(`--root-ref`, e.g. OpenDEAM v0.9.0 against dea-architecture-framework)
and any other upstream's refs are out of scope here.

Usage:
    python tools/check_release_pins.py [--root PATH] [--skip-network]
Exit codes: 0 all pins resolve; 1 a pinned tag does not exist; 2 usage/IO error.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

UPSTREAM_REPOSITORY = "technehub-labs/dea-metaframework"
UPSTREAM_URL = f"https://github.com/{UPSTREAM_REPOSITORY}.git"
_TAG = r"v\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?"

# metaframework_pin: v2.7.0        (dependencies.yaml template)
_METAFRAMEWORK_PIN_RE = re.compile(rf"metaframework_pin:\s*({_TAG})")
# metaframework v2.7.0             (README dependency-table row)
_METAFRAMEWORK_TABLE_RE = re.compile(rf"metaframework\s+({_TAG})\b")
# ref: vX.Y.Z scoped to a step that checks out the upstream repo
_STEP_SPLIT_RE = re.compile(r"(?=\n\s*-?\s*uses:)")
_REF_RE = re.compile(rf"^\s*ref:\s*[\"']?({_TAG})", re.MULTILINE)
_REPO_RE = re.compile(rf"repository:\s*{re.escape(UPSTREAM_REPOSITORY)}")


def extract_pins(text: str) -> list[str]:
    """Metaframework release-tag pins advertised by one file's text.

    `ref:` values count only inside a step that names the upstream
    repository, so a `ref:` belonging to another action (e.g. the
    validate-allocation reusable call pinned to a root-model ref) is
    never mistaken for a metaframework pin.
    """
    pins: list[str] = []
    pins += _METAFRAMEWORK_PIN_RE.findall(text)
    pins += _METAFRAMEWORK_TABLE_RE.findall(text)
    for block in _STEP_SPLIT_RE.split(text):
        if _REPO_RE.search(block):
            pins += _REF_RE.findall(block)
    return sorted(set(pins))


def _scan_targets(root: Path) -> list[Path]:
    targets: list[Path] = [root / "tools" / "generate_catalog_kit.py"]
    template = root / "tools" / "catalog-repo-template"
    if template.is_dir():
        targets += [p for p in sorted(template.rglob("*")) if p.is_file()]
    return [p for p in targets if p.is_file()]


def _existing_tags() -> set[str] | None:
    """All release tags on origin, or None when ls-remote fails."""
    try:
        proc = subprocess.run(
            ["git", "ls-remote", "--tags", UPSTREAM_URL],
            capture_output=True, text=True, timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    tags = set()
    for line in proc.stdout.splitlines():
        ref = line.rsplit("\t", 1)[-1]
        m = re.fullmatch(r"refs/tags/(v\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?)(\^\{\})?", ref)
        if m:
            tags.add(m.group(1))
    return tags


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    ap.add_argument("--skip-network", action="store_true",
                    help="print the pins that would be checked and exit 0")
    args = ap.parse_args()

    targets = _scan_targets(args.root)
    if not targets:
        print(f"ERROR: no scan targets under {args.root}", file=sys.stderr)
        return 2

    found: dict[str, list[str]] = {}
    for path in targets:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for pin in extract_pins(text):
            found.setdefault(pin, []).append(str(path.relative_to(args.root)))

    if not found:
        print("ERROR: no metaframework pins found in the scan targets; "
              "the scan patterns are stale", file=sys.stderr)
        return 2

    print(f"metaframework release pins advertised ({len(found)} distinct):")
    for pin in sorted(found):
        print(f"  {pin}  ({', '.join(sorted(set(found[pin])))})")

    if args.skip_network:
        print("skip-network: existence not checked")
        return 0

    tags = _existing_tags()
    if tags is None:
        print("ERROR: could not list origin tags (ls-remote failed); "
              "a finding must never fire on a transport flake, re-run", file=sys.stderr)
        return 2

    missing = [pin for pin in sorted(found) if pin not in tags]
    if missing:
        for pin in missing:
            print(f"FAIL: pin {pin} does not exist on {UPSTREAM_REPOSITORY}; "
                  f"cut the release first (tag at the intended merge commit, "
                  f"then attach the GitHub release), in that order")
        return 1
    print(f"OK: all {len(found)} pins resolve to existing release tags")
    return 0


if __name__ == "__main__":
    sys.exit(main())
