"""dea-metaframework tooling package.

Why this file exists
--------------------
`tools/cross_repo_consumer/tests/` and `tools/cross_repo_consumer/` both
contain `__init__.py`, so pytest imports the consumer tests as the package
`tools.cross_repo_consumer.tests`. That import needs the repository root on
`sys.path` AND needs `tools` itself to resolve to THIS repo.

Without this file, `tools/` is an implicit namespace package. A namespace
package loses to any REGULAR package of the same name found elsewhere on
`sys.path`, regardless of path order, because a regular package wins the
name outright. Any environment that has an unrelated `tools` package
installed therefore shadows this repo's, and collection fails:

    E   ModuleNotFoundError: No module named 'tools.cross_repo_consumer'

That is not hypothetical: an editable install of an unrelated project
claiming the name `tools` reproduced it here. Neither `PYTHONPATH`, a
repo-root `conftest.py`, nor `[tool.pytest.ini_options] pythonpath`
resolved it, because each of those adjusts `sys.path` while the shadowing
is decided at the meta-path level.

Making `tools` a regular package settles the name against this repo. It is
also the honest declaration: `tools/` is a package of importable modules,
not a loose directory.
"""