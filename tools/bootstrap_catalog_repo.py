"""Catalog repo bootstrap script (CR-CATALOG-STRUCT-06b).

Bootstraps a new TechNeHub Labs catalog repo from
`tools/catalog-repo-template/`. Per the standard's §12 new-repo gate,
future catalog repos MUST be bootstrapped from the template (or be
brought into conformance manually before being referenced by
`dea-metamodel` consumers).

What the script does:

1. Copies the template directory to the target path.
2. Substitutes the catalog id and repo URL into the templated files.
3. Writes a `TEMPLATE_VERSION` file into the new catalog at the
   template's current version.
4. Optionally runs `git init` and stages all files.
5. Optionally creates the GitHub repo via `gh repo create`.

What the script does NOT do:

- It does not run the conformance suite (run it separately).
- It does not publish anything (push is the user's choice).
- It does not pull in any third-party deps (stdlib only).

Convention: zero third-party dependencies. The module imports only from
the standard library so it works in the bare CI image (consistent with
`tools/regenerate_catalog.py` and the rest of `tools/`).

Usage:
  python tools/bootstrap_catalog_repo.py \\
      --target PATH \\
      --catalog-id dea:catalog-foo \\
      --catalog-name "Foo Catalog" \\
      --catalog-abbreviation FC \\
      --owner "TechNeHub Labs" \\
      [--repo-url URL] [--git-init] [--gh-create {public,private,no}]
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml  # type: ignore

DEFAULT_TEMPLATE_ROOT = "tools/catalog-repo-template"

# Templated files: these have placeholder strings replaced during bootstrap.
# Templating is intentionally simple (one pass of str.replace per file).
# No Jinja; no cookiecutter. This matches the D-006 hand-rolled template
# decision from CR-CATALOG-STRUCT-06a planning.
PLACEHOLDERS = {
    "{{CATALOG_ID}}": None,             # replaced via --catalog-id
    "{{CATALOG_NAME}}": None,           # replaced via --catalog-name
    "{{CATALOG_ABBREVIATION}}": None,   # replaced via --catalog-abbreviation
    "{{OWNER}}": None,                 # replaced via --owner
    "{{REPO_URL}}": None,              # replaced via --repo-url (or empty)
    "{{YEAR}}": None,                  # replaced with current UTC year
}


def read_template_version(template_root: Path) -> str:
    """Read the template's TEMPLATE_VERSION file; default to '0.0.0' if missing."""
    path = template_root / "TEMPLATE_VERSION"
    if not path.is_file():
        return "0.0.0"
    return path.read_text(encoding="utf-8").strip()


def current_year() -> str:
    from datetime import datetime, timezone
    return str(datetime.now(tz=timezone.utc).year)


def render_text(content: str, replacements: dict[str, str]) -> str:
    out = content
    for placeholder, value in replacements.items():
        out = out.replace(placeholder, value)
    return out


def is_templated(path: Path) -> bool:
    """Heuristic: a file is templated if its name ends in .yaml, .yml, .md, or .json,
    OR if it's `metamodel-pointer.yaml` / `README.md` / `CHANGELOG.md`. Templates
    intentionally keep binary files (.gitignore-style) unrendered.
    """
    if path.suffix in (".yaml", ".yml", ".md", ".json", ".txt"):
        return True
    return path.name in ("LICENSE", "NOTICE", "CITATION.cff")


