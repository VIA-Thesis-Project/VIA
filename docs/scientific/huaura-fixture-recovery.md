# Huaura scientific fixture recovery audit

## Scope

This audit identifies the exact scientific inputs needed to recover the reviewed Huaura CropSuiteLite execution used by VIA, the repository evidence that explains how those inputs were prepared, the current local availability of the artifacts, and how the recovered artifacts fit the B6.1 production-runtime benchmark contract.

This is an audit only. No scientific data was downloaded, regenerated, resampled, gap-filled, copied, renamed, or otherwise changed. No CropSuiteLite scientific code, backend code, migrations, benchmark harness, Docker/Compose configuration, source hashes, or Graphify output was modified.

The authoritative execution path is the normal Huaura entrypoint tested by `CropSuiteLite/tests/test_huaura_entrypoint.py`, which uses `CropSuiteLite/yaml_configurations/general_config_huaura.yaml` and directly selects `CropSuiteLite/config_access_esm1_5_ssp126_2021_2040.ini`. The current reviewed path therefore bypasses configuration regeneration.

Paths such as `../data/huaura/...` in CropSuiteLite configuration resolve to the repository-root `data/huaura/...` tree.

## Executive status

The scientific fixture is recoverable from the current local workspace without downloading or regenerating scientific data.

- All 39 final environmental GeoTIFFs required by the reviewed INI are currently present under `data/huaura/processed_0041667/`.
- Those 39 GeoTIFFs are ignored by Git, which explains why a tracked-file inventory alone makes the checkout appear to lack the scientific fixture.
- The current SHA-256 values of all 39 final environmental GeoTIFFs match the historical Huaura validation report at `CropSuiteLite/results/huaura_environment_validation/run_mw_8gsjo/report.json` exactly.
- The 35 final soil TIFFs total 33,819 bytes. DEM, land/sea, temperature climatology, and precipitation climatology add 639,694 bytes. The exact current local size of the 39 final environmental GeoTIFFs is therefore **673,513 bytes**. This is the sum of current files on disk, not an estimate or archive size.
- `Temp_avg.tif` and `Prec_avg.tif` are 28 x 21, EPSG:4326, float32, 365-band GeoTIFFs at 1/24 degree resolution. DEM is 28 x 21, EPSG:4326, float32, single-band. Land/sea is 28 x 21, EPSG:4326, uint8, single-band.
- `CropSuiteLite/plant_params/huaura_maize/maize.inf` still matches the historical validation hash.
- The current tracked INI is clean in Git but its current SHA-256 (`0df36a488055479a21442895e1cfa20a7c6f725db57e2920b7190972dfd23d9d`) differs from the historical report value (`255240fbcd3b67eccf6502a495b31c13a44751cca2a119d32ae6826480397a15`). This audit did not modify the INI. Exact reproduction of the historical engine run should therefore treat the INI identity difference as an open traceability question even though the environmental rasters themselves are identical.
- B6.1 does not require a benchmark-harness change. The recovered files can be staged read-only under `/mnt/via/sources`, represented by real Dataset/DatasetVersion metadata, and bound with their legitimate SHA-256 values.
- Remote availability was not tested. Where repository code contains an upstream URL or API it is recorded below; otherwise the audit states `remote availability: not verified`.

## Required final scientific inputs

The reviewed INI directly requires 39 environmental GeoTIFFs: two climate files, one DEM, one land/sea raster, and 35 soil rasters. The reviewed engine run additionally fingerprints the selected INI and `maize.inf`; those two files are engine scientific sources but are not part of the 39 environmental GeoTIFF count.

