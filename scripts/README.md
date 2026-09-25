# Scripts de VIA

Este directorio contiene utilidades de desarrollo, preparación científica, validación, smoke testing y operación.

Los scripts permanecen en una sola carpeta porque varios son referenciados directamente por CI/CD y procedimientos operativos. Este README sirve como índice funcional sin introducir movimientos de archivos innecesarios.

## Operación y despliegue

### `staging_preflight.ps1`

Preflight local seguro para la validación híbrida de staging. Informa presencia
de CLIs, variables de autenticación y disponibilidad del engine de Docker sin
imprimir valores secretos. El procedimiento completo está en
`docs/operations/staging-validation.md`.

### `deploy_digitalocean.sh` / `deploy_digitalocean.ps1`

Herramientas relacionadas con el despliegue de VIA en DigitalOcean.

No ejecutes un despliegue sin revisar previamente la imagen, configuración runtime, migraciones y procedimiento de rollback.

### `backup_postgres.sh`

Backup de PostgreSQL previo a operaciones de release o mantenimiento.

### `sync_digitalocean_sources.ps1`

Sincronización controlada de fuentes/configuración científica requeridas por el entorno DigitalOcean.

## Verificación de producción

### `verify_production_compose.sh`

Valida invariantes de la topología Compose utilizada en producción.

También es utilizado por GitHub Actions, por lo que cambios de nombre o ubicación requieren actualizar CI.

### `smoke_production_api.py`

Smoke test de la API desplegada.

Puede crear recursos persistentes dependiendo del flujo ejecutado. Para comprobaciones puntuales de una release existente, prefiere verificaciones read-only cuando sean suficientes.

### `smoke_frontend_api.ps1` / `smoke_frontend_api.sh`

Pruebas orientadas al contrato que consume el frontend.

## Benchmark

### `benchmark_production_runtime.sh`

Ejecuta el benchmark representativo del runtime científico.

La automatización de GitHub puede utilizarlo con fixtures y fuentes científicas legítimas montadas de solo lectura.

## Preparación científica

Ejemplos:

```text
assemble_soil_final.py
prepare_wise_huaura.py
create_huaura_mask.py
create_huaura_mask_from_dem.py
crop_bdticm_huaura.py
```

Estos scripts preparan o transforman insumos científicos. No deben confundirse con el runtime normal de la API.

Los datos generados o descargados de gran tamaño normalmente permanecen fuera de Git.

## Descarga de datos

El repositorio contiene utilidades históricas o reproducibles para obtener fuentes como DEM, SoilGrids y otros insumos.

Ejemplos:

```text
download_dem_copernicus_huaura.py
download_dem_huaura.py
download_dem_huaura_py3dep.py
download_dem_srtm_huaura.py
test_soilgrids_download.py
```

Antes de ejecutarlos verifica:

- fuente;
- licencia;
- extensión geográfica;
- resolución;
- unidad;
- destino local;
- espacio en disco.

## Diagnóstico y validación científica

Existen scripts `check_*`, `diagnose_*` y `validate_*` para investigar cobertura, nodata, geometrías, fuentes y consistencia del dataset.

Ejemplos:

```text
check_coastal_landsea_cell.py
check_missing_cells_geometry.py
check_raw_missing_cells.py
diagnose_raw_nodata_components.py
validate_huaura_boundary.py
```

Estos scripts son herramientas de investigación/validación y no deben ejecutarse automáticamente en producción salvo que el procedimiento lo indique.

## Reglas al modificar scripts

1. Comprueba si el path aparece en `.github/workflows/`, Docker/Compose o `docs/operations/`.
2. Evita renombrar scripts operativos solo por estética.
3. No hardcodees secretos, credenciales ni rutas personales.
4. Usa rutas configurables o relativas al repositorio cuando sea posible.
5. Si el script modifica datos científicos, documenta entradas, salidas y reproducibilidad.
6. Si forma parte de CI, valida el workflow afectado antes de integrar el cambio.
