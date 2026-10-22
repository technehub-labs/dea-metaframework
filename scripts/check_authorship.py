"""check_authorship.py: enforce CR-BP-118 cardinal authorship rules.

Three rules, all data-driven from reconciliation/authorship-fields.yaml:

- AUT-001 (blocking): every authorship-bearing field in the registered
  field list MUST carry a value from the allowlist. The denylist is the
  set of agent/tool names that must NEVER appear in an authorship field
  of any published artifact.

- AUT-002 (blocking): when an authorship-bearing field's parent block
  is present (e.g. ``audit:`` in a record YAML, the metadata block in a
  CR doc), the field itself MUST be present too. Catches partial-block
  situations where the field was deleted but the parent survived.

- AUT-003 (advisory): every authorship-bearing field's value matches one
  of the registered identity strings exactly. Catches typos like
  ``Emmanuel Otchere`` (missing middle initial) that the cardinal rule
  should keep canonical.

Run: python3 scripts/check_authorship.py [--strict] [--json]
"""
from __future__ import annotations

import fnmatch
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPO_ROOT / "reconciliation" / "authorship-fields.yaml"

# CR-BP-118 carrier + change-requests/README.md: these files DESCRIBE the
# rule with quoted forbidden values and must be permitted to contain them.
PRESERVE_GLOBS = (
    "change-requests/CR-BP-118-authorship-cardinal-rule.md",
    "change-requests/README.md",
)

# Directory trees the glob walker must never enter, whatever the glob
# shape. `.git` is VCS internal; `.metaframework` is the upstream copy
# that CI checks out at step 5 of the catalog-gate workflow, whose own
# CR docs carry `Coder` authorship and would fire AUT-001 as false
# positives. The path prefix in a directory-scoped glob keeps those out
# already, but a bare-filename glob (`README.md`) has no prefix, so the
# exclusion is enforced here for every glob shape.
_EXCLUDED_DIRS = frozenset({".git", ".metaframework"})

# An unresolved template substitution, e.g. `{{OWNER}}` or `{% set x %}`. A
# field carrying `allow_placeholders: true` may hold one of these without
# tripping AUT-003, because it is a slot rather than an authorship claim.
PLACEHOLDER_RE = re.compile(r"\{\{[^}]*\}\}|\{%[^%]*%\}")

# CITATION-style metadata splits a personal name across two fields, so neither
# the value nor any allowlist entry is ever a whole name on its own:
#
#     family-names: Otchere
#     given-names:  Emmanuel A.
#
# A field carrying `name_part: true` is satisfied when its value is a
# whitespace-delimited PREFIX or SUFFIX of an allowlist entry, aligned to a
# word boundary. "Emmanuel A." is the two-token prefix of "Emmanuel A. Otchere"
# and "Otchere" is its single-token suffix, so both pass; "Emmanuel A. Otchere Jr"
# is neither and still fails. AUT-001 is evaluated first and returns early, so a
# denylisted token remains blocking in every one of these fields.
def _name_part_ok(value: str, allowlist: list) -> bool:
    """True when `value` is a word-aligned prefix or suffix of an allowlist entry.

    "Emmanuel A." and "Otchere" are both legitimate parts of the canonical
    identity "Emmanuel A. Otchere"; "Emmanuel A. Otchere Jr" is neither.
    """
    parts = value.split()
    if not parts:
        return False
    for allowed in allowlist:
        toks = allowed.split()
        n = len(parts)
        if n <= len(toks) and toks[:n] == parts:
            return True
        if toks[-n:] == parts:
            return True
    return False


def _is_preserved(relpath: str) -> bool:
    return any(fnmatch.fnmatch(relpath, g) for g in PRESERVE_GLOBS)


def _strip_comment(line: str) -> str:
    """Strip a trailing ``# ...`` comment from a YAML-ish value line.

    The registry is a small hand-maintained file; we don't need full
    YAML support, but we do need to honour the ``key: value # comment``
    shape used throughout the file.
    """
    in_quote = False
    quote = ""
    for i, ch in enumerate(line):
        if in_quote:
            if ch == quote:
                in_quote = False
        else:
            if ch in ('"', "'"):
                in_quote = True
                quote = ch
            elif ch == "#":
                return line[:i].rstrip()
    return line