| Logical input | Exact final path or pattern | Format / grid | Preparation state | VIA integrity binding | Current local status | Reproducible today | Current size |
|---|---|---|---|---|---|---|---:|
| Temperature climatology | `data/huaura/processed_0041667/climate/access-esm1-5_ssp126_2021_2040/Temp_avg.tif` | GeoTIFF, EPSG:4326, 28x21, 365 bands, float32, ~1/24 degree | Prepared final source | SHA-bound | Present, ignored; historical SHA matches | Yes from current local fixture; remote regeneration not verified | 305,372 B |
| Precipitation climatology | `data/huaura/processed_0041667/climate/access-esm1-5_ssp126_2021_2040/Prec_avg.tif` | GeoTIFF, EPSG:4326, 28x21, 365 bands, float32, ~1/24 degree | Prepared final source | SHA-bound | Present, ignored; historical SHA matches | Yes from current local fixture; remote regeneration not verified | 332,249 B |
| DEM | `data/huaura/processed_0041667/dem.tif` | GeoTIFF, EPSG:4326, 28x21, 1 band, float32, ~1/24 degree | Prepared final source | SHA-bound | Present, ignored; historical SHA matches | Yes from current local fixture; upstream acquisition path is ambiguous | 1,627 B |
| Land/sea | `data/huaura/processed_0041667/landsea.tif` | GeoTIFF, EPSG:4326, 28x21, 1 band, uint8, ~1/24 degree | Prepared final source | SHA-bound | Present, ignored; historical SHA matches | Yes from current local fixture; remote acquisition not verified | 446 B |
| Base saturation | `data/huaura/processed_0041667/soil_cropsuite/bsat/bsat_0-20cm.tif` | GeoTIFF, final `_0041667` reference grid | Prepared final source | SHA-bound | Present, ignored; historical SHA matches | Yes from current local fixture | 755 B |
| Coarse fragments | `data/huaura/processed_0041667/soil_cropsuite/cfvo/*.tif` | 6 GeoTIFFs, SoilGrids depth intervals | Prepared final source | SHA-bound | 6 present, ignored; all historical SHAs match | Yes from current local fixture; SoilGrids remote availability not verified | 6,118 B |
| Clay | `data/huaura/processed_0041667/soil_cropsuite/clay/*.tif` | 6 GeoTIFFs, SoilGrids depth intervals | Prepared final source | SHA-bound | 6 present, ignored; all historical SHAs match | Yes from current local fixture; SoilGrids remote availability not verified | 6,170 B |
| Gypsum | `data/huaura/processed_0041667/soil_cropsuite/gyps/gyps_0-20cm.tif` | GeoTIFF, final `_0041667` reference grid | Prepared final source | SHA-bound | Present, ignored; historical SHA matches | Yes from current local fixture; WISE acquisition not documented | 759 B |
| pH | `data/huaura/processed_0041667/soil_cropsuite/ph/*.tif` | 6 GeoTIFFs, SoilGrids depth intervals | Prepared final source | SHA-bound | 6 present, ignored; all historical SHAs match | Yes from current local fixture; SoilGrids remote availability not verified | 5,051 B |
| Salinity | `data/huaura/processed_0041667/soil_cropsuite/sal/sal_0-NA.tif` | GeoTIFF, final `_0041667` reference grid | Prepared final source | SHA-bound | Present, ignored; historical SHA matches | Yes from current local fixture; upstream URL is documented in code | 613 B |
| Sand | `data/huaura/processed_0041667/soil_cropsuite/sand/*.tif` | 6 GeoTIFFs, SoilGrids depth intervals | Prepared final source | SHA-bound | 6 present, ignored; all historical SHAs match | Yes from current local fixture; SoilGrids remote availability not verified | 6,364 B |
| Soil organic carbon | `data/huaura/processed_0041667/soil_cropsuite/soc/*.tif` | 6 GeoTIFFs, SoilGrids depth intervals | Prepared final source | SHA-bound | 6 present, ignored; all historical SHAs match | Yes from current local fixture; SoilGrids remote availability not verified | 6,253 B |
| Sodicity | `data/huaura/processed_0041667/soil_cropsuite/sod/sod_0-20cm.tif` | GeoTIFF, final `_0041667` reference grid | Prepared final source | SHA-bound | Present, ignored; historical SHA matches | Yes from current local fixture; WISE acquisition not documented | 762 B |
| Soil depth | `data/huaura/processed_0041667/soil_cropsuite/soildepth/depth_0-NA.tif` | GeoTIFF, final `_0041667` reference grid | Prepared final source | SHA-bound | Present, ignored; historical SHA matches | Yes from current local fixture; from-scratch upstream chain remains partly ambiguous | 974 B |

The exact reviewed INI directories are `bsat`, `cfvo`, `clay`, `gyps`, `ph`, `sal`, `sand`, `soc`, `sod`, and `soildepth`. The corresponding file count is 35 soil GeoTIFFs: 1 + 6 + 6 + 1 + 6 + 1 + 6 + 6 + 1 + 1.

The reviewed INI also points to `CropSuiteLite/plant_params/huaura_maize` and `data/usda_texture_classification.dat`. `maize.inf` was fingerprinted in the historical validation report. The texture classification data is configuration support rather than one of the recovered Huaura environmental rasters.

## Current identity manifest

The following current files match the hashes captured by the historical validation report. Hash comparison was performed read-only during this audit.

