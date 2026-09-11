# Diagnóstico de precipitación de Huaura

Este documento registra la auditoría inicial con la caché anterior.
La corrección posterior de pérdida de cobertura y su validación están en
[huaura_precipitation_downscaling.md](huaura_precipitation_downscaling.md).
Huaura es la cobertura de los insumos; el objetivo del producto es evaluar
una parcela delimitada por GeoJSON dentro de esa cobertura.

## Corrección de unidades

La entrada `Prec_avg.tif` se interpreta como mm/día. En
`src/downscaling.py::process_precday_interp`, se aplica el umbral diario de
la configuración, se multiplica por 10 y se convierte a `int16`.
Los archivos `ds_prec_*.nc` contienen décimas de mm/día. No tienen un
`scale_factor` que deshaga automáticamente esa multiplicación al leerlos.

`CropSuite.py::compute_climate_suitability` carga esos archivos mediante
`read_area_from_netcdf_list`, sin convertir sus unidades.
`process_day_climsuit_memopt` selecciona el ciclo y calcula:

```python
prec[water_mask == 1] = np.sum(precipitation[water_mask == 1], axis=1)
prec_mm = prec[water_mask == 1] / 10.0
```

Se pasa `prec_mm` a `get_suitability_val_dict(..., 'prec', prec_mm)`.
Esta última función recorta al dominio de `prec_vals` y evalúa la
interpolación; no convierte unidades. Las fórmulas se construyen con los
valores de `maize.inf`, sin escalarlos. Los `conversion_factor` del INI
pertenecen a los parámetros de suelo, no a esta conversión de precipitación.

La copia de trabajo había eliminado `/10` tanto en NumPy como en xarray.
Se restauró en ambas rutas y se documentó el contrato de unidades en el
downscaling. Se conservaron los cambios locales previos de requisitos de
siembra y ejecución de trabajadores. Los umbrales de siembra y de lluvia
letal siguen comparándose en décimas de mm, usando sus factores `*10`.

## Verificación con los archivos disponibles

Escenario: ACCESS-ESM1-5, SSP126, 2021–2040. Ciclo: 110 días.
El raster tiene 28 columnas por 21 filas. La máscara provincial usa el
valor **2**, y contiene 232 celdas, de las cuales 231 son terrestres.

| Medida | 550 celdas terrestres del rectángulo | 231 celdas terrestres de Huaura |
|---|---:|---:|
| Media acumulada días 0–109, unidades almacenadas | 512,807 | 1220,970 |
| Media acumulada días 0–109, mm | 51,281 | 122,097 |
| Media del mejor ciclo por celda, mm (365 fechas evaluadas) | 51,757 | 123,232 |
| Máximo de cualquier ciclo/celda en la caché, mm | 442,700 | 442,700 |

Por tanto, **512 unidades almacenadas no son 512 mm**. Un ciclo de
512 mm reales se representa mediante una suma interna de 5120 y produce
una pertenencia de 0,7704 (77/100 al guardar como entero).

Se recalculó clima y cultivo con los módulos de producción, reutilizando
la caché climática y escribiendo a una carpeta nueva. Se mantuvieron los
datos, parámetros agronómicos y paso de siembra de 10 días del INI;
se usó un trabajador. Los resultados coinciden con los archivos existentes:

- `climate_suitability.tif`: -1 = 38, 0 = 546, 3 = 4.
- `crop_suitability.tif`: -1 = 494, 0 = 94.
- Factor de precipitación: -1, 0, 3, 6, 12, 19, 27, 29, 48.
- Las cuatro bandas de `all_climlim_factors.tif` coinciden exactamente.

En las fechas seleccionadas, 33 celdas con factor de precipitación positivo
tienen factor de temperatura 0; otras 130 tienen temperatura positiva y
precipitación 0. Solo cuatro tienen ambos positivos. La aptitud climática
es el mínimo de los factores, no únicamente la pertenencia de precipitación.

El motor omite cálculos si encuentra resultados o temporales existentes;
editar el código y volver a ejecutar en la misma salida puede reutilizar
resultados anteriores. La auditoría usó una carpeta vacía para evitarlo.

## Hallazgo adicional: pérdida de lluvia en el downscaling

La corrección de unidades no demuestra que todo el downscaling sea correcto.
La media anual de Huaura es 297,585 mm en el original y 169,151 mm en la
caché. Aplicar solamente el umbral configurado de 0,5 mm/día y la
cuantización a décimas al original daría 259,419 mm/año.

Se detectaron **64 celdas terrestres dentro de Huaura** con precipitación
original válida y lluvia superior al umbral, pero con los 365 valores de
la caché iguales a cero. Sus acumulados originales anuales varían entre
73,058 y 730,409 mm. Una ejecución en memoria de
`process_precday_interp` para el día 0, con el original y la configuración
actual, reproduce exactamente la caché sobre tierra, incluidos esos ceros.
Esto señala un problema adicional anterior a la función de pertenencia;
no es evidencia de que deba eliminarse `/10`.

No se cambió la lógica de interpolación o máscaras en aquel ajuste de unidades.
La pérdida se corrigió posteriormente; el estado vigente está documentado en
[huaura_environment_correction.md](huaura_environment_correction.md).
Los máximos y la aptitud descritos arriba corresponden a la caché histórica.

## Reproducción

Desde `CropSuiteLite`:

```powershell
.venv/Scripts/python.exe -m unittest discover -s tests -v
.venv/Scripts/python.exe scripts/validate_huaura_environment.py
```

Las tres pruebas comprueban el escalamiento en ambos métodos de downscaling,
la evaluación NumPy y la evaluación xarray: 512 mm → 77, 750 mm → 100,
51,2 mm → 0, y 512 mm sin lluvia inicial → 0 por el requisito de siembra.

La validación vigente comprueba clima, pendiente y resultados finales en una
carpeta nueva. Los hashes de los insumos y de `maize.inf` se verifican antes
y después.

La auditoría parcial de este documento se archivó en la limpieza del
10/09/2026. Su reporte se conserva en
`../../poc_via_cslite_archive/cleanup_20260910_012022/reports/CropSuiteLite/results/huaura_precipitation_audit/`
y su script en
`../../poc_via_cslite_archive/cleanup_20260910_012022/archived/CropSuiteLite/scripts/audit_huaura_precipitation.py`,
relativos a `CropSuiteLite`. Sus GeoTIFF y cachés anteriores se retiraron.
