#!/usr/bin/env python3
"""Render templates/*.json.tmpl into policies/*.json.

Placeholders use ${VAR} syntax (string.Template), same as the old envsubst
workflow. Values are resolved from the process environment first, falling
back to a .env file at the repo root (KEY=VALUE, one per line).

Usage:
    python scripts/render_policies.py
    python scripts/render_policies.py --templates-dir templates --output-dir policies
"""
import argparse
import json
import os
import sys
from pathlib import Path
from string import Template

REPO_ROOT = Path(__file__).resolve().parent.parent


def load_dotenv(path: Path) -> dict:
    """Minimal .env parser: KEY=VALUE per line, '#' comments, blank lines skipped."""
    values = {}
    if not path.is_file():
        return values

    for lineno, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            print(f"warning: {path}:{lineno}: skipping line with no '=': {raw_line!r}", file=sys.stderr)
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip()
    return values


def render(templates_dir: Path, output_dir: Path, env: dict) -> list[Path]:
    template_files = sorted(templates_dir.glob("*.json.tmpl"))
    if not template_files:
        print(f"warning: no *.json.tmpl files found in {templates_dir}", file=sys.stderr)
        return []

    output_dir.mkdir(parents=True, exist_ok=True)
    written = []
    errors = []

    for tmpl_path in template_files:
        out_path = output_dir / tmpl_path.name[: -len(".tmpl")]
        try:
            rendered = Template(tmpl_path.read_text(encoding="utf-8")).substitute(env)
        except KeyError as exc:
            errors.append(f"{tmpl_path}: missing environment variable {exc}")
            continue

        try:
            json.loads(rendered)
        except json.JSONDecodeError as exc:
            errors.append(f"{tmpl_path}: rendered output is not valid JSON ({exc})")
            continue

        out_path.write_text(rendered, encoding="utf-8")
        written.append(out_path)
        print(f"rendered {tmpl_path.relative_to(REPO_ROOT)} -> {out_path.relative_to(REPO_ROOT)}")

    if errors:
        print("\nFailed to render:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        raise SystemExit(1)

    return written


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--templates-dir", type=Path, default=REPO_ROOT / "templates")
    parser.add_argument("--output-dir", type=Path, default=REPO_ROOT / "policies")
    parser.add_argument("--env-file", type=Path, default=REPO_ROOT / ".env")
    args = parser.parse_args()

    env = {**load_dotenv(args.env_file), **os.environ}
    written = render(args.templates_dir, args.output_dir, env)
    print(f"\n{len(written)} file(s) rendered to {args.output_dir.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
