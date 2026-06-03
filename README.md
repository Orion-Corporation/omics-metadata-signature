# Omics Metadata Schema

This repository is the centralized, application-agnostic storage location for
omics metadata schemas used by Orion projects.

The schemas are written in YAML so they can be consumed by different
applications and languages.

## Repository Structure

```text
conventions/
  file_naming_conventions.yaml
schemas/
  v1.0.0/
    raw-data_schema.yaml
    processed-data_schema.yaml
    samples_schema.yaml
latest/
  raw-data_schema.yaml
  processed-data_schema.yaml
  samples_schema.yaml
```

`schemas/` contains immutable versioned schema definitions. `latest/` contains
copies of the most recent schema files for consumers that do not need to pin a
specific version.

`conventions/file_naming_conventions.yaml` defines the canonical file names for
metadata files generated from these schemas:

- `raw-data.yaml`
- `samples.yaml`
- `processed-data.yaml`

## Schema Format

Each schema file contains a `schema_version` and a list of `fields`.

```yaml
schema_version: 1.0.0

fields:
  - name: assay_type
    type: string
    allowed_values:
      - RNA_SEQ
      - WGS
```

Field entries use these keys:

- `name`: stable field identifier.
- `type`: normalized field type. Allowed values are `string` and `integer`.
- `allowed_values`: optional list of accepted values for controlled fields.
- `multi`: optional flag. If present and set to `true`, the field may contain
  multiple values. If absent, consumers should treat the field as single-valued.

## Source Mapping

Version `1.0.0` was derived from `metadata_schema.py`.

The conversion follows these rules:

- `id` maps to `name`.
- Source UI types are normalized to general schema types: `text`, `textarea`,
  `folder_browser`, `dropdown`, and `email` become `string`; `number` becomes
  `integer`.
- `options` maps to `allowed_values`, using each option's `value`.
- Existing `allowed_values` are copied directly.
- `required`, `section`, labels, and other UI-only descriptors are omitted.
- `multi` is included only when the source field has `multi: true`.

The source file does not define a separate raw-data schema object. For
`v1.0.0`, `METADATA_SCHEMA_DATASET` is represented as
`raw-data_schema.yaml`.