| File | SHA-256 |
|---|---|
| `processed_0041667/dem.tif` | `d00f300733e740d7cca0837986c7386b48e8e0d1ea4f5a96c4574b4040a4e8f1` |
| `processed_0041667/landsea.tif` | `0075b8be5a5693b2681681a91c33f75302bac016f0433b8e14b9f6cf8bf91cc7` |
| `processed_0041667/climate/access-esm1-5_ssp126_2021_2040/Prec_avg.tif` | `18dca73609d936f1b0158a749096da3a1bb53f36fa64747f546e21a530347a72` |
| `processed_0041667/climate/access-esm1-5_ssp126_2021_2040/Temp_avg.tif` | `1aee897ada573554668ab7cd7666b52cbdd0fbf485ba256236e7ea27e1f98de8` |
| `soil_cropsuite/bsat/bsat_0-20cm.tif` | `4bac43ecece669905573cfe22e97ddf19a5cdbb9e392502ffa0c50e14020854c` |
| `soil_cropsuite/cfvo/cfvo_0-5cm_mean.tif` | `7aeebb22a294593de633af81b0a81f312ca6a89702e9fe86a6c10b4c9f8b38ff` |
| `soil_cropsuite/cfvo/cfvo_5-15cm_mean.tif` | `6fac6ec9d1e48d071348060738fe063cefc903df6cf0c4770350218b41207be5` |
| `soil_cropsuite/cfvo/cfvo_15-30cm_mean.tif` | `27d7ca51dcaa3339328c97e78bea6c581a2fc00d611f3df0165bfa6cb8864883` |
| `soil_cropsuite/cfvo/cfvo_30-60cm_mean.tif` | `a16faf4e6c5c97080ee436bc29e46f099dd357fbf7dcf17a3db0de58775543ab` |
| `soil_cropsuite/cfvo/cfvo_60-100cm_mean.tif` | `235ca7ceb8ed51576339cbefc4d6561f1dba6a1fb587c0d614eec6a1ccaddba4` |
| `soil_cropsuite/cfvo/cfvo_100-200cm_mean.tif` | `1036ea27f8f336704f2acce8221cfedfff2158057268eeea0ac08bc68999ba39` |
| `soil_cropsuite/clay/clay_0-5cm_mean.tif` | `e83ab7b94fb619f50360b141696c2bd190aa94d27f0a1a9a63341ce693dcf335` |
| `soil_cropsuite/clay/clay_5-15cm_mean.tif` | `a14b69746825279f25001f1cb720159576f47bfda325de72d44f770b4753e6a6` |
| `soil_cropsuite/clay/clay_15-30cm_mean.tif` | `cc4f8e7276837f774bd2c8a180994102135dc0e40aeca18551143f4c9645d06a` |
| `soil_cropsuite/clay/clay_30-60cm_mean.tif` | `8193df7cd20c218ebf42b249c21f2f420dcf05a5e05e08835d864715610acc3f` |
| `soil_cropsuite/clay/clay_60-100cm_mean.tif` | `55cceb66898a20da2802cd3e9a227db92d6847286a7db3e992614a57c1560aa1` |
| `soil_cropsuite/clay/clay_100-200cm_mean.tif` | `f84c5671f72977ab4cc5adb48044a5fa6db237f9971cfbafdce4ffe532b241fc` |
| `soil_cropsuite/gyps/gyps_0-20cm.tif` | `70291323f5d76a12c05e1da7c5f8bd0624406e7170ffff9091adf0db7276410b` |
| `soil_cropsuite/ph/phh2o_0-5cm_mean.tif` | `101dc4ce8d11646a33fda24b6af8d0af5a49803b622e3fe35d18bcfe33fdfa91` |
| `soil_cropsuite/ph/phh2o_5-15cm_mean.tif` | `334d26fd58d22db848fb0d412fd5055fc3413083ab85bb095673335f56ed5a66` |
| `soil_cropsuite/ph/phh2o_15-30cm_mean.tif` | `336b38ccc82124e900035c90a27373c2df3f46ab22aa7ce29a0b22e4d025a288` |
| `soil_cropsuite/ph/phh2o_30-60cm_mean.tif` | `c54d508758aebb92e4f12e6a5ed1a8d6a735d5494d7c6c882dcf81eead349ee0` |
| `soil_cropsuite/ph/phh2o_60-100cm_mean.tif` | `4f9109c304ff7325e788c90759b27fa9c9229f18e6583551fc6e8522d8714d72` |
| `soil_cropsuite/ph/phh2o_100-200cm_mean.tif` | `0372bc1e1ea40865bb13ccae5aaf2824d872526d42988ace9a7687bebc3f0755` |
| `soil_cropsuite/sal/sal_0-NA.tif` | `22413cf86763f5405089b93dfb79f491e0fef6d592ef00df7722636e0ea71cc4` |
| `soil_cropsuite/sand/sand_0-5cm_mean.tif` | `e5ab750b616ac3f1570941ca4e21b551a9083d976eb3823235c61bed7e3b0350` |
| `soil_cropsuite/sand/sand_5-15cm_mean.tif` | `d05be43271e161cd7225239abff7840db0cf96ee4e0faacc9e1ff801cfb697e3` |
| `soil_cropsuite/sand/sand_15-30cm_mean.tif` | `b311acc3cbcb1d88c060e50c6013d6ced542342e68f2cf735f5bc2b528b1a30b` |
| `soil_cropsuite/sand/sand_30-60cm_mean.tif` | `e1f1add4e1ef550cae71cc7725de63950e66a4893284c9b7a3410960d306607f` |
| `soil_cropsuite/sand/sand_60-100cm_mean.tif` | `9b18f2e5686a26be3cb1b6f30aa18f92399a4312bc5c13adf6c682d829fcb8be` |
| `soil_cropsuite/sand/sand_100-200cm_mean.tif` | `b87042fcb62cff8c0cb7b087de659692f2e803fd4fad262f2d4a4bf02659b3ca` |
| `soil_cropsuite/soc/soc_0-5cm_mean.tif` | `9a849ab72a6f5e0f0c0a7e991a6a26cab24e5b760ae76f83e6839f148df847aa` |
| `soil_cropsuite/soc/soc_5-15cm_mean.tif` | `e3dcf926926f4ed9469653f1855c6716f320965c3335191675e94b003f45294a` |
| `soil_cropsuite/soc/soc_15-30cm_mean.tif` | `73ca62f7597597dcf82ab04a5859ff44cc7fc80fbcb4bd3aa69e13ab4b9ecdf7` |
| `soil_cropsuite/soc/soc_30-60cm_mean.tif` | `08cb3307df892f0efe6537c6e93c7d4134606447469c99351c9f794e3c33abbe` |
| `soil_cropsuite/soc/soc_60-100cm_mean.tif` | `a945629578e392f5cd7d7e80cd14d4d80397ab017b5b09f5309b3a1e25f0958d` |
| `soil_cropsuite/soc/soc_100-200cm_mean.tif` | `6d3988eaf4a8d580ed623340de3a1e7aae108615f12de4846c6bad13b869173e` |
| `soil_cropsuite/sod/sod_0-20cm.tif` | `7143f45f0362dce1015e407b4ea194907052a62091cb4d831107e609d959b330` |
| `soil_cropsuite/soildepth/depth_0-NA.tif` | `3099926bc3f231fcc17b529d82072f8454632a85c81b135c19b903e551b9083f` |

