"""test_check_authorship.py: tests for the CR-BP-118 authorship gate.

Coverage:
- Registry loads with the expected fields, allowlist, denylist.
- Allowlist contains the canonical name + the org.
- Denylist contains every agent/tool name from CR-BP-118 R1.
- AUT-001 substring match catches forbidden values embedded in prose.
- AUT-002 fires when the field's parent block is present but the field
  itself is empty.
- AUT-003 fires for typos that pass AUT-001 but are not in the allowlist.
- Live tree contains zero AUT-001 blocking findings after the sweep
  (the CR's main acceptance criterion).
- The --json output envelope is stable.
- The --strict flag exits non-zero on advisory findings.
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_authorship.py"
REGISTRY = ROOT / "reconciliation" / "authorship-fields.yaml"


def _load_module():
    spec = importlib.util.spec_from_file_location("check_authorship_test", SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


MOD = _load_module()


def _run(args: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT, capture_output=True, text=True, **kwargs,
    )


def test_registry_exists():
    assert REGISTRY.exists(), f"missing authorship registry at {REGISTRY}"


def test_registry_loads_expected_fields():
    fields, _, _ = MOD._load_registry()
    paths = {f["path"] for f in fields}
    # Every repo's registry must have at least **Owner** and **Author**
    # (the 118a baseline CR-doc metadata fields). Other fields are
    # per-repo extensions.
    assert "**Owner**" in paths, (
        f"every repo's authorship registry must include **Owner**; got {paths}"
    )
    assert "**Author**" in paths, (
        f"every repo's authorship registry must include **Author**; got {paths}"
    )


def test_allowlist_contains_canonical_name_and_org():
    _, allowlist, _ = MOD._load_registry()
    assert "Emmanuel A. Otchere" in allowlist
    assert "TechNeHub Labs" in allowlist


@pytest.mark.parametrize("name", [
    "Coder", "Agent", "Hermes", "Claude", "GPT", "Cline",
    "OpenAI", "MiniMax", "MiniMax-M3",
])
def test_denylist_contains_agent_tool_names(name):
    _, _, denylist = MOD._load_registry()
    assert name in denylist


def _run_check(path: str, value: str, kind: str = "metadata"):
    _, allowlist, denylist = MOD._load_registry()
    findings: list[dict] = []
    summary = {"AUT-001": 0, "AUT-002": 0, "AUT-003": 0}
    fake_field = {"path": path, "file_glob": "x.md", "kind": kind}
    MOD._check_value("x.md", 1, path, value, allowlist, denylist, findings, summary, fake_field)
    return findings


def test_aut001_substring_match_catches_forbidden_embedded_in_prose():
    """A field value like 'Emmanuel A. Otchere (Coder for eaojnr)' must trip AUT-001
    because 'Coder' is a substring of the value."""
    findings = _run_check("**Owner**", "Emmanuel A. Otchere (Coder for eaojnr)")
    assert len(findings) == 1
    assert findings[0]["rule"] == "AUT-001"
    assert findings[0]["deny_hit"] == "Coder"


def test_aut002_fires_on_empty_value():
    findings = _run_check("audit.author", "")
    assert len(findings) == 1
    assert findings[0]["rule"] == "AUT-002"


def test_aut003_fires_on_canonical_typo():
    """'Emmanuel Otchere' (missing middle initial) is not in the allowlist
    and trips AUT-003 advisory."""
    findings = _run_check("**Owner**", "Emmanuel Otchere")
    assert len(findings) == 1
    assert findings[0]["rule"] == "AUT-003"
    assert findings[0]["value"] == "Emmanuel Otchere"


def test_clean_value_passes_all_rules():
    findings = _run_check("**Owner**", "Emmanuel A. Otchere")
    assert findings == []


def test_self_test_exits_zero():
    r = _run(["--self-test"])
    assert r.returncode == 0, f"self-test failed: {r.stdout}\n{r.stderr}"


def test_live_tree_has_zero_aut001_blocking_findings():
    """The main CR-BP-118a acceptance criterion: after the sweep, no
    AUT-001 (deny-list substring) finding in the live tree."""
    r = _run(["--json"])
    assert r.returncode == 0, f"gate non-conformant: {r.stdout}\n{r.stderr}"
    envelope = json.loads(r.stdout)
    assert envelope["gate"] == "AUT-001..003"
    assert envelope["summary"]["AUT-001"] == 0, (
        f"AUT-001 blocking findings remain after sweep: "
        f"{envelope['blocking'][:5]}"
    )


def test_json_output_envelope_schema_stable():
    r = _run(["--json"])
    envelope = json.loads(r.stdout)
    assert set(envelope.keys()) >= {
        "gate", "cr", "summary", "blocking", "advisory", "verdict",
    }
    assert set(envelope["summary"].keys()) == {"AUT-001", "AUT-002", "AUT-003"}


def test_strict_exits_zero_on_clean_tree():
    """The CR-BP-118a acceptance: --strict exit 0 after the sweep.
    AUT-003 advisory findings would fail --strict; the sweep should
    leave none."""
    r = _run(["--strict"])
    assert r.returncode == 0, f"--strict non-conformant: {r.stdout}\n{r.stderr}"


def test_iter_files_does_not_escape_into_metaframework():
    """Regression test for the CI-only false positive: the CI workflow
    fetches dea-metaframework into .metaframework/ at step 5. The
    dea-metaframework repo contains its own change-requests/CR-*.md
    files with `Coder` authorship, which would otherwise produce
    AUT-001 findings. The glob walker must bound itself to the
    path prefix in the glob (change-requests/) and not escape into
    vendored content.
    """
    import tempfile
    import re as _re
    from pathlib import Path
    # Sanity check: the gate's own _iter_files, when called against
    # the real REPO_ROOT, must NOT walk into .metaframework/ -- the
    # walker is now bounded by the glob's literal prefix. We assert
    # that no yielded path contains `.metaframework` for any
    # registered glob, since the real repo has no .metaframework/
    # directory at all (it only exists in CI). The stronger check
    # (that the walker is bounded) is implicit in the implementation:
    # the walker computes the prefix from the glob and walks from
    # REPO_ROOT / prefix.
    fields, _, _ = MOD._load_registry()
    for fld in fields:
        for fp in MOD._iter_files(fld["file_glob"]):
            rel = fp.relative_to(ROOT).as_posix()
            assert ".metaframework" not in rel, (
                f"glob {fld['file_glob']!r} escaped into vendored content: {rel}"
            )
    # Verify the glob-prefix-bounded walker logic: for a path-prefixed
    # glob like 'change-requests/CR-*.md', a real CR-*.md file
    # directly under REPO_ROOT (no change-requests/ prefix) must NOT
    # be picked up. This locks in the fix that the walker uses the
    # prefix, not the filename.
    with tempfile.TemporaryDirectory() as tmp:
        fake = Path(tmp) / "fake"
        fake.mkdir()
        (fake / "change-requests").mkdir()
        (fake / "change-requests" / "CR-IN-SCOPE.md").write_text("")
        # A file at the root with the same name -- should be skipped.
        (fake / "CR-AT-ROOT.md").write_text("")
        # The walker should NOT pick up CR-AT-ROOT.md because the glob
        # is bounded to the change-requests/ prefix.
        # We need to test the bounded walker directly, so we re-implement
        # the prefix computation here.
        glob = "change-requests/CR-*.md"
        wc = _re.search(r"[?*]", glob)
        prefix = glob[: wc.start()] if wc else glob
        if not prefix.endswith("/") and prefix:
            prefix = prefix.rsplit("/", 1)[0] + "/"
        base = fake / prefix.rstrip("/") if prefix.rstrip("/") else fake
        rel_glob = glob[len(prefix):]
        walked = [p.relative_to(fake).as_posix() for p in base.rglob(rel_glob)]
        assert "change-requests/CR-IN-SCOPE.md" in walked
        assert "CR-AT-ROOT.md" not in walked, (
            f"glob escaped its prefix; walked: {walked}"
        )


# --- Regression tests for the bare-filename glob false green ---------
# The walker's literal-prefix derivation used to produce "<glob>/" for a
# glob with no directory component, making `base` a file and matching
# nothing. The gate then reported CONFORMANT while inspecting zero files,
# which is a false green: indistinguishable from a passing gate. These
# tests lock in the fixed behaviour.


def _walker_against(tmp_root, glob, monkeypatch):
    """Call the real _iter_files with REPO_ROOT rebound to a temp tree."""
    spec = importlib.util.spec_from_file_location("check_authorship_probe", SCRIPT)
    assert spec is not None
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    monkeypatch.setattr(mod, "REPO_ROOT", tmp_root)
    return sorted(
        p.relative_to(tmp_root).as_posix() for p in mod._iter_files(glob)
    )


def test_bare_filename_glob_finds_root_level_file(monkeypatch):
    """A glob with no directory component must resolve its base to
    REPO_ROOT, not to REPO_ROOT/<filename>, and so must match the
    root-level file."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        fake = Path(tmp)
        (fake / "README.md").write_text("# hi\n")
        walked = _walker_against(fake, "README.md", monkeypatch)
        assert "README.md" in walked, (
            f"bare-filename glob matched nothing; walked: {walked}"
        )


