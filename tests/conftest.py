"""Pytest fixtures for the catalog index machinery self-tests.

The self-tests in `tests/test_catalog_index_machinery.py` and
`tests/test_conformance_catalog_structure.py` are also runnable as
standalone modules (no pytest required), and pytest discovers them via
its standard test collection. This file bridges both runners.
"""

from __future__ import annotations

import shutil
from collections.abc import Generator
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_SRC = REPO_ROOT / "tools" / "catalog-index-schema.json"
TEMPLATE_SRC = REPO_ROOT / "tools" / "catalog-repo-template"


@pytest.fixture
def tmp_root(tmp_path: Path) -> Generator[Path, None, None]:
    """Return a tmp directory with the schema and template seeded.

    The regenerator expects `tools/catalog-index-schema.json` and the
    conformance suite expects `tools/catalog-repo-template/` (relative to
    the catalog root). Both fixtures place the seed under
    `<tmp_root>/tools/`.
    """
    tools_dst = tmp_path / "tools"
    tools_dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SCHEMA_SRC, tools_dst / "catalog-index-schema.json")
    shutil.copytree(TEMPLATE_SRC, tools_dst / "catalog-repo-template")
    yield tmp_path
    shutil.rmtree(tmp_path, ignore_errors=True)