Historical engine-source identities recorded in the same report:

- `CropSuiteLite/plant_params/huaura_maize/maize.inf`: historical and current SHA-256 `f948b1192ea73587aaf442045a28f630088f464bff9f483fc1494bef89b675a7`.
- `CropSuiteLite/config_access_esm1_5_ssp126_2021_2040.ini`: historical SHA-256 `255240fbcd3b67eccf6502a495b31c13a44751cca2a119d32ae6826480397a15`; current SHA-256 `0df36a488055479a21442895e1cfa20a7c6f725db57e2920b7190972dfd23d9d`. The file is not dirty in the current Git working tree.

The B6.1 integrity verifier allows extra engine-reported source hashes beyond the hashes bound to environmental DatasetVersions. The current INI hash difference therefore does not by itself require a benchmark-harness change, but it matters if the goal is bit-identical reproduction of the earlier validated engine run.

## Preparation chains

### Boundary and reference mask

The tracked province boundary is `data/huaura/boundary/huaura_province.geojson`. `data/huaura/boundary/metadata.json` identifies it as Provincia de Huaura, Lima, Peru; CRS EPSG:4326; `MultiPolygon`; area 4,944.18 km2; source GADM 4.1.

`scripts/extract_huaura_boundary.py` reads `downloads/gadm/gadm41_PER_2.json`, filters `NAME_1 == Lima` and `NAME_2 == HUAURA`, converts to EPSG:4326, and writes the tracked GeoJSON. The GADM JSON is currently present locally but ignored through the `downloads/` rule.

The current `_0041667` preprocessing mask is `data/huaura/masks/huaura_mask_0041667.tif`, currently present locally and ignored by `*.tif`. `scripts/prepare_reference_grid_0041667.py` derives it from the province boundary, using the native 2.5 arc-minute CropSuite resolution (`1/24` degree), a fixed 28-column by 21-row EPSG:4326 grid, uint8 values 2 inside Huaura and 0 outside, and LZW compression. `crop_suite_datasets_huaura_0041667.yaml` references this exact mask.

The current `_0041667` mask does not require the DEM. Older `scripts/create_huaura_mask.py` and `scripts/create_huaura_mask_from_dem.py` write `data/huaura/boundary/huaura_boundary.tif` and belong to alternative/historical paths.

The mask is a preparation/reference-grid artifact; it is not a direct final input in the reviewed INI.

### Climate

`CropSuiteLite/yaml_configurations/download_cmip6_huaura.yaml` declares:

- source family: NEX-GDDP-CMIP6;
- GCM: `ACCESS-ESM1-5`;
- scenario: `ssp126`;
- variables: `pr`, `tasmin`, `tasmax`, `rsds`;
- requested year bounds `[2021, 2041]`, while the downloader uses a Python end-exclusive range, yielding 2021-2040 inclusive;
- bounding box `[-77.9, -11.6, -76.3, -10.4]`;
- raw output root `data/huaura/raw/nex-gddp-cmip6/`.

`CropSuiteLite/datasets/download_data.py` constructs paths below `https://nex-gddp-cmip6.s3-us-west-2.amazonaws.com/NEX-GDDP-CMIP6`, tries known NEX file-version suffixes, and stores raw files by variable/scenario/GCM. It converts precipitation from kg m-2 s-1 to mm/day, temperature from K to C, and shortwave radiation from W/m2 to MJ/m2/day before saving NetCDF.

The current local raw climate tree contains exactly **80 files / 7,671,189 bytes**, consistent with four variables x twenty years x one GCM x one scenario.

`CropSuiteLite/datasets/create_spatial_datasets.py` creates the climatological `Temp_avg.tif` and `Prec_avg.tif` source files used by the reviewed INI. The current files are 365-band daily climatologies on the 28x21 reference grid. `CropSuiteLite/docs/huaura_precipitation_units.md` records that `Prec_avg.tif` is interpreted as mm/day.

The `ds_temp_*.nc` and `ds_prec_*.nc` files described by validation documentation are runtime downscaling products/cache, not source-fixture inputs that need to be recovered for B6.1.

Remote availability: **not verified** during this audit.

### Soil