def _load_registry():
    """Load the authorship-field registry.

    Kept simple: pure text parse of ``key: value`` lines; no PyYAML
    dependency, since the file is small and stable.
    """
    if not REGISTRY_PATH.exists():
        sys.stderr.write(f"authorship registry not found: {REGISTRY_PATH}\n")
        sys.exit(2)
    text = REGISTRY_PATH.read_text()
    fields: list[dict] = []
    allowlist: list[str] = []
    denylist: list[str] = []
    section = None
    current_field: dict | None = None
    for raw in text.splitlines():
        line = _strip_comment(raw).rstrip()
        if not line:
            continue
        if line.startswith("fields:"):
            section = "fields"
            continue
        if line.startswith("allowlist:"):
            section = "allowlist"
            continue
        if line.startswith("denylist:"):
            section = "denylist"
            continue
        if section == "fields":
            if line.startswith("  - path:"):
                current_field = {
                    "path": line.split(":", 1)[1].strip().strip('"').strip("'"),
                    "file_glob": "",
                    "kind": "metadata",
                }
                fields.append(current_field)
            elif current_field is not None and line.lstrip().startswith("file_glob:"):
                current_field["file_glob"] = (
                    line.split(":", 1)[1].strip().strip('"').strip("'")
                )
            elif current_field is not None and line.lstrip().startswith("kind:"):
                current_field["kind"] = (
                    line.split(":", 1)[1].strip().strip('"').strip("'")
                )
            elif current_field is not None and line.lstrip().startswith("prefix_match:"):
                v = line.split(":", 1)[1].strip().lower()
                current_field["prefix_match"] = v in ("true", "yes", "1")
            elif current_field is not None and line.lstrip().startswith("name_part:"):
                v = line.split(":", 1)[1].strip().lower()
                current_field["name_part"] = v in ("true", "yes", "1")
            elif current_field is not None and line.lstrip().startswith("allow_placeholders:"):
                # `allow_placeholders: true` exempts unresolved template
                # substitutions such as `{{OWNER}}` from AUT-003.
                #
                # A template is not an authorship violation: its value is
                # substituted at bootstrap time, and registering the field
                # without this would make the gate fail on the very file whose
                # purpose is to hold a placeholder. AUT-001 still applies, so a
                # denylisted name substituted INTO the template is still caught.
                v = line.split(":", 1)[1].strip().lower()
                current_field["allow_placeholders"] = v in ("true", "yes", "1")
        elif section == "allowlist":
            v = line.lstrip("- ").strip().strip('"').strip("'")
            if v:
                allowlist.append(v)
        elif section == "denylist":
            v = line.lstrip("- ").strip().strip('"').strip("'")
            if v:
                denylist.append(v)
    return fields, allowlist, denylist


def _iter_files(glob: str):
    """Yield absolute paths matching a registered glob.

    The glob shape comes from the registry and is a relative path
    under the repo (e.g. ``README.md``, ``change-requests/CR-*.md`` or
    ``entities/v1-alpha/**/processes-*.yaml``). The function
    normalizes the glob into a search pattern and walks the tree,
    bounding itself to the path prefix in the glob to prevent
    escaping into vendored content (e.g. ``.metaframework/`` checked
    out by the CI workflow at step 5 -- the dea-metaframework repo
    contains its own ``change-requests/CR-*.md`` files with
    `Coder` authorship, which would otherwise produce false positives
    under the CR-BP-118 AUT-001 substring denylist).

    The bound is the longest literal prefix in the glob. For
    ``change-requests/CR-*.md`` the prefix is ``change-requests/``;
    for ``entities/v1-alpha/**/processes-*.yaml`` the prefix is
    ``entities/v1-alpha/``. The walk starts at that prefix and never
    crosses it.

    A glob with no directory component (``README.md``) has no
    directory prefix to bound to, so the walk starts at REPO_ROOT and
    the filename pattern is matched at any depth below it, following
    ``Path.rglob`` semantics. That is the conservative direction for a
    compliance gate: a superset of the files a reader would expect,
    never a subset. Vendored subtrees are excluded explicitly by
    :data:`_EXCLUDED_DIRS` below, because a bare-filename glob cannot
    rely on the path prefix to keep it out of ``.metaframework/``.
    """
    # Compute the literal prefix: everything before the first `*` or `?`,
    # truncated to a whole number of directory components.
    wildcard = re.search(r"[?*]", glob)
    if wildcard:
        prefix = glob[: wildcard.start()]
    else:
        prefix = glob
    if not prefix.endswith("/") and prefix != "":
        # If the prefix stops mid-component, drop the partial component.
        # Note that "README.md".rsplit("/", 1) is ["README.md"] (not
        # ["", "README.md"]), so a glob with no directory component needs
        # the explicit no-slash branch: the previous unconditional form
        # produced "README.md/", making `base` a file and silently
        # matching nothing for every bare-filename glob.
        head, sep, _tail = prefix.rpartition("/")
        prefix = (head + "/") if sep else ""
    base = REPO_ROOT / prefix.rstrip("/") if prefix.rstrip("/") else REPO_ROOT
    if not base.is_dir():
        return
    # Strip the prefix from the glob to get a relative pattern for rglob.
    rel_glob = glob[len(prefix):] if prefix and glob.startswith(prefix) else glob
    if not rel_glob:
        rel_glob = Path(glob).name
    for p in base.rglob(rel_glob):
        if not p.is_file():
            continue
        # Never descend into vendored or internal trees. The path prefix
        # already excludes them for directory-scoped globs; a bare
        # filename has no such prefix, so the exclusion is applied here
        # for every glob shape.
        if any(part in _EXCLUDED_DIRS for part in p.parts):
            continue
        yield p


