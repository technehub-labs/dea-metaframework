"""Tests for the cross-repo consumer module (CR-CATALOG-STRUCT-07a).

All tests use the offline path: the parser is exercised against inline
YAML fixtures, and the fetcher is exercised against a local cache
directory (no network round-trips in CI). The end-to-end smoke path
(`test_cli_against_real_catalogs`) makes live fetches when a network
is available and skips otherwise.
"""

from __future__ import annotations

import pytest
import yaml

from tools.cross_repo_consumer import (
    Catalog,
    CatalogCounts,
    CatalogEntity,
    CatalogMetadata,
    aggregate_summary,
    parse_catalog_yaml,
    summary,
)
from tools.cross_repo_consumer.fetch import (
    DEFAULT_RAW_BASE,
    DEFAULT_TIMEOUT_S,
    FetchResult,
    fetch_catalog_yaml,
)


# ---------------------------------------------------------------------------
# Fixtures (module-level so other test files can import them)
# ---------------------------------------------------------------------------


# Mirrors the actual regenerator output schema:
#   id, type, state, path, lifecycle_status, version, last_modified,
#   research_count, candidate_count, canonical_count, retired_count.
# No `name`, no `tags` (those are NOT emitted by the regenerator).
SAMPLE_YAML_TEXT = """\
catalog:
  id: dea:catalog-processes
  name: Processes
  abbreviation: BP
  owner: TechNeHub Labs
  license: Apache-2.0
  repository: https://github.com/technehub-labs/dea-catalog-processes
  metamodel_version: "^0.2.1"
  description: Process definitions.
  counts:
    entities: 2
    canonical: 1
    candidates: 1
    retired: 0
    research_files: 3
    open_change_requests: 0
  entities:
    - id: dea:process-manage-customer-relationship
      type: Process
      state: canonical
      path: entities/v1-alpha/dea:process-manage-customer-relationship/dea:process-manage-customer-relationship.yaml
      lifecycle_status: active
      version: "1.0.0"
      last_modified: "2026-09-03"
      research_count: 1
      candidate_count: 0
      canonical_count: 1
      retired_count: 0
    - id: dea:process-onboard-supplier
      type: Process
      state: canonical
      path: entities/v1-alpha/dea:process-onboard-supplier/dea:process-onboard-supplier.yaml
      lifecycle_status: active
      version: "1.0.0"
      last_modified: "2026-09-03"
      research_count: 2
      candidate_count: 1
      canonical_count: 1
      retired_count: 0
"""

EMPTY_YAML_TEXT = """\
catalog:
  id: dea:catalog-stakeholders
  name: Stakeholders
  abbreviation: SH
  metamodel_version: "^0.2.1"
  counts:
    entities: 0
    canonical: 0
    candidates: 0
    retired: 0
    research_files: 0
    open_change_requests: 0
  entities: []
"""


@pytest.fixture
def sample_yaml_text() -> str:
    return SAMPLE_YAML_TEXT


@pytest.fixture
def empty_yaml_text() -> str:
    return EMPTY_YAML_TEXT


# ---------------------------------------------------------------------------
# parse_catalog_yaml
# ---------------------------------------------------------------------------


