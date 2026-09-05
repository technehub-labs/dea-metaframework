"""Pytest fixtures for the catalog index machinery self-tests.

The self-tests in `tests/test_catalog_index_machinery.py` are also runnable
as a standalone module (no pytest required), and pytest discovers them via
its standard test collection. This file bridges both runners: pytest sees
the `tmp_root` fixture below; the standalone runner uses
`tests/test_catalog_index_machinery.py:make_tmp_root()`.
"""

from __future__ import annotations

import shutil
from collections.abc import Generator
from pathlib import Path

import pytest


@pytest.fixture
def tmp_root(tmp_path: Path) -> Generator[Path, None, None]:
    """Return a tmp directory; copy the schema into it so the regenerator
    can find `tools/catalog-index-schema.json` at its default location."""
    schema_src = Path(__file__).resolve().parent.parent / "tools" / "catalog-index-schema.json"
    schema_dst = tmp_path / "tools" / "catalog-index-schema.json"
    schema_dst.parent.mkdir(parents=True, exist_ok=True)
    schema_dst.write_bytes(schema_src.read_bytes())
    yield tmp_path
    shutil.rmtree(tmp_path, ignore_errors=True)
