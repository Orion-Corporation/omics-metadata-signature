"""Access the versioned Omics metadata schemas bundled with this package."""

from collections.abc import Mapping
from importlib.resources import files
from typing import Any

import yaml

__version__ = "1.2.0"


def schema_path(version: str, filename: str):
    """Return a traversable path to a versioned schema resource."""
    return files("omics_metadata_signature").joinpath(
        "schemas", version, filename
    )


def load_latest_schemas() -> dict[str, dict[str, Any]]:
    """Load every schema bundled in the package's ``latest`` directory.

    The returned mapping uses stable, Python-friendly schema names. For
    example, ``raw-data_schema.yaml`` is available as ``"raw_data"``. The
    values are the parsed YAML schema documents.
    """
    latest_directory = files("omics_metadata_signature").joinpath("latest")
    schemas: dict[str, dict[str, Any]] = {}

    for schema_file in sorted(latest_directory.iterdir(), key=lambda path: path.name):
        if not schema_file.is_file() or schema_file.suffix not in {".yaml", ".yml"}:
            continue

        schema_name = schema_file.name.removesuffix("_schema.yaml").removesuffix(
            "_schema.yml"
        ).replace("-", "_")
        schema = yaml.safe_load(schema_file.read_text(encoding="utf-8"))

        if not isinstance(schema, Mapping):
            raise ValueError(f"Latest schema {schema_file.name!r} must be a YAML mapping.")

        schemas[schema_name] = dict(schema)

    return schemas


def load_metadata_file_names() -> dict[str, str]:
    """Load the canonical metadata file names bundled with the package.

    Returns a mapping such as ``{"raw_data": "raw_data.yaml"}`` from
    ``conventions/file_naming_conventions.yaml``.
    """
    conventions_file = files("omics_metadata_signature").joinpath(
        "conventions", "file_naming_conventions.yaml"
    )
    conventions = yaml.safe_load(conventions_file.read_text(encoding="utf-8"))

    if not isinstance(conventions, Mapping):
        raise ValueError("File-naming conventions must be a YAML mapping.")

    metadata_file_names = conventions.get("metadata_file_names")
    if not isinstance(metadata_file_names, Mapping) or not all(
        isinstance(name, str) and isinstance(filename, str)
        for name, filename in metadata_file_names.items()
    ):
        raise ValueError(
            "File-naming conventions must define metadata_file_names as a string mapping."
        )

    return dict(metadata_file_names)
