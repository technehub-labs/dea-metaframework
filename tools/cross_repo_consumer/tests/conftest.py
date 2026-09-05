# Pytest configuration for the cross-repo consumer tests.

# Register the `network` marker so pytest -m network does not warn.
markers = [
    "network: tests that require live network access (deselect with -m 'not network')",
]