class TestParseCatalogYaml:
    def test_parses_minimal_catalog(self, sample_yaml_text: str) -> None:
        cat = parse_catalog_yaml(sample_yaml_text)
        assert isinstance(cat, Catalog)
        assert cat.metadata.id == "dea:catalog-processes"
        assert cat.metadata.abbreviation == "BP"
        assert cat.metadata.owner == "TechNeHub Labs"
        assert cat.metadata.license == "Apache-2.0"
        assert cat.metadata.metamodel_version == "^0.2.1"

    def test_counts_are_int(self, sample_yaml_text: str) -> None:
        cat = parse_catalog_yaml(sample_yaml_text)
        assert isinstance(cat.counts, CatalogCounts)
        assert cat.counts.entities == 2
        assert cat.counts.canonical == 1
        assert cat.counts.candidates == 1
        assert cat.counts.research_files == 3

    def test_entities_are_typed(self, sample_yaml_text: str) -> None:
        cat = parse_catalog_yaml(sample_yaml_text)
        assert len(cat.entities) == 2
        e = cat.entities[0]
        assert isinstance(e, CatalogEntity)
        assert e.id == "dea:process-manage-customer-relationship"
        assert e.type == "Process"
        assert e.state == "canonical"
        assert e.lifecycle_status == "active"
        assert e.version == "1.0.0"
        assert e.last_modified == "2026-09-03"
        assert e.research_count == 1

    def test_handles_bytes_input(self, sample_yaml_text: str) -> None:
        cat = parse_catalog_yaml(sample_yaml_text.encode("utf-8"))
        assert cat.metadata.abbreviation == "BP"

    def test_handles_empty_catalog(self, empty_yaml_text: str) -> None:
        cat = parse_catalog_yaml(empty_yaml_text)
        assert cat.counts.entities == 0
        assert cat.entities == ()
        assert cat.entity_ids == frozenset()

    def test_missing_top_level_catalog_key_raises(self) -> None:
        bad = yaml.safe_dump({"foo": "bar"})
        with pytest.raises(ValueError, match="top-level `catalog:` key"):
            parse_catalog_yaml(bad)

    def test_top_level_must_be_mapping(self) -> None:
        with pytest.raises(ValueError, match="top level"):
            parse_catalog_yaml("- just a list\n")

    def test_invalid_yaml_raises(self) -> None:
        with pytest.raises(yaml.YAMLError):
            parse_catalog_yaml("not: valid: yaml: at: all:\n")

    def test_entity_missing_id_raises(self) -> None:
        bad = yaml.safe_dump(
            {
                "catalog": {
                    "id": "x",
                    "name": "X",
                    "abbreviation": "X",
                    "counts": {},
                    "entities": [{"type": "X", "state": "canonical", "path": "x"}],
                }
            }
        )
        with pytest.raises(ValueError, match="missing required key 'id'"):
            parse_catalog_yaml(bad)

    def test_entity_missing_state_raises(self) -> None:
        bad = yaml.safe_dump(
            {
                "catalog": {
                    "id": "x",
                    "name": "X",
                    "abbreviation": "X",
                    "counts": {},
                    "entities": [{"id": "dea:x", "path": "x"}],
                }
            }
        )
        with pytest.raises(ValueError, match="missing required key 'state'"):
            parse_catalog_yaml(bad)

    def test_count_coercion_robust_to_strings(self) -> None:
        """Counts that arrive as strings (e.g. from a future regenerator
        change) coerce to int cleanly rather than crashing the parser."""
        doc = yaml.safe_dump(
            {
                "catalog": {
                    "id": "x",
                    "name": "X",
                    "abbreviation": "X",
                    "counts": {"entities": "5", "canonical": "5"},
                    "entities": [],
                }
            }
        )
        cat = parse_catalog_yaml(doc)
        assert cat.counts.entities == 5
        assert cat.counts.canonical == 5


# ---------------------------------------------------------------------------
# Catalog helpers
# ---------------------------------------------------------------------------