def test_bare_filename_glob_does_not_escape_into_vendored_subtree(monkeypatch):
    """A bare-filename glob has no path prefix to bound it, so the
    vendored `.metaframework/` tree must be excluded explicitly or the
    upstream repo's own Coder-authored docs fire AUT-001."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        fake = Path(tmp)
        (fake / "README.md").write_text("# mine\n")
        vendored = fake / ".metaframework"
        vendored.mkdir()
        (vendored / "README.md").write_text("# upstream\n")
        walked = _walker_against(fake, "README.md", monkeypatch)
        assert "README.md" in walked
        assert ".metaframework/README.md" not in walked, (
            f"glob escaped into the vendored subtree; walked: {walked}"
        )


def test_bare_filename_glob_does_not_escape_into_git_dir(monkeypatch):
    """`.git` is internal to every repo and must never be walked."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        fake = Path(tmp)
        git = fake / ".git"
        git.mkdir()
        (git / "README.md").write_text("# internal\n")
        walked = _walker_against(fake, "README.md", monkeypatch)
        assert walked == [], (
            f"glob walked into .git; walked: {walked}"
        )


def test_denylisted_value_in_bare_filename_glob_now_fails_the_gate():
    """End-to-end: a denylisted value in a root-level README must make the
    gate exit non-zero. Before the fix this combination reported
    CONFORMANT because the glob matched no files."""
    import shutil
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        cat = Path(tmp) / "catalog"
        (cat / "scripts").mkdir(parents=True)
        (cat / "reconciliation").mkdir(parents=True)
        shutil.copy(SCRIPT, cat / "scripts" / "check_authorship.py")
        (cat / "README.md").write_text("# T\n\n**Owner**: Coder\n")
        (cat / "reconciliation" / "authorship-fields.yaml").write_text(
            "fields:\n"
            "  - path: \"**Owner**\"\n"
            "    file_glob: \"README.md\"\n"
            "    kind: \"metadata\"\n"
            "allowlist:\n"
            "  - \"TechNeHub Labs\"\n"
            "denylist:\n"
            "  - \"Coder\"\n"
        )
        r = subprocess.run(
            [sys.executable, str(cat / "scripts" / "check_authorship.py"), "--strict"],
            capture_output=True, text=True,
        )
        assert r.returncode != 0, (
            "denylisted value passed the gate: the bare-filename glob is "
            f"not being enforced\n{r.stdout}\n{r.stderr}"
        )
        assert "AUT-001" in (r.stdout + r.stderr)


