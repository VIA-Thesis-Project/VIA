# Environmental Information metadata slice

## Responsibility and semantics

This slice catalogs geoenvironmental metadata. Dataset is the stable logical
identity for one source/variable/unit combination. DatasetVersion is an
immutable registered release whose exact metadata can later participate in a
reproducible environmental input manifest.

Environmental Information owns both types and their persistence. It does not
read Farm Management entities or tables, decide suitability, create
recommendations, invoke CropSuiteLite, or depend on evaluation internals.

## Use cases and HTTP resources

Application owns the create/list/get commands and queries. REST is a transport
adapter and returns DTOs rather than ORM records.

| Method | Resource | Purpose |
|---|---|---|
| POST | /datasets | Register a logical dataset. |
| GET | /datasets | List datasets. |
| GET | /datasets/{dataset_id} | Retrieve a dataset. |
| POST | /datasets/{dataset_id}/versions | Register an immutable version. |
| GET | /datasets/{dataset_id}/versions | List versions for a dataset. |
| GET | /datasets/{dataset_id}/versions/{version_id} | Retrieve one version. |

Missing resources map to 404, invalid interface/domain data to 422, and a
duplicate version identifier within the same dataset to 409.

## Metadata and validation

Dataset metadata includes UUID, name, source/provider description,
environmental variable, variable unit, and creation time. Version metadata
includes UUID, version identifier, EPSG CRS, two-axis resolution and its unit,
rectangular extent, optional validity bounds and scenario, checksum, opaque
storage reference, and registration time.

Required text is non-empty and trimmed. Resolution is finite and positive.
Extent coordinates are finite and ordered; EPSG:4326 additionally uses valid
longitude/latitude bounds. If both validity dates exist, the start is not after
the end. Other CRS definitions are deliberately deferred.

## Persistence

The context owns schema environmental_information, with datasets and
dataset_versions. A version identifier is unique per dataset. The extent is a
PostGIS POLYGON in the dataset version's native EPSG CRS and has a GiST index;
it is a bounding rectangle only, not the valid-data mask. See
[ADR-012](../adr/ADR-012-postgresql-postgis-environmental-information-persistence.md).

The checksum identifies versioned content but its algorithm policy is not yet
fixed. The storage reference is an opaque catalog value so Domain has no
filesystem dependency and a future storage adapter can translate it to local or
object storage.

## Deliberately out of scope

Coverage calculations, parcel intersection, exact validity masks, raster/NetCDF
loading, file-format inspection, suitability, recommendations, evaluation
orchestration, workers, authorization, and frontend changes are not part of this
slice.

The future public collaboration should expose compatible version descriptions
to Agroclimatic Evaluation through a consumer-owned port and adapter. Its
coverage and compatibility rules still require explicit modeling; this CRUD
catalog does not imply those decisions.
