# CropSuiteLite con insumos de Huaura

Proyecto de evaluación multicultivo con clima, suelo, DEM y máscara de Huaura.
La evaluación recibe una parcela GeoJSON dentro de Huaura y uno o varios
cultivos seleccionados. Produce resultados separados y una comparación.
Se verificó el flujo con maíz, papa y arroz; la referencia anterior de maíz se conserva.

## Catálogo y selección de cultivos

El catálogo completo se conserva en `CropSuiteLite/plant_params/available/`:
79 archivos `.inf`, que incluyen cultivos y variantes de parametrización.
Los 78 archivos retirados durante la limpieza se restauraron desde el respaldo
y se verificaron por SHA256. Se mantiene el archivo original de maíz.

`evaluate.py --list-crops` ofrece todo el catálogo para seleccionar uno o varios
cultivos por evaluación. Cada trabajo utiliza únicamente los archivos seleccionados,
copiados sin modificaciones a carpetas propias y referenciadas por `plant_param_dir`.
La selección no elimina ni reescribe archivos del catálogo compartido.

La selección por CLI y el motor científico Python están implementados. VIA ya
dispone de un backend modular con persistencia PostgreSQL/PostGIS, ejecución
agroclimática en background, integración aislada con CropSuiteLite y API de
consulta de estado, resultados y evidencia. La interfaz web continúa pendiente.
Los parámetros disponibles no implican que los 79 cultivos y variantes hayan
sido ejecutados o validados para Huaura.

## Evaluar varios cultivos en una parcela

Desde `CropSuiteLite`:

```powershell
.venv/Scripts/python.exe evaluate.py --list-crops
.venv/Scripts/python.exe evaluate.py --parcel mi_parcela.geojson --crops maize potato rice
```

Para probar con una parcela **sintética**, incluida en las pruebas:

```powershell
.venv/Scripts/python.exe evaluate.py --parcel tests/fixtures/huaura_parcel_example.geojson --crops maize potato rice
```

Cada solicitud crea `results/evaluations/evaluation_*/evaluation.json`, con
estados, resúmenes por cultivo, cobertura y ranking sobre la superficie válida
común. Los cultivos se calculan por turnos en procesos aislados; si uno falla,
continúan los demás. Se preservan insumos, parámetros y configuración de referencia.
La opción `--whole-huaura` permite un diagnóstico provincial explícito.
Véase [uso y alcance del flujo multicultivo](CropSuiteLite/docs/multicrop_evaluation.md).

La [versión 2 del documento de arquitectura](docs/Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx)
incorpora la selección multicultivo, los resultados por parcela y la arquitectura que actualmente guía su integración con el backend modular.

## Ejecutar la referencia anterior de maíz

Desde esta carpeta:

```powershell
cd CropSuiteLite
.venv/Scripts/python.exe run_cropsuitelite.py -config yaml_configurations/general_config_huaura.yaml
```

El YAML selecciona `config_access_esm1_5_ssp126_2021_2040.ini` mediante
`GENERAL.run_config`. Ese INI es la configuración operativa: conserva
`plant_params/huaura_maize/maize.inf` y apunta a la ejecución validada.
El motor reutiliza los archivos existentes; no recalcula al volver a ejecutar.
El resto de las opciones del YAML sirve como referencia para el flujo de
generación de configuraciones, que no se usa mientras `run_config` esté definido.

## Validar después de cambiar código

Desde `CropSuiteLite`:

```powershell
.venv/Scripts/python.exe -m unittest discover -s tests -v
.venv/Scripts/python.exe scripts/validate_huaura_environment.py
```

La segunda orden regenera los datos derivados y ejecuta el pipeline en una
carpeta nueva, preservando la salida operativa y los datos originales.

## Carpetas conservadas

| Ruta | Uso |
|---|---|
| `CropSuiteLite/src/` | Motor corregido de interpolación y aptitud. |
| `CropSuiteLite/datasets/`, `solutions/` | Preparación de datos y dependencias del lanzador. |
| `CropSuiteLite/tests/`, `scripts/` | Pruebas y validación completa. |
| `CropSuiteLite/plant_params/available/` | Catálogo completo de cultivos y variantes para seleccionar por evaluación. |
| `CropSuiteLite/plant_params/huaura_maize/` | Parámetros de la ejecución de referencia de maíz. |
| `data/huaura/processed_0041667/` | Insumos preparados que usa el INI. |
| `data/huaura/boundary/`, `masks/` | Límite provincial y máscaras. |
| `data/huaura/raw/`, `downloads/`, `scripts/` | Fuentes y herramientas de preparación; los scripts históricos conservan su contexto. |
| `CropSuiteLite/docs/` | Documentación del motor y las correcciones. |

La salida operativa está en:

```text
CropSuiteLite/results/huaura_environment_validation/run_mw_8gsjo/
  simulation_downscaled/Area_-10N-77E--11N-76E/
  simulation_novar/Area_-10N-77E--11N-76E/maize/
  config.ini
  report.json
```

Resultados validados: 231 celdas terrestres con clima y pendiente disponibles;
siete celdas sin resultado de cultivo por faltantes en suelos originales.
La resolución aproximada de 4,6 km no proporciona detalle dentro de una
parcela pequeña. Véase el [informe de corrección](CropSuiteLite/docs/huaura_environment_correction.md).

## Archivo y limpieza

Los antecedentes se guardan fuera del proyecto operativo, en
`../poc_via_cslite_archive/cleanup_20260910_012022/`:

- `before_cleanup/`: copias de los archivos actualizados durante la limpieza.
- `archived/`: código anterior, otros cultivos, utilidades y preparación antigua.
- `reports/`: reportes, configuraciones y logs de resultados retirados.
- `manifest.json`: inventario de las operaciones y su verificación.
- `crop_catalog_restoration.json`: registro de los 78 parámetros restaurados al catálogo activo después de la limpieza.

Las cachés temporales, documentación HTML generada, intermediarios de descarga
y resultados de ejecuciones superadas se eliminaron. Los archivos que se
archivaron pueden recuperarse desde la carpeta anterior. Los datos originales,
el entorno `.venv`, el historial `.git` y la ejecución validada se conservan.