def render_template_file(
    src: Path,
    dst: Path,
    replacements: dict[str, str],
) -> None:
    """Copy src to dst, applying placeholder substitution if the file is templated."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    if is_templated(src):
        try:
            content = src.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            shutil.copy2(src, dst)
            return
        rendered = render_text(content, replacements)
        dst.write_text(rendered, encoding="utf-8")
    else:
        shutil.copy2(src, dst)


def build_metamodel_pointer(replacements: dict[str, str]) -> dict[str, Any]:
    """Build the metamodel-pointer.yaml content for the new catalog."""
    return {
        "id": replacements["{{CATALOG_ID}}"],
        "name": replacements["{{CATALOG_NAME}}"],
        "abbreviation": replacements["{{CATALOG_ABBREVIATION}}"],
        "version": "0.1.0",
        "status": "active",
        "metamodel_version": "1.0.0",
        "description": (
            f"Reference catalog for {replacements['{{CATALOG_NAME}}']} entities. "
            "Bootstrapped from dea-metaframework/tools/catalog-repo-template/."
        ),
        "owner": replacements["{{OWNER}}"],
    }


def git_init(target: Path) -> tuple[int, str]:
    """Run `git init` in target; return (returncode, stderr)."""
    try:
        result = subprocess.run(
            ["git", "init"],
            cwd=str(target),
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return 1, str(exc)
    return result.returncode, result.stderr


def git_add_all(target: Path) -> tuple[int, str]:
    """Run `git add -A` in target; return (returncode, stderr)."""
    try:
        result = subprocess.run(
            ["git", "add", "-A"],
            cwd=str(target),
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return 1, str(exc)
    return result.returncode, result.stderr


def gh_create(target: Path, visibility: str, repo_url: str | None) -> tuple[int, str]:
    """Run `gh repo create`; return (returncode, stderr)."""
    if visibility == "no":
        return 0, ""
    cmd = ["gh", "repo", "create", "--source", str(target), "--" + visibility]
    if repo_url:
        cmd.extend(["--remote", "origin", "--push"])
    try:
        result = subprocess.run(
            cmd,
            cwd=str(target),
            capture_output=True,
            text=True,
            timeout=120,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return 1, str(exc)
    return result.returncode, result.stderr


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Bootstrap a new catalog repo from tools/catalog-repo-template/ (CR-CATALOG-STRUCT-06b)."
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Target directory for the new catalog (created if absent).",
    )
    parser.add_argument(
        "--catalog-id",
        required=True,
        help="Canonical catalog id, e.g. dea:catalog-foo.",
    )
    parser.add_argument(
        "--catalog-name",
        required=True,
        help="Human-readable catalog name (used in README, pointer, CHANGELOG).",
    )
    parser.add_argument(
        "--catalog-abbreviation",
        default=None,
        help="Short abbreviation (default: derived from catalog name).",
    )
    parser.add_argument(
        "--owner",
        default="TechNeHub Labs",
        help="Owning organization (default: TechNeHub Labs).",
    )
    parser.add_argument(
        "--repo-url",
        default=None,
        help="Origin URL for the catalog (optional; can be set later via `git remote add`).",
    )
    parser.add_argument(
        "--template-root",
        default=DEFAULT_TEMPLATE_ROOT,
        help=f"Path to the canonical template (default: {DEFAULT_TEMPLATE_ROOT}).",
    )
    parser.add_argument(
        "--git-init",
        action="store_true",
        help="Run `git init` and `git add -A` in the target.",
    )
    parser.add_argument(
        "--gh-create",
        choices=["public", "private", "no"],
        default="no",
        help="Create the GitHub repo via `gh` (default: no).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the target directory if it exists.",
    )
    args = parser.parse_args(argv)

    template_root = Path(args.template_root).resolve()
    target = Path(args.target).resolve()

    if not template_root.is_dir():
        print(f"ERROR: template root {template_root} is not a directory", file=sys.stderr)
        return 1

    if target.exists():
        if not args.force:
            print(
                f"ERROR: target {target} already exists; pass --force to overwrite",
                file=sys.stderr,
            )
            return 1
        if target.is_dir():
            shutil.rmtree(target)
        else:
            target.unlink()

    abbreviation = args.catalog_abbreviation or args.catalog_name.split()[0][:4].upper()

    replacements: dict[str, str] = {
        "{{CATALOG_ID}}": args.catalog_id,
        "{{CATALOG_NAME}}": args.catalog_name,
        "{{CATALOG_ABBREVIATION}}": abbreviation,
        "{{OWNER}}": args.owner,
        "{{REPO_URL}}": args.repo_url or "",
        "{{YEAR}}": current_year(),
    }

    # Copy every file in the template, rendering placeholders for templated files.
    target.mkdir(parents=True, exist_ok=True)
    for src in sorted(template_root.rglob("*")):
        if not src.is_file():
            continue
        # Skip the template's own TEMPLATE_VERSION (the catalog gets its own).
        if src.name == "TEMPLATE_VERSION" and src.parent == template_root:
            continue
        rel = src.relative_to(template_root)
        dst = target / rel
        render_template_file(src, dst, replacements)

    # Overwrite metamodel-pointer.yaml with the bootstrap's authoritative version.
    pointer = build_metamodel_pointer(replacements)
    (target / "metamodel-pointer.yaml").write_text(
        yaml.safe_dump(pointer, sort_keys=True, default_flow_style=False, allow_unicode=True),
        encoding="utf-8",
    )

    # Write the catalog's TEMPLATE_VERSION (matches the template at bootstrap time).
    template_version = read_template_version(template_root)
    (target / "TEMPLATE_VERSION").write_text(template_version + "\n", encoding="utf-8")

    # Optional git init.
    if args.git_init:
        rc, err = git_init(target)
        if rc != 0:
            print(f"ERROR: git init failed: {err}", file=sys.stderr)
            return 1
        rc, err = git_add_all(target)
        if rc != 0:
            print(f"ERROR: git add failed: {err}", file=sys.stderr)
            return 1

    # Optional gh create.
    rc, err = gh_create(target, args.gh_create, args.repo_url)
    if rc != 0:
        print(f"ERROR: gh repo create failed: {err}", file=sys.stderr)
        return 1

    print(f"OK: bootstrapped {args.catalog_id} at {target} (template version {template_version})")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
