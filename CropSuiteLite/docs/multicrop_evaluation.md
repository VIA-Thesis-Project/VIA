# Evaluación de varios cultivos para una parcela de Huaura

Una solicitud contiene una parcela y los identificadores de los cultivos elegidos.
El catálogo conserva los 79 archivos `.inf` de cultivos y variantes. El flujo copia
únicamente los seleccionados, sin cambiar parámetros ni datos ambientales.

## Uso

Desde `CropSuiteLite`, con su entorno existente:

```powershell
.venv/Scripts/python.exe evaluate.py --list-crops
.venv/Scripts/python.exe evaluate.py --parcel mi_parcela.geojson --crops maize potato rice
.venv/Scripts/python.exe evaluate.py --parcel tests/fixtures/huaura_parcel_example.geojson --crops maize potato rice --max-workers 2
```

El tercer comando usa un polígono sintético para pruebas, no una propiedad
registrada. Los identificadores son los del catálogo, por ejemplo `maize`,
`potato` y `rice`. Se rechazan listas vacías, duplicados e identificadores desconocidos.

Se acepta Polygon o MultiPolygon WGS84 (longitud, latitud), como geometría,
Feature o FeatureCollection con exactamente una parcela. La geometría debe ser
válida y estar completamente dentro del límite de Huaura. El límite del archivo
es 5 MB. Estar dentro de la provincia no garantiza cobertura ambiental completa.

`--whole-huaura` reemplaza a `--parcel` solamente para un diagnóstico provincial
explícito. El comando anterior `run_cropsuitelite.py` conserva la referencia de maíz.
`--output` permite elegir la carpeta padre de nuevos trabajos; no reutiliza una
ejecución existente. `--config` es una opción local de administración, no una ruta
que deba recibir el futuro servidor desde un usuario público.

## Ejecución y archivos

`src.multicrop.run_evaluation(crops, parcel_path, ...)` ofrece la misma capacidad
como servicio Python para el futuro adaptador del worker. Es una llamada bloqueante;
no debe ejecutarse en el proceso HTTP de una API pública.

Los cultivos de una solicitud se procesan secuencialmente, con subprocesos aislados.
`--max-workers` limita los procesos internos del motor por cultivo (predeterminado 2).
Cada cultivo vuelve a preparar su clima; no existe caché compartida entre cultivos.

```text
results/evaluations/evaluation_<id>/
  parcel.geojson
  evaluation.json
  maize/
    config.ini
    engine.log
    plant_params/maize.inf
    simulation_downscaled/...
    simulation_novar/Area_.../maize/...
    parcel/crop_suitability.tif
    parcel/climate_suitability.tif
    parcel/soil_suitability.tif
  potato/...
  rice/...
```

La configuración efectiva cambia rutas y opciones operativas para el aislamiento;
se conservan escenario, manejo y reglas científicas del INI seleccionado. La
variante resumida es `novar`. La conversión de precipitación a décimas de mm y
su conversión posterior a mm permanecen en el motor existente.

El manifiesto guarda la geometría usada, hashes de entradas, parámetros, código,
configuración y rásteres de parcela; tiempos, estados, resultados y comprobación
de que los insumos no cambiaron durante el trabajo. Se actualiza después de cada
cultivo. Es evidencia local, no una base de datos ni auditoría de usuarios.

## Resumen y comparación

Se usan las celdas que intersectan la parcela, incluso cuando el polígono es más
pequeño que una celda y no contiene su centro. Las áreas se calculan mediante
intersecciones y la proyección de áreas equivalentes EPSG:6933.

Por cultivo, clima y suelo se informa media ponderada por superficie válida,
mínimo, máximo, número de celdas válidas, superficie válida, fracción de cobertura
y superficie con aptitud cero. La escala de aptitud es **0 a 100**; la fracción de
cobertura usa **0 a 1**. Nodata, NaN y valores fuera de 0 a 100 se excluyen.
Un cero válido participa en la media; no se convierte en ausencia de información.

El ranking compara `crop_suitability` usando la **misma superficie válida común**
entre los cultivos con cobertura. Ordena la media descendente y mantiene empates.
Publica su cobertura común, alternativas fallidas y alternativas sin cobertura.
Sin superficie común no hay ranking. Si falta algún cultivo,
`all_selected_crops_comparable` es falso. Una posición superior puede corresponder
a una aptitud baja; el ranking no demuestra rentabilidad ni constituye por sí solo
una recomendación agronómica.

## Estados

| Ámbito | Estado | Significado |
|---|---|---|
| Solicitud | `running` | Procesamiento en curso. |
| Solicitud | `completed` | Todos los cultivos terminaron; revisar cobertura individual. |
| Solicitud | `partial` | Algún cultivo falló y otros finalizaron. |
| Solicitud | `failed` | Fallaron todos o se detectaron cambios en los insumos. |
| Cultivo | `succeeded` | Resultados calculados con cobertura de aptitud de cultivo. |
| Cultivo | `no_coverage` | Cálculo finalizado, pero sin puntuaciones válidas para la parcela. |
| Cultivo | `failed` | Fallo registrado; se conservan logs y continúan los demás. |

La CLI devuelve código 0 para `completed`, 1 para `partial`/`failed` y 2 para
solicitud inválida. Una cobertura nula no equivale a un error del proceso:
el consumidor debe revisar el manifiesto además del código de salida.

## Comprobaciones realizadas

22 pruebas automáticas pasan, incluidas selección, parcelas pequeñas, huecos,
geometría fuera del límite, ceros válidos, nodata, pesos, empates, soporte disjunto,
fallos parciales, fallo de todos y exportación de valores inválidos como nodata.

Se ejecutó el motor real con maíz, papa y arroz en dos solicitudes:

- Diagnóstico provincial: `results/evaluations/evaluation_xfjrhxq8/evaluation.json`.
- Parcela sintética de aproximadamente 4,84 ha:
  `results/evaluations/evaluation_5cgva7iy/evaluation.json`.
  Los tres finalizaron, con 100 % de cobertura común; papa obtuvo 19/100,
  maíz 0/100 y arroz 0/100. Son resultados del ejemplo, no de una parcela del usuario.

Los tres cultivos están comprobados técnicamente en este flujo. Los otros 76
parámetros permanecen seleccionables, sin afirmar que todos sus cálculos hayan
sido comprobados. No se modifican las reglas para elevar las puntuaciones.

## Límites actuales y conexión futura al backend

El motor calcula la malla regional de 28 por 21 celdas y luego resume la parcela.
Los rásteres recortados conservan las celdas intersectadas completas, incluso en
el borde. El resumen pondera únicamente el área interior. No se aumenta la
resolución aproximada de 4,6 km; parcelas dentro de la misma celda pueden recibir
los mismos valores.

El servicio aún no incluye API REST, autenticación, persistencia de usuarios,
cola, cancelación, reintentos, recuperación de trabajos interrumpidos ni cuotas.
Cada nueva invocación crea otro trabajo. El backend modular deberá incorporar
esas capacidades y transformar el manifiesto a DTO públicos sin exponer rutas
internas. El adaptador pertenecerá a infraestructura del contexto consumidor;
el controlador no debe invocar directamente el motor durante una solicitud HTTP.

El tiempo y el almacenamiento crecen con el número de cultivos: cada uno conserva
sus propios archivos de clima y resultados. La reutilización de insumos derivados
compatibles y una política de retención quedan como optimizaciones posteriores.