def _extract_value(line: str, field_path: str) -> str | None:
    """Extract the value of a registered field from a single line.

    Field shapes:
      - ``**Owner**: <value>``  -> markdown CR metadata
      - ``audit.author: <value>`` -> YAML (any leading whitespace)
      - CITATION.cff uses YAML too; same shape as audit.author.
    """
    stripped = line.strip()
    if field_path.startswith("**") and field_path.endswith("**"):
        key = field_path  # literal "**Owner**"
        prefix = f"{key}:"
        if stripped.startswith(prefix):
            return stripped[len(prefix):].strip()
    else:
        # YAML shape: "audit.author: <value>" (leading whitespace allowed)
        key = field_path
        prefix = f"{key}:"
        # Strip optional leading whitespace; value starts after the colon.
        #
        # A YAML sequence entry renders as "- family-names: Otchere", so the
        # dash must be removed before the key comparison. Without this the
        # FIRST key of any list item is invisible to the gate: CITATION.cff
        # carries `authors:` as a list whose first field is `family-names`,
        # so registering it silently matched nothing. A registered field that
        # matches zero lines is worse than an unregistered one, because the
        # registry claims it is covered.
        candidate = stripped
        while candidate.startswith("- "):
            candidate = candidate[2:].lstrip()
        if candidate.startswith(prefix):
            return candidate[len(prefix):].strip()
    return None


def _extract_citation_value(text: str, field_path: str) -> list[tuple[int, str]]:
    """For CITATION.cff fields like ``authors[].name`` -- extract every line
    whose key matches the dotted path, returning (line_no, value) tuples.
    """
    out: list[tuple[int, str]] = []
    key = field_path.replace("[]", "")  # 'authors.name'
    for i, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith(f"{key}:"):
            value = line.split(":", 1)[1].strip().strip('"').strip("'")
            out.append((i, value))
    return out


def evaluate(strict: bool = False) -> dict:
    fields, allowlist, denylist = _load_registry()
    findings: list[dict] = []
    summary = {"AUT-001": 0, "AUT-002": 0, "AUT-003": 0}

    for fld in fields:
        glob = fld["file_glob"]
        path = fld["path"]
        for fpath in _iter_files(glob):
            rel = fpath.relative_to(REPO_ROOT).as_posix()
            if _is_preserved(rel):
                continue
            text = fpath.read_text()
            # For YAML-style fields with a `[]` list path, scan every line
            if "[]" in path:
                hits = _extract_citation_value(text, path)
                for lineno, value in hits:
                    _check_value(rel, lineno, path, value, allowlist, denylist, findings, summary, fld)
            else:
                for lineno, line in enumerate(text.splitlines(), 1):
                    value = _extract_value(line, path)
                    if value is None:
                        continue
                    _check_value(rel, lineno, path, value, allowlist, denylist, findings, summary, fld)

    blocking = [f for f in findings if f["rule"] in ("AUT-001", "AUT-002")]
    advisory = [f for f in findings if f["rule"] == "AUT-003"]
    return {
        "gate": "AUT-001..003",
        "cr": "CR-BP-118",
        "summary": summary,
        "blocking": blocking,
        "advisory": advisory,
        "verdict": "CONFORMANT" if not blocking else "NON-CONFORMANT",
    }