The reviewed final soil tree is `data/huaura/processed_0041667/soil_cropsuite/` and contains 35 GeoTIFFs. All 35 are currently present, ignored by Git, and hash-identical to the historical validation report.

The repository-supported preparation chain is:

1. Acquire/prepare raw component sources under `data/huaura/raw/`.
2. `scripts/assemble_soil_final.py` assembles the normalized source tree `data/huaura/raw/soil_final/`.
3. `scripts/prepare_soil_0041667.py` reprojects every source TIFF onto `huaura_mask_0041667.tif` using nearest-neighbor resampling, float32 output, NaN outside Huaura, and LZW compression, writing `data/huaura/processed_0041667/soil/` while preserving the relative property layout.
4. The final reviewed INI expects abbreviated CropSuite folder names below `processed_0041667/soil_cropsuite/` (`bsat`, `cfvo`, `clay`, `gyps`, `ph`, `sal`, `sand`, `soc`, `sod`, `soildepth`). No repository script was found that explicitly transforms `processed_0041667/soil/` into that final folder layout. The current local `soil_cropsuite/` tree exists and is complete, so the gap is a provenance/documentation gap for regeneration, not a missing current artifact.

Current local supporting trees further confirm that this is a recoverable local fixture:

- `data/huaura/raw/soilgrids/`: 42 files / 3,807,741 bytes.
- `data/huaura/raw/wise30sec_huaura/`: 3 files / 14,215 bytes.
- `data/huaura/raw/soil_final/`: 35 files / 3,026,049 bytes.
- `data/huaura/processed_0041667/soil/`: 35 files / 33,819 bytes.
- `data/huaura/processed_0041667/soil_cropsuite/`: 35 TIFFs / 33,819 bytes.

#### SoilGrids components

`scripts/download_soilgrids_huaura.py` uses `https://files.isric.org/soilgrids/latest/data` and defines `clay`, `sand`, `cfvo`, `phh2o`, `soc`, `bdod`, and `cec` at depths 0-5, 5-15, 15-30, 30-60, 60-100, and 100-200 cm. It crops the source VRTs to Huaura and reprojects to EPSG:4326 with bilinear resampling.

The current assembly uses SoilGrids `clay`, `sand`, `cfvo`, `phh2o`, and `soc`. Although the downloader can fetch `bdod` and `cec`, those two variables are not used by the current `assemble_soil_final.py` chain.

Remote availability: **not verified**.

#### WISE30sec components

`scripts/prepare_wise_huaura.py` expects these local inputs below `data/huaura/raw/wise30sec/source/WISE30sec/Interchangeable_format/`:

- `wise_30sec_v1.tif`;
- `wise_30sec_v1.tsv`;
- `HW30s_FULL.txt`.

They are currently present locally. The script builds D1/topsoil (`0-20cm`) base saturation, sodicity, and gypsum rasters using composition-weighted aggregation after excluding invalid special/negative values.

No repository acquisition URL or downloader was found for WISE30sec. Authentication requirements and remote retrievability are therefore **uncertain; remote availability: not verified**.

#### Salinity

`scripts/prepare_salinity_huaura.py` reads `https://files.isric.org/public/global_soil_salinity/salmap2016.vrt` and writes `data/huaura/raw/salinity/salinity_2016.tif`, which is currently present locally. The script maps ISRIC salinity classes to lower-bound ECe values in dS/m: 0 -> 0, 1 -> 2, 2 -> 4, 3 -> 8, 4 -> 16. `assemble_soil_final.py` places it as `salinity/sal_0-NA.tif`, and the reviewed INI requires the final `soil_cropsuite/sal` input.

Salinity is therefore required, not an optional/experimental source.

Remote availability: **not verified**.

#### Soil depth

`scripts/crop_bdticm_huaura.py` documents the legacy SoilGrids BDTICM source `https://files.isric.org/soilgrids/former/2017-03-10/data/BDTICM_M_250m_ll.tif` and produces `data/huaura/raw/soildepth/bdticm_huaura_cm.tif`, which is currently present.

`scripts/download_pelletier_nasa.py` uses the protected ORNL DAAC URL `https://data.ornldaac.earthdata.nasa.gov/protected/bundle/Global_Soil_Regolith_Sediment_1304.zip` and explicitly performs interactive `earthaccess.login(...)`, so NASA Earthdata authentication is required by repository evidence. That downloader extracts `average_soil_and_sedimentary-deposit_thickness.tif`.

`scripts/prepare_soildepth_huaura.py`, however, consumes `data/huaura/raw/pelletier/upland_hill-slope_soil_thickness.tif`. The local Pelletier directory currently contains all of the following:

- `Global_Soil_Regolith_Sediment_1304.zip` — 944,551,751 bytes;
- `average_soil_and_sedimentary-deposit_thickness.tif` — 73,091,828 bytes;
- `upland_hill-slope_soil_thickness.tif` — 217,656,520 bytes.

The immediate local fixture is therefore recoverable, but the repository does not explain how the `upland_hill-slope_soil_thickness.tif` prerequisite is obtained from the downloader as currently written. That remains a from-scratch recovery ambiguity.