def test_registered_globs_still_resolve_to_expected_file_sets(monkeypatch):
    """The fix must not change behaviour for the directory-scoped globs
    already in the registry. Each is still bounded to its own prefix."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        fake = Path(tmp)
        (fake / "change-requests").mkdir()
        (fake / "change-requests" / "CR-a.md").write_text("")
        (fake / "change-requests" / "CR-b.md").write_text("")
        (fake / "docs").mkdir()
        (fake / "docs" / "s.md").write_text("")
        # Same-named files outside each prefix must not be picked up.
        (fake / "CR-a.md").write_text("")
        (fake / "s.md").write_text("")
        assert _walker_against(fake, "change-requests/CR-*.md", monkeypatch) == [
            "change-requests/CR-a.md",
            "change-requests/CR-b.md",
        ]
        assert _walker_against(fake, "docs/*.md", monkeypatch) == ["docs/s.md"]


def test_missing_prefix_directory_yields_nothing_rather_than_raising(monkeypatch):
    """A glob whose prefix directory does not exist must yield nothing
    quietly, matching the pre-existing early-return behaviour."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        fake = Path(tmp)
        (fake / "README.md").write_text("")
        assert _walker_against(fake, "nowhere/CR-*.md", monkeypatch) == []


# ── CR-BP-118c: CITATION.cff authorship coverage ─────────────────────────────
# Two distinct defects, both of which left a REGISTERED field matching zero
# lines, which is worse than an unregistered one because the registry claims
# the field is covered.


