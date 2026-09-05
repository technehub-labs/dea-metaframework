"""Smoke test for the cross-repo consumer CLI.

Runs the CLI in-process via `CliRunner.main` against a local cache
(no network). Verifies the CLI exits 0 and prints the expected
one-line-per-catalog rollup.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from tools.cross_repo_consumer import cli as cli_mod
from tools.cross_repo_consumer.tests.test_catalog_parser import (
    EMPTY_YAML_TEXT,
    SAMPLE_YAML_TEXT,
)


@pytest.fixture
def two_repos_in_cache(tmp_path):
    from pathlib import Path
    cache = Path(tmp_path) / "cache"
    cache.mkdir()
    (cache / "dea-catalog-processes@main.yaml").write_text(SAMPLE_YAML_TEXT)
    (cache / "dea-catalog-stakeholders@main.yaml").write_text(EMPTY_YAML_TEXT)
    return cache


def test_cli_runs_against_offline_cache(two_repos_in_cache, capsys) -> None:
    rc = cli_mod.main(
        [
            "--repos",
            "dea-catalog-processes",
            "dea-catalog-stakeholders",
            "--cache-dir",
            str(two_repos_in_cache),
            "--offline",
        ]
    )
    assert rc == 0
    captured = capsys.readouterr()
    assert "BP" in captured.out
    assert "SH" in captured.out
    assert "abbrev" in captured.out  # header line


def test_cli_failure_exit_code(two_repos_in_cache, capsys) -> None:
    rc = cli_mod.main(
        [
            "--repos",
            "dea-catalog-processes",
            "dea-catalog-does-not-exist",
            "--cache-dir",
            str(two_repos_in_cache),
            "--offline",
        ]
    )
    assert rc == 1
    captured = capsys.readouterr()
    assert "dea-catalog-does-not-exist" in captured.err
    assert "FileNotFoundError" in captured.err


def test_cli_default_repos_lists_all_four() -> None:
    """The CLI's default --repos includes all four known adopters."""
    # Parse-only; do not actually run.
    parser = cli_mod._build_parser()
    args = parser.parse_args([])
    assert set(args.repos) == {
        "dea-catalog-processes",
        "dea-catalog-business-capabilities",
        "dea-catalog-digital-business-service-factory",
        "dea-catalog-stakeholders",
    }


@pytest.mark.network
def test_live_fetch_against_real_catalog(tmp_path: Path) -> None:
    """Live fetch + parse against `dea-catalog-stakeholders` (smallest
    conforming adopter). Marked `network` so CI can opt out with
    `-m "not network"` when running offline.

    Asserts:
      - The fetch returns 200-class bytes.
      - The bytes parse as a Catalog.
      - counts.entities == 0 (stakeholders is a scaffold).
    """
    import urllib.error

    cache = tmp_path / "cache"
    try:
        res = cli_mod.fetch_catalog_yaml(
            "dea-catalog-stakeholders",
            cache_dir=cache,
            offline=False,
            timeout_s=10.0,
        )
    except urllib.error.URLError as exc:
        pytest.skip(f"network unreachable in this environment: {exc}")
    cat = cli_mod.parse_catalog_yaml(res.bytes)
    assert cat.metadata.abbreviation == "SH"
    assert cat.counts.entities == 0