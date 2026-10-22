"""Pytest configuration for the cross-repo consumer tests.

Registers the `network` marker so pytest -m network does not warn, and
puts the repository root on sys.path.

The sys.path entry is load-bearing, not a convenience. This directory
contains an `__init__.py`, so pytest imports these modules as the
package `tools.cross_repo_consumer.tests`, which requires the repo root
to be importable. Without it, collection fails with
`ModuleNotFoundError: No module named 'tools'`.

That failure was invisible in CI only by accident: the workflow runs
`pytest -q tests/ tools/cross_repo_consumer/tests/`, and collecting
`tests/` first loads `tests/conftest.py`, whose module-level
`sys.path.insert(0, str(REPO_ROOT / "tools"))` side effect happens to
leave the root importable. Running the consumer tests on their own fails:

    pytest -q tools/cross_repo_consumer/tests/   -> ModuleNotFoundError

Declaring the dependency here makes the suite independently runnable and
removes the ordering dependency.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

markers = [
    "network: tests that require live network access (deselect with -m 'not network')",
]