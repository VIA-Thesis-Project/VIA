# Precipitación: conservación de la cobertura de datos de Huaura

La corrección posterior de temperatura, pendiente y máscara climática, con
una ejecución completa nueva, está documentada en
[huaura_environment_correction.md](huaura_environment_correction.md).

Huaura es la cobertura de los insumos agroambientales. La evaluación del
producto corresponderá a una parcela delimitada por un GeoJSON dentro de
Huaura. Los recuentos de esta validación comprueban la integridad de los
insumos; no representan una evaluación de aptitud de toda la provincia.
No se ha implementado aquí la entrada GeoJSON ni calculado aptitud parcelaria.

## Corrección en `process_precday_interp`

1. Identificar NaN, infinitos, valores negativos y el nodata declarado
   antes de aplicar el umbral diario; trabajar sobre una copia.
2. Conservar el umbral configurado de precipitación, en mm/día.
3. Rellenar temporalmente los valores faltantes con el vecino válido más
   cercano. Un cero válido sigue siendo un día seco, no se rellena.
4. Multiplicar por 10, conservando el formato interno de décimas de mm/día.
5. Si el grid ya tiene la forma de destino, no interpolar los valores.
   Si cambia la resolución, interpolar la lluvia con el método solicitado
   y la máscara de datos faltantes por vecino cercano. `preserve_range=True`
   impide normalizar valores por el tipo numérico de entrada.
6. Restaurar nodata en la cobertura faltante y en el mar de destino,
   representado tanto por 0 como por NaN. Guardar `int16`, nodata -32767.

El caso completamente sin datos produce solo nodata. Los cambios de
resolución por vecino cercano admiten tamaños no múltiplos y reducciones.
El relleno temporal no autoriza extrapolar la cobertura a zonas sin insumos.

La versión local encontrada al iniciar esta corrección ya contenía un
relleno por vecino cercano, pero había dejado sin aplicar la máscara original.
En el día 0 extendía lluvia a 295 celdas fuera de la cobertura de la entrada.
La corrección restaura las 356 celdas faltantes como nodata.

## Qué significan los 37 ceros

El INI mantiene `downscaling_precipitation_per_day_threshold = 0.5`.
En el día 0 hay exactamente 37 celdas terrestres de Huaura con lluvia
original inferior a 0,5 mm/día. Por tanto, esos ceros son consecuencia de
la regla existente, no pérdida por contaminación del borde.

| Día 0, cobertura de Huaura | Umbral configurado 0,5 mm/día | Control aislado con umbral 0 |
|---|---:|---:|
| Celdas terrestres con lluvia | 194 | 231 |
| Celdas terrestres con cero | 37 | 0 |
| Celdas de mar excluidas | 1 | 1 |

La cobertura tiene 232 celdas, pero `landsea.tif` marca una como mar.
Por ello, el máximo compatible con esa máscara es 231 celdas terrestres.
Los 356 NaN de `Prec_avg.tif` indican falta de cobertura; no deben
interpretarse todos como océano, pues la máscara landsea clasifica parte
del exterior provincial como tierra. La salida del día 0 contiene 357
nodata: 356 fuera de cobertura y esa celda de mar.

## Validación ejecutada

- Ocho pruebas automáticas aprobadas: costa, grid idéntico, cambios de
  resolución, máscaras 0/NaN, entradas completamente faltantes, sentinelas,
  conservación del array de entrada y las pruebas previas de unidades.
- Reejecución de `interpolate_precipitation` con el archivo real para los
  365 días, en una carpeta nueva, sin reutilizar la caché anterior.
- Comparación de todas las celdas contra el original con el mismo umbral,
  conversión a décimas y máscaras: **0 diferencias inesperadas**.
- **0 celdas-día positivas perdidas** respecto de ese resultado esperado.
- Hashes SHA-256 de precipitación, DEM, landsea y `maize.inf` sin cambios.

La validación de igualdad exacta se aplica al caso real, cuyos grids
coinciden. Cuando cambia la resolución, la interpolación puede cambiar
valores locales; las pruebas de costa comprueban que datos faltantes no
atenúen artificialmente una lluvia terrestre constante.

Desde `CropSuiteLite`:

```powershell
.venv/Scripts/python.exe -m unittest discover -s tests -v
.venv/Scripts/python.exe scripts/validate_huaura_environment.py
```

Esta auditoría parcial fue sustituida por la validación completa descrita en
[huaura_environment_correction.md](huaura_environment_correction.md).
La serie diaria vigente está en
`results/huaura_environment_validation/run_mw_8gsjo/simulation_downscaled/Area_-10N-77E--11N-76E/`.

Durante la limpieza del 10/09/2026 se retiraron los NetCDF de la auditoría
parcial. Su reporte y script se guardaron, relativos a `CropSuiteLite`, en:

```text
../../poc_via_cslite_archive/cleanup_20260910_012022/reports/CropSuiteLite/results/huaura_downscaling_validation/run_r8rjpv5j/report.json
../../poc_via_cslite_archive/cleanup_20260910_012022/archived/CropSuiteLite/scripts/validate_huaura_downscaling.py
```

El control con umbral cero fue solo una prueba diagnóstica. La configuración
vigente mantiene 0,5 mm/día. El motor reutiliza las salidas existentes;
`validate_huaura_environment.py` crea una salida nueva para comprobar cambios.