The preparation script aligns Pelletier to the BDTICM grid with nearest resampling, converts Pelletier meters to centimeters, prioritizes valid Pelletier depths up to 2.0 m, falls back to BDTICM elsewhere, caps at 5,000 cm, and writes `data/huaura/raw/soildepth_final/soildepth_0-200cm.tif`.

### DEM

The final required DEM is `data/huaura/processed_0041667/dem.tif`. `scripts/prepare_dem_0041667.py` consumes `data/huaura/raw/dem.tif` and the `_0041667` mask, reprojects to the reference grid using bilinear resampling, writes float32, masks outside Huaura as NaN, and applies LZW compression.

The raw and final DEM files are currently present locally.

The repository contains multiple upstream producers that all target the same `data/huaura/raw/dem.tif` path:

- `scripts/download_dem_huaura.py`: SRTM1 through the Python `elevation` package;
- `scripts/download_srtm_huaura.py`: direct anonymous `elevation-tiles-prod/skadi` SRTM tiles, one arc-second, EPSG:4326, then merge/clip;
- `scripts/download_dem_srtm_huaura.py`: another Skadi attempt with suspicious northern tile naming for the Huaura latitude;
- `scripts/download_dem_huaura_py3dep.py`: py3dep 30 m path, with no evidence that it was selected for this Peru fixture;
- `scripts/download_dem_copernicus_huaura.py`: despite its filename, it calls OpenTopography `globaldem` with `demtype=SRTMGL1`, not Copernicus.

No downstream consumer or repository decision record identifies which producer created the current raw DEM. SRTM1/SRTMGL1 is the recurring source family, but exact upstream provenance remains **uncertain**. The current prepared DEM identity is not uncertain because its hash matches the historical validated fixture.

Slope is derived downstream from the DEM; the historical validation records 231 valid DEM land cells and 231 valid slope cells. No separate slope source raster needs recovery. No separate TWI input is referenced by the reviewed INI.

Remote availability: **not verified**.

### Land/sea

The final required file is `data/huaura/processed_0041667/landsea.tif`, currently present and hash-identical to the historical validated fixture.

Both current-looking preparation scripts consume `data/huaura/raw/landsea/ne_10m_land.geojson`, which is currently present locally:

- `scripts/prepare_landsea_huaura.py` rasterizes Natural Earth land geometry to land=1 / sea=0 on the reference grid with `all_touched=False`.
- `scripts/prepare_landsea_0041667_majority.py` computes per-cell land fraction in EPSG:32718 and marks a cell as land when the fraction is at least 0.50.

The majority-cell script appears to be the later correction path because the Huaura validation documentation records one coastal cell classified as sea and `scripts/check_coastal_landsea_cell.py` explicitly inspects that coastal cell against the Natural Earth geometry. This conclusion is evidence-based but no explicit decision record was found naming the majority script as authoritative.

No repository downloader or URL was found for `ne_10m_land.geojson`. Provider identity is supported by script comments/filename as Natural Earth; acquisition and authentication are **unclear; remote availability: not verified**.

Land/sea is derived from Natural Earth geometry, not from the DEM.

## Historical alternatives / abandoned paths

The following paths should not be treated as the current `_0041667` source chain unless new evidence says otherwise:

- `CropSuiteLite/yaml_configurations/crop_suite_datasets_huaura.yaml` uses the older `raw/soil_final_gapfilled/` path and predates the current `_0041667` preparation configuration.
- `scripts/fill_soil_nodata_raw.py` belongs to the older 0.05-degree/gap-filled path. The current `_0041667` soil preparation explicitly does not fill missing cells.
- `scripts/prepare_soilgrids_huaura.py` is zero bytes and is not an implementation path.
- `scripts/prepare_soilgrids_cropsuite.py` maps raw SoilGrids variables into older CropSuite-style semantic names and incorrectly treats `cec` as base saturation and `bdod` as soil depth relative to the current assembled chain; it is not evidence for the reviewed final `_0041667` layout.
- `scripts/create_huaura_mask.py` and `scripts/create_huaura_mask_from_dem.py` create `data/huaura/boundary/huaura_boundary.tif`, whereas current `_0041667` preparation references `data/huaura/masks/huaura_mask_0041667.tif`.
- The multiple DEM acquisition scripts are alternatives feeding the same raw path. Downstream provenance does not select one.
- Runtime `ds_temp_*.nc` / `ds_prec_*.nc` products regenerated during historical validation are outputs/cache, not required source-fixture inputs.

## Missing artifacts

### Missing from the current local workspace

None of the 39 final environmental GeoTIFFs required by the reviewed INI is missing from the current local workspace.

The current local workspace also contains the reference mask, raw DEM, Natural Earth land GeoJSON, 80 raw NEX climate files, SoilGrids cache, WISE source files, salinity raster, BDTICM crop, and the Pelletier files needed by the existing soil-depth preparation script.

### Missing from tracked repository state / portability

The final scientific rasters and most raw scientific sources are intentionally or effectively outside tracked Git state:

- `.gitignore` ignores `*.tif`;
- `downloads/` is ignored;
- `CropSuiteLite/results/` is ignored.

Consequently, a fresh clone cannot be assumed to contain the locally verified scientific fixture even though this workspace does. The recovery problem for B6.1 is therefore primarily **portable staging and provenance**, not reconstruction of currently absent local files.