def _cff_repo(tmp, cff_body, registry_extra=""):
    """Build a throwaway repo carrying a CFF file and a matching registry."""
    import shutil
    import tempfile
    holder = tempfile.TemporaryDirectory()
    cat = Path(holder.name) / "catalog"
    (cat / "scripts").mkdir(parents=True)
    (cat / "reconciliation").mkdir(parents=True)
    shutil.copy(SCRIPT, cat / "scripts" / "check_authorship.py")
    (cat / "CITATION.cff").write_text(cff_body)
    (cat / "reconciliation" / "authorship-fields.yaml").write_text(
        "fields:\n"
        '  - path: "given-names"\n'
        '    file_glob: "CITATION.cff"\n'
        '    kind: "cff-author"\n'
        "    name_part: true\n"
        '  - path: "family-names"\n'
        '    file_glob: "CITATION.cff"\n'
        '    kind: "cff-author"\n'
        "    name_part: true\n"
        + registry_extra +
        "allowlist:\n"
        '  - "Emmanuel A. Otchere"\n'
        "denylist:\n"
        '  - "Coder"\n'
    )
    return holder, cat


def _run_gate(cat):
    import subprocess
    return subprocess.run(
        [sys.executable, str(cat / "scripts" / "check_authorship.py"), "--strict"],
        capture_output=True, text=True,
    )


CFF_AUTHORS = (
    "cff-version: 1.2.0\n"
    "title: T\n"
    "authors:\n"
    "  - family-names: Otchere\n"
    "    given-names: Emmanuel A.\n"
)


def test_list_item_first_key_is_matched():
    """`- family-names: X` is the FIRST key of a YAML sequence item.

    Before the dash-stripping fix the registry entry matched zero lines, so a
    denylisted value here passed the gate silently.
    """
    holder, cat = _cff_repo(None, CFF_AUTHORS.replace("Otchere", "Coder"))
    try:
        r = _run_gate(cat)
        assert r.returncode != 0, (
            "denylisted family-names passed: the list-item dash is not stripped\n"
            f"{r.stdout}\n{r.stderr}"
        )
        # Assert on the finding detail, not the rule name: the header and the
        # "AUT-001 hits: N" summary line contain "AUT-001" on every run, so a
        # substring check on the rule name passes even when the value was only
        # rejected as an allowlist mismatch rather than as a denylisted name.
        assert "deny=Coder" in (r.stdout + r.stderr), (
            "family-names was rejected, but not as a denylisted name\n"
            f"{r.stdout}\n{r.stderr}"
        )
    finally:
        holder.cleanup()