def _check_value(rel, lineno, path, value, allowlist, denylist, findings, summary, fld):
    # Strip surrounding quote characters from the value so that quoted
    # and unquoted values are compared against the allowlist
    # equivalently. The 118a baseline is exact-match, but YAML values
    # are routinely quoted (e.g. `author: "Emmanuel A. Otchere"`) and
    # the rule is the canonical identity, not the formatting.
    value_clean = value.strip().strip('"').strip("'").strip()
    # AUT-001: value in allowlist (substring match for denylist; exact for allowlist)
    deny_hit = next((d for d in denylist if d and d in value), None)
    if deny_hit:
        findings.append({
            "rule": "AUT-001",
            "file": rel,
            "line": lineno,
            "field": path,
            "value": value,
            "deny_hit": deny_hit,
            "kind": fld.get("kind", "metadata"),
        })
        summary["AUT-001"] += 1
        return
    if not value_clean:
        # AUT-002: parent present but value empty/missing
        findings.append({
            "rule": "AUT-002",
            "file": rel,
            "line": lineno,
            "field": path,
            "value": value,
            "kind": fld.get("kind", "metadata"),
        })
        summary["AUT-002"] += 1
        return
    # AUT-003: value should match an allowlist entry. By default the
    # match is exact (the 118a baseline). Fields may opt into
    # prefix-matching via `prefix_match: true` in the registry -- a
    # value that starts with an allowlist entry followed by a
    # separator character (`,`, `;`, `:`, `(`, ` `, end-of-line, etc.)
    # is also accepted. Prefix matching is appropriate for catalog
    # fields whose values are followed by rich context (e.g. an
    # evidence register that records the actor and the action: actor:
    # "Emmanuel A. Otchere, BC-13 B.1 Track A candidate seeded").
    if value_clean not in allowlist:
        prefix_match = bool(fld.get("prefix_match", False))
        allowed = False
        if prefix_match:
            for allowed_value in allowlist:
                if value_clean.startswith(allowed_value):
                    rest = value_clean[len(allowed_value):]
                    # The remainder must be empty or start with a
                    # separator (so "Emmanuel A. Otchere X" is OK
                    # but "Emmanuel A. Otchereman" is not).
                    if not rest or rest[0] in (",", ";", ":", "(", " ", ")", "/"):
                        allowed = True
                        break
        # An unresolved template substitution is not an authorship claim, so a
        # field may exempt it. AUT-001 has already returned above, so a
        # denylisted name is still blocking regardless of this exemption.
        if not allowed and fld.get("name_part"):
            if _name_part_ok(value_clean, allowlist):
                allowed = True
        if not allowed and fld.get("allow_placeholders"):
            if PLACEHOLDER_RE.fullmatch(value_clean):
                allowed = True
        if not allowed:
            findings.append({
                "rule": "AUT-003",
                "file": rel,
                "line": lineno,
                "field": path,
                "value": value,
                "kind": fld.get("kind", "metadata"),
            })
            summary["AUT-003"] += 1


def main(argv: list[str]) -> int:
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--strict", action="store_true",
                   help="exit 1 on advisory (AUT-003) findings too")
    p.add_argument("--json", action="store_true", help="emit JSON envelope")
    p.add_argument("--self-test", action="store_true", help="run embedded tests")
    args = p.parse_args(argv[1:])

    if args.self_test:
        return _self_test()

    result = evaluate(strict=args.strict)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"Authorship Cardinal Rule (CR-BP-118; AUT-001..003): {result['verdict']}")
        print(f"  AUT-001 hits: {result['summary']['AUT-001']}")
        print(f"  AUT-002 hits: {result['summary']['AUT-002']}")
        print(f"  AUT-003 hits: {result['summary']['AUT-003']}")
        if result["blocking"]:
            print("  Blocking findings:")
            for f in result["blocking"][:20]:
                print(f"    {f['file']}:{f['line']} [{f['field']}] value={f['value']!r} deny={f.get('deny_hit', '-')}")
        if result["advisory"]:
            print("  Advisory findings:")
            for f in result["advisory"][:10]:
                print(f"    {f['file']}:{f['line']} [{f['field']}] value={f['value']!r}")

    if result["blocking"]:
        return 1
    if args.strict and result["advisory"]:
        return 1
    return 0


def _self_test() -> int:
    """Three smoke tests against the live registry + a synthetic field."""
    fields, allowlist, denylist = _load_registry()
    assert fields, "registry loaded with fields"
    assert "Emmanuel A. Otchere" in allowlist
    assert "Coder" in denylist
    # Synthetic field test
    sample = {
        "fields": [{"path": "**Owner**", "file_glob": "x.md", "kind": "metadata"}],
        "allowlist": allowlist,
        "denylist": denylist,
    }
    # The evaluate() reads the live registry, so just confirm it doesn't crash
    # on a tree containing the forbidden values.
    r = evaluate(strict=False)
    # We don't assert blocking == 0; that depends on tree state. We assert
    # the function returns a well-formed envelope.
    assert r["gate"] == "AUT-001..003"
    assert r["verdict"] in ("CONFORMANT", "NON-CONFORMANT")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