### Missing provenance or regeneration evidence

The following gaps remain even though the required local artifacts exist:

- explicit script/decision for the final rename/layout step from `processed_0041667/soil/` to `processed_0041667/soil_cropsuite/`;
- explicit WISE30sec acquisition URL/auth flow;
- explicit Natural Earth `ne_10m_land.geojson` acquisition path;
- authoritative selection among competing raw DEM acquisition scripts;
- explanation of how `upland_hill-slope_soil_thickness.tif` is obtained, since the current NASA downloader extracts a different Pelletier filename;
- explanation for the historical/current INI SHA-256 difference.

## Recovery order

For B6.1, the safest deterministic recovery path is to preserve the already validated local final artifacts rather than regenerate them:

1. Treat the 39 current final environmental GeoTIFFs listed above as the source fixture because their SHA-256 values match the historical validated run.
2. Copy/stage those files outside the repository into the B6.1 source directory that is mounted read-only as `/mnt/via/sources`. This copy/staging action is intentionally outside this audit.
3. Preserve the relative grouping needed by the benchmark fixture and Dataset/DatasetVersion metadata; do not alter raster content while staging.
4. Populate each benchmark environmental input with real Dataset/DatasetVersion metadata and the legitimate SHA-256 array for the concrete files represented by that version.
5. Verify the staged copy hashes against the identity manifest in this document before running B6.1.
6. Run the production benchmark only after staging and metadata creation. The benchmark itself is outside this audit.

If the current ignored local fixture is ever lost, then use a from-scratch recovery sequence:

1. Recreate/verify the Huaura province boundary from the GADM source.
2. Rebuild `huaura_mask_0041667.tif` from the boundary on the fixed 28x21, 1/24-degree grid.
3. Restore raw NEX-GDDP-CMIP6, SoilGrids, WISE30sec, salinity, BDTICM, Pelletier, Natural Earth land geometry, and a provenance-approved raw DEM.
4. Assemble soil source layers with `assemble_soil_final.py`.
5. Prepare soil and DEM onto the `_0041667` reference grid; prepare land/sea using the validated coastal-cell rule; build the two climate climatology GeoTIFFs.
6. Resolve and document the final `soil` -> `soil_cropsuite` normalization step rather than recreating it by assumption.
7. Compare every resulting final file against the historical SHA-256 manifest. A hash mismatch means the result is a different scientific fixture and must not silently replace the validated one.

The from-scratch path is currently **uncertain** because of the documented WISE, Natural Earth, DEM-provenance, Pelletier-filename, final soil-layout, and INI-identity gaps. Remote availability was not checked.

## Benchmark compatibility

The existing B6.1 harness is compatible with the recovered fixture.

`scripts/benchmark_production_runtime.sh` requires each `fixture.environmental_inputs[]` item to contain exactly `input_key`, `dataset`, `version`, and `source_sha256`. It requires:

- `version.storage_reference` to equal `/mnt/via/sources` or be beneath `/mnt/via/sources/`;
- `source_sha256` to be a non-empty array of unique valid lowercase SHA-256 values;
- real B6.1 values rather than the startup-only smoke binding/hash;
- the source directory to be mounted read-only into the benchmark worker.

The script creates `/etc/via/input-bindings.json` from the Dataset/DatasetVersion records created for the fixture. `docs/architecture/cropsuite-integration.md` defines `storage_reference` and DatasetVersion `checksum` as opaque environmental metadata at the application boundary, while deployment bindings map the exact DatasetVersion identity to one or more expected concrete CropSuite source hashes.

The runtime integrity verifier requires every expected hash configured for an environmental DatasetVersion to appear in the engine-reported `source_sha256` map. Extra CropSuite source hashes are allowed, including configuration/plant-parameter fingerprints that are not themselves represented as environmental DatasetVersions.

Therefore:

- the 39 verified GeoTIFF hashes can be used as legitimate B6.1 integrity bindings;
- the fixture can be staged below `/mnt/via/sources` without changing the benchmark harness;
- no mock/stub/startup-only hash is required;
- no source hash needs to be modified;
- the INI historical/current hash difference should be tracked separately as scientific-run provenance, while the environmental-input integrity gate can continue to bind the exact recovered environmental files.

**Harness change required: no.**

## Open uncertainties

1. **Current INI versus historical INI identity.** The file is clean in Git, but its current SHA-256 differs from the validation report. Exact historical-run reproducibility needs that difference explained or the historical INI bytes recovered from an authoritative source.
2. **Final soil layout normalization.** The repository has a clear chain through `processed_0041667/soil/`, but no explicit script was found that produces the abbreviated `processed_0041667/soil_cropsuite/` folder layout consumed by the reviewed INI.
3. **WISE acquisition.** Required WISE source files are local, but repository acquisition/authentication evidence is absent.
4. **Natural Earth acquisition.** `ne_10m_land.geojson` is local and clearly consumed, but its acquisition path is not documented in repository code.
5. **DEM upstream provenance.** Several acquisition scripts feed the same raw DEM path. The current final DEM is validated by hash, but the selected upstream producer is not proven.
6. **Pelletier filename gap.** The downloader extracts `average_soil_and_sedimentary-deposit_thickness.tif`; the soil-depth preparation consumes `upland_hill-slope_soil_thickness.tif`. Both are local today, but the repository does not connect those steps.
7. **Remote availability.** No upstream endpoint was contacted during this audit. All remote availability remains unverified.

