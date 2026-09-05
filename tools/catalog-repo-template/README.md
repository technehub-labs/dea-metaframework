# {{CATALOG_NAME}}

**Catalog ID**: `{{CATALOG_ID}}`
**Layer**: L1 (Reference Catalog)
**Owner**: {{OWNER}}
**Authority**: Mandatory conformance to the catalog repository standard (CR-CATALOG-STRUCT-01).

This catalog hosts governed entities of one metamodel type. It was bootstrapped from
[`dea-metaframework/tools/catalog-repo-template/`](https://github.com/technehub-labs/dea-metaframework/tree/main/tools/catalog-repo-template)
via `tools/bootstrap_catalog_repo.py` (CR-CATALOG-STRUCT-06b).

## Quickstart

```bash
# Add your first entity
mkdir -p entities/v1-alpha/dea:your-entity-id
$EDITOR entities/v1-alpha/dea:your-entity-id/dea:your-entity-id.yaml

# Regenerate the index
python scripts/regenerate_catalog.py

# Validate
python scripts/check_catalog_index.py

# Run the cross-repo conformance suite
python ../dea-metaframework/tools/conformance_test_catalog_structure.py --catalog-root .
```

## Structure

```
.
├── CATALOG.yaml                    # machine-generated; do not hand-edit
├── TEMPLATE_VERSION                 # tracks template sync state
├── metamodel-pointer.yaml           # entity-to-metamodel mapping
├── README.md
├── CHANGELOG.md
├── LICENSE
├── NOTICE
├── CITATION.cff
├── entities/
│   └── v1-alpha/                    # one directory per entity
│       └── dea:your-entity-id/
│           ├── dea:your-entity-id.yaml    # canonical
│           ├── research/                  # research state
│           ├── candidates/                # candidate state
│           └── retired/                   # retired state
├── classifications/                 # controlled vocabularies
├── schemas/                         # JSON Schema files
├── scripts/                         # regenerator + gate (copies from dea-metaframework)
├── contributions/                   # contribution intake queue
├── change-requests/                 # CRs governing this catalog
└── .github/workflows/ci.yml         # CI gate
```

See the [catalog repository standard](https://github.com/technehub-labs/dea-metaframework/blob/main/docs/standards/catalog-repository-pattern.md)
for the full contract.

## Conformance

Run `python scripts/check_catalog_index.py --strict` to verify conformance. CI runs the
regenerator + gate on every PR; a stale `CATALOG.yaml` blocks merge.