class TestCatalogHelpers:
    def test_entity_ids_set(self, sample_yaml_text: str) -> None:
        cat = parse_catalog_yaml(sample_yaml_text)
        assert cat.entity_ids == frozenset(
            {
                "dea:process-manage-customer-relationship",
                "dea:process-onboard-supplier",
            }
        )

    def test_entities_by_state(self, sample_yaml_text: str) -> None:
        cat = parse_catalog_yaml(sample_yaml_text)
        canonical = cat.entities_by_state("canonical")
        assert len(canonical) == 2
        candidate = cat.entities_by_state("candidate")
        assert candidate == ()

    def test_entities_by_lifecycle(self, sample_yaml_text: str) -> None:
        cat = parse_catalog_yaml(sample_yaml_text)
        active = cat.entities_by_lifecycle("active")
        assert len(active) == 2
        retired = cat.entities_by_lifecycle("retired")
        assert retired == ()

    def test_latest_last_modified(self, sample_yaml_text: str) -> None:
        cat = parse_catalog_yaml(sample_yaml_text)
        assert cat.latest_last_modified() == "2026-09-03"

    def test_latest_last_modified_empty(self, empty_yaml_text: str) -> None:
        cat = parse_catalog_yaml(empty_yaml_text)
        assert cat.latest_last_modified() is None

    def test_summary_one_line(self, sample_yaml_text: str) -> None:
        cat = parse_catalog_yaml(sample_yaml_text)
        s = summary(cat)
        assert "\n" not in s
        assert "BP" in s
        assert "2 entities" in s

    def test_aggregate_summary_sorted_by_abbreviation(
        self, sample_yaml_text: str, empty_yaml_text: str
    ) -> None:
        cats = [parse_catalog_yaml(sample_yaml_text), parse_catalog_yaml(empty_yaml_text)]
        agg = aggregate_summary(cats)
        lines = agg.splitlines()
        assert lines[0].startswith("abbrev")
        # Sorted by abbreviation (ASCII): BP (P=80) < SH (S=83)
        # summary() pads the abbreviation column to width 6, so lines
        # start with "  BP" / "    SH" rather than "BP"/"SH".
        data_rows = lines[2:]
        proc_rows = [i for i, r in enumerate(data_rows) if "BP" in r]
        sh_rows = [i for i, r in enumerate(data_rows) if "SH" in r]
        assert proc_rows == [0]
        assert sh_rows == [1]

    def test_aggregate_summary_empty(self) -> None:
        assert aggregate_summary([]) == "no catalogs"


# ---------------------------------------------------------------------------
# fetch_catalog_yaml (offline)
# ---------------------------------------------------------------------------


class TestFetchOffline:
    def test_offline_cache_hit(
        self, tmp_path, sample_yaml_text: str
    ) -> None:
        cache = tmp_path / "cache"
        cache.mkdir()
        (cache / "dea-catalog-processes@main.yaml").write_text(sample_yaml_text)
        res = fetch_catalog_yaml(
            "dea-catalog-processes",
            cache_dir=cache,
            offline=True,
        )
        assert isinstance(res, FetchResult)
        assert res.from_cache is True
        assert res.repo == "dea-catalog-processes"
        assert res.ref == "main"
        # Round-trip parses cleanly
        cat = parse_catalog_yaml(res.bytes)
        assert cat.metadata.abbreviation == "BP"

    def test_offline_cache_miss_raises(self, tmp_path) -> None:
        cache = tmp_path / "cache"
        cache.mkdir()
        with pytest.raises(FileNotFoundError, match="cache miss"):
            fetch_catalog_yaml(
                "dea-catalog-missing",
                cache_dir=cache,
                offline=True,
            )

    def test_ref_with_slash_is_flattened(
        self, tmp_path, sample_yaml_text: str
    ) -> None:
        cache = tmp_path / "cache"
        cache.mkdir()
        (cache / "dea-catalog-processes@feature_branch.yaml").write_text(
            sample_yaml_text
        )
        res = fetch_catalog_yaml(
            "dea-catalog-processes",
            ref="feature/branch",
            cache_dir=cache,
            offline=True,
        )
        assert res.from_cache is True


# ---------------------------------------------------------------------------
# FetchResult + constants
# ---------------------------------------------------------------------------


class TestModuleSurface:
    def test_default_raw_base(self) -> None:
        assert DEFAULT_RAW_BASE.startswith("https://raw.githubusercontent.com/")
        assert "{repo}" in DEFAULT_RAW_BASE
        assert "{ref}" in DEFAULT_RAW_BASE

    def test_default_timeout_is_positive(self) -> None:
        assert DEFAULT_TIMEOUT_S > 0

    def test_fetch_result_is_frozen(self) -> None:
        # dataclass(frozen=True) means assignment raises
        res = FetchResult(repo="x", ref="main", bytes=b"", from_cache=False)
        with pytest.raises((AttributeError, Exception)):
            res.repo = "y"  # type: ignore[misc]

    def test_metadata_is_frozen(self) -> None:
        m = CatalogMetadata(
            id="x", name="X", abbreviation="X", owner=None, license=None,
            repository=None, metamodel_version=None,
        )
        with pytest.raises((AttributeError, Exception)):
            m.abbreviation = "Y"  # type: ignore[misc]