# Copyright (c) 2026 Pointmatic
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Throwaway spike script for Story K.a — exercises the full archive_stories
pipeline end-to-end against a fixture stories.md, before any productionized
mode template, metadata entry, or new action type lands.

Pipeline:
  1. Detect latest version from `vX.Y.Z` story headings
  2. Detect latest phase letter from `## Phase <Letter>:` headings
  3. Extract `## Future` section (everything from `## Future` to EOF)
  4. Move source → <dir>/.archive/<basename>-vX.Y.Z.md
  5. Re-render a fresh stories.md from the artifact template with `## Future`
     re-injected and an empty body

Usage:
  pyve run python scripts/spike_archive_stories.py docs/specs/stories-tmp.md

Verification (manual after running):
  - .archive/<basename>-vX.Y.Z.md byte-matches the original
  - new <basename>.md contains the artifact template body + carried `## Future`

This script is intentionally standalone — no imports from project_guide. It
will be deleted in Story K.d once the productionized mode supersedes it.
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ARTIFACT_TEMPLATE = (
    REPO_ROOT
    / "project_guide"
    / "templates"
    / "project-guide"
    / "templates"
    / "artifacts"
    / "stories.md"
)

# Matches `### Story X.y: vMAJOR.MINOR.PATCH ...`
VERSION_RE = re.compile(r"^###\s+Story\s+[A-Z]+\.[a-z]+:\s+v(\d+)\.(\d+)\.(\d+)", re.M)

# Matches `## Phase <Letter(s)>:`
PHASE_RE = re.compile(r"^##\s+Phase\s+([A-Z]+):", re.M)

# Matches `## Future` heading and grabs everything to EOF.
FUTURE_RE = re.compile(r"^##\s+Future\s*$.*", re.M | re.S)


def detect_latest_version(text: str) -> tuple[int, int, int]:
    versions = [
        (int(m.group(1)), int(m.group(2)), int(m.group(3)))
        for m in VERSION_RE.finditer(text)
    ]
    if not versions:
        raise ValueError("No versioned story headings found")
    return max(versions)


def detect_latest_phase_letter(text: str) -> str:
    """
    Returns the highest phase letter using base-26 ordering (no zero):
    A < B < ... < Z < AA < AB < ... < AZ < BA < ...
    """
    letters = [m.group(1) for m in PHASE_RE.finditer(text)]
    if not letters:
        raise ValueError("No phase headings found")
    # Sort by (length, lex) — longer letters always rank higher
    letters.sort(key=lambda s: (len(s), s))
    return letters[-1]


def extract_future_section(text: str) -> str:
    """
    Returns the `## Future` section verbatim (heading included), or empty
    string if no such section exists.
    """
    m = FUTURE_RE.search(text)
    return m.group(0) if m else ""


def render_fresh_stories(future_section: str) -> str:
    """
    Renders the stories.md artifact template with an empty `phases_and_stories`
    body and the carried `## Future` section appended (if any).

    Standalone Jinja substitution — no project_guide.render import.
    """
    template = ARTIFACT_TEMPLATE.read_text(encoding="utf-8")
    # Naive {{var}} substitution — we control all the variables here.
    rendered = (
        template.replace("{{project_name}}", "project-guide")
        .replace("{{programming_language}}", "Python")
        .replace("{{phases_and_stories}}", "")
    )
    # Trim trailing blank lines from the empty phases_and_stories slot,
    # then re-attach the future section with one blank-line separator.
    rendered = rendered.rstrip() + "\n"
    if future_section:
        rendered += "\n" + future_section.rstrip() + "\n"
    return rendered


def archive_stories(source: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(f"Source not found: {source}")

    text = source.read_text(encoding="utf-8")

    major, minor, patch = detect_latest_version(text)
    version = f"v{major}.{minor}.{patch}"
    phase_letter = detect_latest_phase_letter(text)
    future = extract_future_section(text)

    archive_dir = source.parent / ".archive"
    archive_dir.mkdir(exist_ok=True)
    archive_target = archive_dir / f"{source.stem}-{version}{source.suffix}"

    if archive_target.exists():
        raise FileExistsError(f"Archive target already exists: {archive_target}")

    print(f"  source:        {source}")
    print(f"  latest version: {version}")
    print(f"  latest phase:   {phase_letter}")
    print(f"  future bytes:   {len(future)}")
    print(f"  archive target: {archive_target}")

    shutil.move(str(source), str(archive_target))

    fresh = render_fresh_stories(future)
    source.write_text(fresh, encoding="utf-8")

    print(f"  fresh {source.name}: {len(fresh)} bytes")
    print("  done.")

    # Round-trip verification
    archived_text = archive_target.read_text(encoding="utf-8")
    assert archived_text == text, "archived file does not match original"
    fresh_text = source.read_text(encoding="utf-8")
    assert "## Future" in fresh_text or not future, "future section was lost"
    assert "{{phases_and_stories}}" not in fresh_text, "template placeholder leaked"
    print("  round-trip verified ✓")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        print("error: exactly one argument required (path to stories.md)", file=sys.stderr)
        return 2
    archive_stories(Path(argv[1]).resolve())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