## Recommended next action

Create a separate, portable B6.1 source-fixture staging directory from the **already present and hash-verified 39 final environmental GeoTIFFs**, preserve their bytes exactly, compute/confirm the staged hashes, and populate the benchmark Dataset/DatasetVersion fixture metadata so its `storage_reference` values resolve below `/mnt/via/sources`.

Do not regenerate the current scientific fixture unless the local verified copy is unavailable. If regeneration becomes necessary, first close the provenance gaps above so that a new result can be compared against the historical identity manifest rather than accepted by path/name alone.

## Repository evidence inspected

The audit inspected or queried the following repository evidence. Search-only inspection means only relevant excerpts/symbols were read rather than the entire file.

- `CropSuiteLite/tests/test_huaura_entrypoint.py`
- `CropSuiteLite/scripts/run_evaluation_engine.py`
- `CropSuiteLite/yaml_configurations/general_config_huaura.yaml`
- `CropSuiteLite/yaml_configurations/download_cmip6_huaura.yaml`
- `CropSuiteLite/yaml_configurations/crop_suite_datasets_huaura.yaml`
- `CropSuiteLite/yaml_configurations/crop_suite_datasets_huaura_0041667.yaml`
- `CropSuiteLite/config_access_esm1_5_ssp126_2021_2040.ini`
- `CropSuiteLite/datasets/download_data.py`
- `CropSuiteLite/datasets/create_spatial_datasets.py`
- `CropSuiteLite/src/downscaling.py` (search excerpts)
- `CropSuiteLite/docs/huaura_precipitation_units.md` (search excerpts)
- `CropSuiteLite/docs/huaura_precipitation_downscaling.md`
- `CropSuiteLite/docs/huaura_environment_correction.md`
- `CropSuiteLite/scripts/validate_huaura_environment.py` (search excerpts)
- `CropSuiteLite/results/huaura_environment_validation/run_mw_8gsjo/report.json`
- `CropSuiteLite/plant_params/huaura_maize/maize.inf` (identity check)
- `CropSuiteLite/run_cropsuitelite.py` (soil directory mapping excerpt)
- `CropSuiteLite/solutions/utils.py` (search result)
- `data/huaura/README.md`
- `data/huaura/huaura_config.yaml`
- `data/huaura/boundary/metadata.json`
- `data/huaura/boundary/huaura_province.geojson`
- `downloads/gadm/gadm41_PER_2.json` (presence/tracking check)
- `scripts/extract_huaura_boundary.py`
- `scripts/validate_huaura_boundary.py`
- `scripts/prepare_reference_grid_0041667.py`
- `scripts/create_huaura_mask.py`
- `scripts/create_huaura_mask_from_dem.py`
- `scripts/download_soilgrids_huaura.py`
- `scripts/test_soilgrids_download.py`
- `scripts/prepare_soilgrids_cropsuite.py`
- `scripts/prepare_soilgrids_huaura.py` (confirmed zero-byte)
- `scripts/prepare_wise_huaura.py`
- `scripts/check_wise_d1_weighting.py` (search excerpts)
- `scripts/prepare_salinity_huaura.py`
- `scripts/crop_bdticm_huaura.py`
- `scripts/download_pelletier_nasa.py`
- `scripts/compare_soildepth_sources.py` (search excerpts)
- `scripts/prepare_soildepth_huaura.py`
- `scripts/assemble_soil_final.py`
- `scripts/fill_soil_nodata_raw.py` (search excerpts)
- `scripts/prepare_soil_0041667.py`
- `scripts/check_missing_0041667.py` (search excerpts)
- `scripts/check_coastal_landsea_cell.py` (search excerpts)
- `scripts/check_missing_cells_geometry.py` (search excerpts)
- `scripts/prepare_landsea_huaura.py`
- `scripts/prepare_landsea_0041667_majority.py`
- `scripts/prepare_dem_0041667.py`
- `scripts/download_dem_huaura.py`
- `scripts/download_dem_srtm_huaura.py`
- `scripts/download_srtm_huaura.py`
- `scripts/download_dem_huaura_py3dep.py` (search excerpts)
- `scripts/download_dem_copernicus_huaura.py`
- `scripts/benchmark_production_runtime.sh`
- `backend/tests/test_resource_benchmark_contract.py`
- `backend/tests/test_scientific_input_integrity.py`
- `backend/src/via_backend/contexts/agroclimatic_evaluation/domain/environmental_inputs.py` (search excerpts)
- `docs/architecture/deployment-runtime.md` (search excerpts)
- `docs/architecture/cropsuite-integration.md`
- `docs/adr/ADR-006-scientific-traceability.md` (search excerpts)

Read-only filesystem checks also inspected the presence, count, file size, raster metadata, ignore/tracking state, and SHA-256 identities of the current local Huaura source/prepared trees relevant to this audit.
