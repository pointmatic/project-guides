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

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, TemplateNotFound, Undefined

from project_guide.exceptions import RenderError
from project_guide.metadata import Metadata, ModeDefinition


def render_go_project_guide(
    template_dir: Path,
    mode: ModeDefinition,
    metadata: Metadata,
    output_path: Path,
) -> None:
    """
    Render go.md from the entry point template and mode template.

    Args:
        template_dir: Path to the project's template directory (e.g., docs/project-guide)
        mode: The active mode definition
        metadata: The parsed metadata (for context variables)
        output_path: Where to write the rendered output
    """
    # The Jinja2 loader searches the templates/ subdirectory where the
    # entry point and all mode/artifact templates live
    templates_subdir = template_dir / "templates"
    if not templates_subdir.exists():
        raise RenderError(f"Templates directory not found: {templates_subdir}")

    env = Environment(
        loader=FileSystemLoader([str(templates_subdir)], encoding="utf-8"),
        keep_trailing_newline=True,
        undefined=_LenientUndefined,
    )

    # Resolve the mode template path relative to templates/
    mode_template_rel = mode.mode_template
    # Strip leading path components to get the relative path within templates/
    # e.g., "project_guide/templates/project-guide/templates/modes/plan-concept-mode.md"
    # becomes "modes/plan-concept-mode.md"
    if "modes/" in mode_template_rel:
        mode_template_rel = "modes/" + mode_template_rel.split("modes/")[-1]

    # Read the optional project-essentials.md artifact. When present and
    # non-empty, _header-common.md renders its content as a top-level
    # "Project Essentials" section visible to every mode. When missing or
    # empty, the section is omitted entirely. The lookup is resolved against
    # the `spec_artifacts_path` common variable (typically `docs/specs`) and
    # is always optional — a project that chooses not to maintain this file
    # renders cleanly.
    project_essentials = _read_project_essentials(metadata.common.get("spec_artifacts_path"))

    # Build context variables for Jinja2
    context = {
        "mode_name": mode.name,
        "mode_info": mode.info,
        "mode_description": mode.description,
        "sequence_or_cycle": mode.sequence_or_cycle,
        "next_mode": mode.next_mode or "",
        "mode_template": mode_template_rel,
        "target_dir": str(template_dir),
        "project_essentials": project_essentials,
        **metadata.common,
    }

    try:
        template = env.get_template("llm_entry_point.md")
        rendered = template.render(**context)
    except TemplateNotFound as e:
        raise RenderError(f"Template not found: {e}")
    except Exception as e:
        raise RenderError(f"Failed to render go.md: {e}")

    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")


class _LenientUndefined(Undefined):
    """
    Custom undefined that renders undefined variables as their placeholder.

    This prevents Jinja2 from erroring on variables that are meant as
    LLM instruction placeholders (e.g., {{problem_statement}} in artifact
    templates that get included by mistake).
    """

    def __str__(self):
        return f"{{{{ {self._undefined_name} }}}}" if self._undefined_name else ""

    def __iter__(self):
        return iter([])

    def __bool__(self):
        return False


def _read_project_essentials(spec_artifacts_path: str | None) -> str:
    """Read the optional project-essentials.md artifact.

    Returns the file's content as a string, or an empty string if the file is
    missing, empty (whitespace-only), or if ``spec_artifacts_path`` is not set.
    An empty return value causes ``_header-common.md`` to omit the
    "Project Essentials" section entirely via a ``{% if %}`` guard.

    Resolution rules:
    - When ``spec_artifacts_path`` is ``None`` (e.g., unit tests with minimal
      metadata): return ``""``.
    - When the file does not exist: return ``""`` silently (not an error).
    - When the file exists but is whitespace-only: return ``""``. This lets
      a project keep the file around with just a comment block and still
      have the rendered section suppressed.
    - Otherwise: return the file's full UTF-8 content.
    """
    if not spec_artifacts_path:
        return ""
    path = Path(spec_artifacts_path) / "project-essentials.md"
    if not path.exists():
        return ""
    content = path.read_text(encoding="utf-8")
    if not content.strip():
        return ""
    return content
