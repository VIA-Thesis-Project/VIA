# Corrección de temperatura, pendiente y cobertura climática

Huaura es la cobertura de los insumos. Esta ejecución verifica el pipeline
sobre esos insumos; no implementa ni sustituye la evaluación de una parcela
delimitada mediante GeoJSON.

## Cambios

- **Temperatura:** se identifican los valores faltantes antes de convertir
  a enteros, se rellena temporalmente por vecino cercano solo cuando hay
  que interpolar y se restaura la cobertura original y el mar de destino.
  Un grid de igual tamaño no se interpola. Temperaturas negativas y cero
  siguen siendo observaciones válidas. Se mantiene la escala de décimas de °C.
- **Pendiente:** no se interpola innecesariamente el DEM cuando el grid
  coincide. Las diferencias usan vecinos válidos: centradas en el interior
  y unilaterales en el borde de cobertura. Si un eje no tiene vecino válido,
  se usa una extensión constante en ese eje; una celda totalmente aislada
  queda sin estimación. Se conservan las celdas sin DEM como nodata.
  Se mantiene la conversión de distancia existente del motor.
- **Cobertura climática:** una celda debe ser terrestre y tener temperatura
  diaria completa; en secano también requiere precipitación diaria completa.
  Los valores faltantes, incluidos -32767 y NaN, no se evalúan como días secos
  o fríos. Se aplica la exclusión en NumPy, xarray y en las salidas finales.
  La regla es conservadora: una observación diaria ausente excluye la celda
  de esta ejecución; no se imputa ni se evalúan solo temporadas parciales.
- **Salidas de cultivo:** se conserva nodata en el mar y en el resultado
  multiplicativo. No se convierte el producto de sentinelas negativos en
  una aptitud aparentemente válida.
- **Agregación de suelo:** un conjunto vacío de valores sigue siendo nodata,
  sin provocar la advertencia de media de una muestra vacía.

No se modificaron `maize.inf`, las funciones de pertenencia, los umbrales
agronómicos, los factores de unidades, los datos de entrada ni las salidas
anteriores. Las correcciones locales previas se conservaron.

## Validación ejecutada

Las 14 pruebas automáticas pasan. Incluyen temperatura negativa, cero real,
datos ausentes, costa a distinta resolución, equivalencia diaria entre
NumPy y xarray, y la pendiente de un plano con inclinación conocida y
huecos de nodata. Las pruebas climáticas tratan los `RuntimeWarning` como
errores para detectar conversiones numéricas inválidas.

Se ejecutó `CropSuiteLite.run()` desde una carpeta nueva con la configuración
actual de Huaura, sus cuatro trabajadores y paso de siembra de 10 días.
Se regeneraron 365 archivos de temperatura y 365 de precipitación.

| Comprobación | Antes | Después |
|---|---:|---:|
| Celdas terrestres con temperatura perdida a cero todo el año | 64 | 0 |
| Celdas terrestres con pendiente válida | 94 | 231 |
| Celdas fuera de Huaura con falsa aptitud climática 0 | 319 | 0 |
| Celdas terrestres sin resultado de cultivo | 137 | 7 |

Los 365 días de ambas variables coinciden exactamente con el original tras
aplicar el filtrado existente, la escala ×10, la cuantización y las máscaras:
**0 diferencias inesperadas**. Los GeoTIFF finales tienen EPSG:4326 y el
transformado del grid original, dentro de tolerancia numérica 1e-12.
No aparecen `RuntimeWarning` en la ejecución completa. Las advertencias
`NotGeoreferencedWarning` restantes corresponden a los TIFF temporales por
fecha usados internamente, no a los GeoTIFF finales verificados.

Distribuciones finales en el rectángulo de 588 celdas:

| Producto | -1: sin datos | 0 | 3 |
|---|---:|---:|---:|
| `climate_suitability.tif` | 357 | 224 | 7 |
| `crop_suitability.tif` | 364 | 218 | 6 |

Los 357 nodata climáticos corresponden a 356 celdas fuera de la cobertura
original y una celda provincial clasificada como mar. Las 231 celdas
terrestres sí tienen resultado climático. La aptitud sigue siendo baja
bajo el escenario y los parámetros actuales; corregir nodata no fuerza
una aptitud alta ni constituye validación agronómica con observaciones.

Las siete celdas terrestres que quedan sin resultado de cultivo coinciden
exactamente con la unión de faltantes de los **suelos originales**. Sus
índices `(fila, columna)`, empezando en cero, son:

```text
(4, 12), (6, 26), (8, 12), (8, 26), (9, 20), (9, 21), (14, 2)
```

No se rellenaron esos suelos ni se inventaron resultados para esas celdas.
La futura evaluación de parcelas debe informar si intersecta estos faltantes.

## Archivos y reproducción

Ejecución validada:

```text
results/huaura_environment_validation/run_mw_8gsjo/
  config.ini
  report.json
  simulation_downscaled/Area_-10N-77E--11N-76E/
  simulation_novar/Area_-10N-77E--11N-76E/maize/
```

`report.json` incluye recuentos, comparación con la ejecución anterior,
rutas de resultados y hashes SHA-256 verificados de todos los insumos
configurados y `maize.inf`. Todos permanecen sin cambios.

Desde `CropSuiteLite`, para comprobar o repetir en otra carpeta nueva:

```powershell
.venv/Scripts/python.exe -m unittest discover -s tests -v
.venv/Scripts/python.exe scripts/validate_huaura_environment.py
```

El script de validación crea una copia del INI con rutas absolutas y una
salida nueva para cada auditoría. Tras la limpieza del 10/09/2026, el INI
habitual apunta a `results/huaura_environment_validation/run_mw_8gsjo/simulation`.
El YAML de Huaura lo selecciona mediante `GENERAL.run_config`: no regenera
los parámetros del cultivo ni deriva otra salida del nombre del escenario.

Para el arranque habitual desde `CropSuiteLite`:

```powershell
.venv/Scripts/python.exe run_cropsuitelite.py -config yaml_configurations/general_config_huaura.yaml
```

El motor reutiliza los resultados validados existentes. Las salidas antiguas
de `huaura_corrected` se retiraron del proyecto. Los antecedentes de limpieza
están en `../../poc_via_cslite_archive/cleanup_20260910_012022/`, relativo a
`CropSuiteLite`. El `report.json` original se conserva sin editar: sus hashes
registran el estado de los archivos durante aquella validación, anterior al
cambio de ruta del INI habitual.
