import unittest
from importlib.resources import files

from omics_metadata_signature import load_latest_schemas, load_metadata_file_names
import yaml


class SchemasTests(unittest.TestCase):
    def test_loadLatestSchema_loads_latestSchemas(self) -> None:
        schemas = load_latest_schemas()

        latest_version = "1.2.0"

        self.assertEqual(set(schemas), {"processed_data", "raw_data", "samples", "file_tree", "metadata"})
        self.assertEqual(schemas["raw_data"]["schema_version"], latest_version)
        self.assertEqual(schemas["processed_data"]["schema_version"], latest_version)
        self.assertEqual(schemas["samples"]["schema_version"], latest_version)
        self.assertEqual(schemas["file_tree"]["schema_version"], latest_version)
        self.assertEqual(schemas["metadata"]["schema_version"], latest_version)

    def test_loads_canonical_metadata_file_names(self) -> None:
        self.assertEqual(
            load_metadata_file_names(),
            {
                "raw_data": "raw_data.yaml",
                "samples": "samples.yaml",
                "processed_data": "processed_data.yaml",
                "file_tree": "file_tree.yaml",
                "metadata": "metadata.yaml",
            },
        )

    def test_schema_releases_are_complete_versioned_snapshots(self) -> None:
        schemas_directory = files("omics_metadata_signature").joinpath("schemas")
        releases = sorted(
            directory
            for directory in schemas_directory.iterdir()
            if directory.is_dir() and directory.name.startswith("v")
        )
        expected_schema_files = {
            schema_file.name
            for schema_file in releases[0].iterdir()
            if schema_file.is_file() and schema_file.suffix == ".yaml"
        }

        for release in releases:
            schema_files = {
                schema_file.name
                for schema_file in release.iterdir()
                if schema_file.is_file() and schema_file.suffix == ".yaml"
            }

            for schema_file in release.iterdir():
                if schema_file.name not in schema_files:
                    continue
                schema = yaml.safe_load(schema_file.read_text(encoding="utf-8"))
                self.assertEqual(schema["schema_version"], release.name.removeprefix("v"))

    def test_latest_is_an_exact_copy_of_the_highest_schema_release(self) -> None:
        package_directory = files("omics_metadata_signature")
        schemas_directory = package_directory.joinpath("schemas")
        latest_release = max(
            (
                directory
                for directory in schemas_directory.iterdir()
                if directory.is_dir() and directory.name.startswith("v")
            ),
            key=lambda directory: directory.name,
        )
        latest_directory = package_directory.joinpath("latest")

        release_schemas = {
            schema_file.name: schema_file.read_text(encoding="utf-8")
            for schema_file in latest_release.iterdir()
            if schema_file.is_file() and schema_file.suffix == ".yaml"
        }
        latest_schemas = {
            schema_file.name: schema_file.read_text(encoding="utf-8")
            for schema_file in latest_directory.iterdir()
            if schema_file.is_file() and schema_file.suffix == ".yaml"
        }

        self.assertEqual(latest_schemas, release_schemas)


if __name__ == "__main__":
    unittest.main()
