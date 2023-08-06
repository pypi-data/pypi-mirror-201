from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import databind.json
import yaml

DEFAULT_CONFIG_FILE = Path("~/.config/terracomp/config.yaml")


@dataclass
class TerracompConfig:
    """
    Schema for the Terracomp configuration file.
    """

    #: The alias of the default configuration profile to use.
    current_profile: str | None = None

    #: Aliases for configuration profiles.
    profiles: dict[str, TerracompProfile] = field(default_factory=dict)


@dataclass
class TerracompProfile:
    """
    Represents a profile for a Terracomp server.
    """

    url: str
    token: str


def load_config(filename: Path = DEFAULT_CONFIG_FILE) -> TerracompConfig:
    raw_data = yaml.safe_load(filename.read_text())
    return databind.json.load(raw_data, TerracompConfig)


def save_config(config: TerracompConfig, filename: Path = DEFAULT_CONFIG_FILE) -> None:
    raw_data = databind.json.dump(config, TerracompProfile)
    filename.write_text(yaml.safe_dump(raw_data))
