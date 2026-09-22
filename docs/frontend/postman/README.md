# Colección Postman de VIA

Estos archivos permiten probar el flujo frontend real del backend VIA sin configurar cada request manualmente:

- `VIA.postman_collection.json`: colección Postman Schema v2.1.
- `VIA.postman_environment.json`: environment importable sin credenciales ni tokens.

La fuente principal es la aplicación FastAPI actual. `docs/frontend/` se usó como validación secundaria. La colección conserva los prefijos mixtos reales: `/health`, `/projects` y `/datasets` no están versionados; autenticación, capacidades, evaluaciones y Decision Support usan `/api/v1`.

## Importar y preparar

1. En Postman, selecciona **Import** e importa los dos archivos JSON.
2. Selecciona el environment **VIA** en la esquina superior derecha.
3. Edita `email` y `password` con las credenciales de un usuario de integración dedicado.
4. Verifica `base_url`. El valor inicial es `https://ubuntu-s-1vcpu-2gb-nyc1.tail5eff67.ts.net`.
5. Ejecuta **01 - Authentication / Login**. El test guarda `access_token` automáticamente.
6. Ejecuta los folders en orden numérico o usa el Collection Runner.

No exportes ni versionees un environment después de introducir credenciales o tokens. `password` y `access_token` se entregan vacíos y marcados como secretos.

## Flujo y variables automáticas

La colección usa Bearer `{{access_token}}` en todas las requests protegidas. Las requests públicas sobrescriben la autenticación heredada con `No Auth`.

Los tests rellenan automáticamente:

| Variable | Origen |
| --- | --- |
| `access_token` | Login y Refresh Session |
| `project_id` | Create Project |
| `parcel_id`, `parcel_version` | Create Parcel y Create Parcel Version |
| `dataset_id`, `dataset_version_id` | Primer binding publicado por Get Evaluation Capabilities |
| `evaluation_id` | Create Evaluation |
| `evaluation_poll_count`, `last_evaluation_status` | Poll Evaluation Status |

Las variables configurables son `base_url`, `email`, `password`, `crop_id`, `water_regime`, `evaluation_poll_max` y `evaluation_poll_delay_ms`. Los valores iniciales solicitados son `crop_id=maize` y `water_regime=rainfed`. Capabilities verifica que ese cultivo y régimen estén disponibles en el deployment; no reemplaza silenciosamente una opción no soportada.

La geometría de parcela es sintética y no contiene datos de usuario. Fue verificada contra el asset autoritativo de Huaura versionado en este repositorio. Si el AOI del deployment difiere del repositorio, reemplaza el ejemplo por otra geometría sintética permitida.

## Evaluaciones y polling

`Create Evaluation` envía sólo `parcel_reference`, cultivos, regímenes y referencias exactas de versiones ambientales. No envía una geometría ni un `parcel_snapshot` suministrado por el cliente.

`Poll Evaluation Status` funciona de dos maneras:

- Ejecutado manualmente, realiza una consulta y muestra el estado actual.
- En Collection Runner, vuelve a llamarse mientras el estado sea `queued`, `preparing`, `running` o `summarizing`. Espera `evaluation_poll_delay_ms` entre intentos y nunca supera `evaluation_poll_max` (30 intentos de 2 segundos por defecto).

El polling termina al recibir `succeeded`, `failed` o `cancelled`. Un fallo/cancelación o agotar el máximo produce un test fallido claro y detiene el Runner. No hay loop infinito. Después de `succeeded`, el Runner continúa con resultado, evidencia, limitaciones y Decision Support.

No hay assertions sobre valores científicos concretos. Los tests verifican únicamente estados HTTP, JSON, campos contractuales y vocabularios explícitos como lifecycle/availability.

## Refresh cookie y logout

Login establece una refresh cookie rotatoria con `HttpOnly`, `Secure` y `Path=/api/v1/auth`. Postman debe conservarla en su cookie jar para el host de `base_url`.

`Refresh Session` no envía body ni intenta leer la cookie desde JavaScript; utiliza el cookie jar y guarda únicamente el nuevo access token retornado en JSON. `Logout` utiliza la misma cookie, espera `204` y limpia `access_token` del environment.

El backend valida `Origin` sólo cuando el cliente envía ese header. Postman normalmente no lo añade. Un navegador sí debe usar un origen permitido por el deployment.

## Environmental Inputs

El flujo portable obtiene las referencias ambientales desde `GET /api/v1/evaluation-capabilities` y luego consulta sus metadatos y cobertura. Si capabilities retorna `503`, no publica bindings, o no incluye `maize/rainfed`, la evaluación no puede construirse fielmente; corrige la configuración del deployment o selecciona opciones que el endpoint publique.

Los siguientes endpoints reales no están en la colección:

- `POST /datasets`
- `POST /datasets/{dataset_id}/versions`

Ambos requieren rol ADMIN y mutan catálogo compartido. Además, registrar una versión no crea por sí mismo el binding científico que requiere una evaluación. Omitirlos evita cambios accidentales durante el Runner y evita fingir un fixture portable que el contrato no ofrece. Todos los endpoints de lectura y cobertura necesarios para el flujo frontend sí están incluidos.

## Producción, OpenAPI y CORS

Producción deshabilita deliberadamente:

- `/docs`
- `/redoc`
- `/openapi.json`

Un `404` en esas rutas es esperado; no se incluyen como requests. La fuente machine-readable versionada está en `docs/frontend/openapi.json`.

Postman no está sujeto a CORS del navegador. Que una request funcione en Postman no demuestra que el origen de una aplicación web esté permitido por CORS.

## Endpoints incluidos

| Folder | Requests |
| --- | --- |
| 00 - Health | `GET /health` |
| 01 - Authentication | `POST /api/v1/auth/login`; prueba negativa `GET /api/v1/auth/me` sin Bearer |
| 02 - Projects | `POST/GET /projects`; `GET /projects/{project_id}` |
| 03 - Parcels | `POST/GET /projects/{project_id}/parcels`; `GET /projects/{project_id}/parcels/{parcel_id}`; `POST .../versions` |
| 04 - Environmental Inputs | capabilities; datasets/versiones GET; coverage POST |
| 05 - Evaluations | `POST/GET /api/v1/evaluations`; status GET |
| 06 - Scientific Results | result, evidence y limitations GET |
| 07 - Decision Support | knowledge GET; recommendations POST/GET |
| 08 - Session | current user GET; refresh POST; logout POST |

## Notas de documentación

No se detectaron diferencias entre las rutas/schemas de FastAPI y `docs/frontend/api-reference.md`. `docs/frontend/postman.md` propone `crop_id=avocado` como valor sugerido, mientras este environment usa `maize` según el requerimiento de esta colección; el endpoint de capabilities sigue siendo la autoridad en cada deployment.
