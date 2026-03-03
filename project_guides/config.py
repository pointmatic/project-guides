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

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Dict

import yaml


@dataclass
class GuideOverride:
    """Represents an overridden guide."""
    reason: str
    locked_version: str
    last_updated: date

    def to_dict(self) -> dict:
        """Convert to dictionary for YAML serialization."""
        return {
            "reason": self.reason,
            "locked_version": self.locked_version,
            "last_updated": self.last_updated.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "GuideOverride":
        """Create from dictionary loaded from YAML."""
        return cls(
            reason=data["reason"],
            locked_version=data["locked_version"],
            last_updated=date.fromisoformat(data["last_updated"]),
        )


@dataclass
class Config:
    """Project configuration for project-guides."""
    version: str = "1.0"
    installed_version: str = ""
    target_dir: str = "docs/guides"
    overrides: Dict[str, GuideOverride] = field(default_factory=dict)

    @classmethod
    def load(cls, path: str = ".project-guides.yml") -> "Config":
        """Load configuration from YAML file."""
        config_path = Path(path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")
        
        try:
            with open(config_path, "r") as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Failed to parse YAML: {e}")
        
        if data is None:
            data = {}
        
        overrides = {}
        if "overrides" in data and data["overrides"]:
            for guide_name, override_data in data["overrides"].items():
                overrides[guide_name] = GuideOverride.from_dict(override_data)
        
        return cls(
            version=data.get("version", "1.0"),
            installed_version=data.get("installed_version", ""),
            target_dir=data.get("target_dir", "docs/guides"),
            overrides=overrides,
        )

    def save(self, path: str = ".project-guides.yml") -> None:
        """Save configuration to YAML file."""
        data = {
            "version": self.version,
            "installed_version": self.installed_version,
            "target_dir": self.target_dir,
        }
        
        if self.overrides:
            data["overrides"] = {
                guide_name: override.to_dict()
                for guide_name, override in self.overrides.items()
            }
        
        config_path = Path(path)
        with open(config_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    def is_overridden(self, guide_name: str) -> bool:
        """Check if a guide is overridden."""
        return guide_name in self.overrides

    def add_override(self, guide_name: str, reason: str, version: str) -> None:
        """Add or update an override."""
        self.overrides[guide_name] = GuideOverride(
            reason=reason,
            locked_version=version,
            last_updated=date.today(),
        )

    def remove_override(self, guide_name: str) -> None:
        """Remove an override."""
        self.overrides.pop(guide_name, None)