def test_given_names_denylisted_fails():
    holder, cat = _cff_repo(None, CFF_AUTHORS.replace("Emmanuel A.", "Coder"))
    try:
        r = _run_gate(cat)
        assert r.returncode != 0, "denylisted given-names passed the gate"
        assert "deny=Coder" in (r.stdout + r.stderr), (
            "given-names was rejected, but not as a denylisted name\n"
            f"{r.stdout}\n{r.stderr}"
        )
    finally:
        holder.cleanup()


def test_split_name_parts_are_accepted():
    """`given-names: Emmanuel A.` and `family-names: Otchere` are legitimate
    halves of the canonical identity. Neither is a whole name on its own, so
    exact matching cannot accept them and a strict run would fail CI."""
    holder, cat = _cff_repo(None, CFF_AUTHORS)
    try:
        r = _run_gate(cat)
        assert r.returncode == 0, (
            "a correctly split canonical name was rejected\n"
            f"{r.stdout}\n{r.stderr}"
        )
    finally:
        holder.cleanup()


def test_name_part_mode_rejects_an_unrelated_name():
    """name_part must not become a blanket exemption: a name that is not a
    prefix or suffix of the allowlist entry is still a finding."""
    holder, cat = _cff_repo(None, CFF_AUTHORS.replace("Emmanuel A.", "Someone Else"))
    try:
        r = _run_gate(cat)
        assert r.returncode != 0, "an unrelated name passed under name_part"
        assert "Someone Else" in (r.stdout + r.stderr), (
            "the unrelated name was not reported\n" + r.stdout + r.stderr
        )
    finally:
        holder.cleanup()


def test_allow_placeholders_exempts_template_slot():
    """A template field holds a substitution slot, not an authorship claim."""
    import shutil
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        cat = Path(tmp) / "catalog"
        (cat / "scripts").mkdir(parents=True)
        (cat / "reconciliation").mkdir(parents=True)
        shutil.copy(SCRIPT, cat / "scripts" / "check_authorship.py")
        (cat / "README.md").write_text("# T\n\n**Owner**: {{OWNER}}\n")
        (cat / "reconciliation" / "authorship-fields.yaml").write_text(
            "fields:\n"
            '  - path: "**Owner**"\n'
            '    file_glob: "README.md"\n'
            '    kind: "metadata"\n'
            "    allow_placeholders: true\n"
            "allowlist:\n"
            '  - "Emmanuel A. Otchere"\n'
            "denylist:\n"
            '  - "Coder"\n'
        )
        r = _run_gate(cat)
        assert r.returncode == 0, (
            "an unresolved template placeholder failed the gate\n"
            f"{r.stdout}\n{r.stderr}"
        )


def test_allow_placeholders_does_not_excuse_a_denylisted_substitution():
    """The exemption covers the SLOT, not whatever is later substituted into
    it. AUT-001 returns before AUT-003, so this must still be blocking."""
    import shutil
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        cat = Path(tmp) / "catalog"
        (cat / "scripts").mkdir(parents=True)
        (cat / "reconciliation").mkdir(parents=True)
        shutil.copy(SCRIPT, cat / "scripts" / "check_authorship.py")
        (cat / "README.md").write_text("# T\n\n**Owner**: Coder\n")
        (cat / "reconciliation" / "authorship-fields.yaml").write_text(
            "fields:\n"
            '  - path: "**Owner**"\n'
            '    file_glob: "README.md"\n'
            '    kind: "metadata"\n'
            "    allow_placeholders: true\n"
            "allowlist:\n"
            '  - "Emmanuel A. Otchere"\n'
            "denylist:\n"
            '  - "Coder"\n'
        )
        r = _run_gate(cat)
        assert r.returncode != 0, "allow_placeholders excused a denylisted value"


def test_live_citation_file_is_conformant_under_strict():
    """The real CITATION.cff must stay clean, or CI goes red on merge."""
    citation = ROOT / "CITATION.cff"
    if not citation.exists():
        pytest.skip("no CITATION.cff at repo root")
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--strict"],
        capture_output=True, text=True, cwd=ROOT,
    )
    assert r.returncode == 0, f"live tree is not conformant\n{r.stdout}\n{r.stderr}"


# ---------------------------------------------------------------------------
# Catalog repo template registry (Slice 3b-5)
#
# The template ships its OWN registry, not a copy of this repo's. Its CITATION
# author field was withheld between v2.6.0 and v2.7.0 because the gate could
# not match the YAML list-item form, and the registry recorded that reason.
# PR #48 fixed the extractor, so the field is now registered.
#
# These tests pin that the field is actually ARMED. A registered field that
# matches zero lines is worse than an unregistered one, because the registry
# claims coverage while the gate scans nothing.
# ---------------------------------------------------------------------------

TEMPLATE_REGISTRY = ROOT / "tools" / "catalog-repo-template" / "reconciliation" / "authorship-fields.yaml"


def _template_catalog(tmp_path: Path) -> Path:
    """Build a catalog repo carrying the gate plus the TEMPLATE registry.

    The gate resolves REPO_ROOT and REGISTRY_PATH from its own location, so
    running it against a foreign catalog requires the script to sit inside
    that catalog. Copying it in is what makes the template's registry the one
    under test.
    """
    cat = tmp_path / "template-catalog"
    shutil.copytree(ROOT / "tools" / "catalog-repo-template", cat)
    (cat / "scripts").mkdir(exist_ok=True)
    shutil.copy2(SCRIPT, cat / "scripts" / "check_authorship.py")
    return cat


def test_template_registry_registers_citation_name():
    """The template registry must carry CITATION authors[].name."""
    assert TEMPLATE_REGISTRY.exists(), f"missing {TEMPLATE_REGISTRY}"
    text = TEMPLATE_REGISTRY.read_text(encoding="utf-8")
    assert 'path: "name"' in text, "template registry does not register CITATION authors[].name"
    assert "CITATION.cff" in text, "template registry has no CITATION.cff glob"
    # The stale blocker note must not survive: it would tell a future reader
    # the field is unreachable when the extractor now matches it.
    assert "deliberately NOT registered" not in text, (
        "template registry still claims CITATION cannot be registered; PR #48 "
        "fixed the list-item extraction that was the stated blocker"
    )


def test_template_citation_field_accepts_legitimate_name(tmp_path: Path):
    """A bootstrapped catalog passes: the real owner name is allowlisted."""
    cat = _template_catalog(tmp_path)
    (cat / "CITATION.cff").write_text(
        'cff-version: 1.2.0\nauthors:\n  - name: "Emmanuel A. Otchere"\n',
        encoding="utf-8",
    )
    r = _run_gate(cat)
    assert r.returncode == 0, f"legitimate CITATION author should pass\n{r.stdout}\n{r.stderr}"


def test_template_citation_field_catches_denylisted_name(tmp_path: Path):
    """The armed field must actually fire. This is the negative test.

    Without the dash-stripping fix, `- name: "Coder"` matched no registered
    key and the gate reported CONFORMANT: the registry looked complete and
    scanned nothing.
    """
    cat = _template_catalog(tmp_path)
    (cat / "CITATION.cff").write_text(
        'cff-version: 1.2.0\nauthors:\n  - name: "Coder"\n',
        encoding="utf-8",
    )
    r = _run_gate(cat)
    assert r.returncode != 0, "denylisted CITATION author passed the gate"
    # Assert on the discriminating token, not the rule name: "AUT-001" also
    # appears in the summary header on every run, so asserting on it passes
    # whether or not the rule fired.
    assert "deny=Coder" in (r.stdout + r.stderr), (
        f"gate failed without naming the denied value\n{r.stdout}\n{r.stderr}"
    )


def test_template_citation_placeholder_is_exempt(tmp_path: Path):
    """The shipped template still holds {{OWNER}}; that slot is not a claim."""
    cat = _template_catalog(tmp_path)
    (cat / "CITATION.cff").write_text(
        'cff-version: 1.2.0\nauthors:\n  - name: "{{OWNER}}"\n',
        encoding="utf-8",
    )
    r = _run_gate(cat)
    assert r.returncode == 0, (
        f"unresolved placeholder should be exempt\n{r.stdout}\n{r.stderr}"
    )
