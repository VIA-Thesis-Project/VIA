# Probar la API de VIA con Postman

Esta guía permite probar el backend desplegado antes de que exista un frontend definitivo.

Postman no está sujeto a CORS del navegador, por lo que puede utilizarse para validar la API aunque todavía no se haya definido el dominio del frontend.

## Base URL de integración

El endpoint público actualmente disponible es:

```text
https://ubuntu-s-1vcpu-2gb-nyc1.tail5eff67.ts.net
```

Configúralo como variable de entorno de Postman:

```text
base_url
```

Valor:

```text
https://ubuntu-s-1vcpu-2gb-nyc1.tail5eff67.ts.net
```

No hardcodees la URL en todas las requests; el hostname de integración puede cambiar.

## Variables recomendadas

Crea un Environment de Postman con:

```text
base_url
access_token
project_id
parcel_id
evaluation_id
crop_id
water_regime
```

Valores iniciales sugeridos:

```text
crop_id = avocado
water_regime = rainfed
```

No guardes contraseñas reales en un environment exportado o versionado.

## 1. Health

Request:

```http
GET {{base_url}}/health
```

Respuesta esperada:

```json
{
  "status": "ok"
}
```

Este endpoint es público.

## 2. Login

Request:

```http
POST {{base_url}}/api/v1/auth/login
Content-Type: application/json
```

Body:

```json
{
  "email": "USUARIO_ASIGNADO",
  "password": "PASSWORD"
}
```

La respuesta contiene un access token. Además, el backend utiliza una refresh cookie segura.

No copies ni publiques credenciales de smoke o producción en el repositorio.

### Guardar el access token automáticamente

En la pestaña **Tests** de la request de login puedes usar:

```javascript
const body = pm.response.json();

if (body.access_token) {
    pm.environment.set("access_token", body.access_token);
}
```

## 3. Requests autenticadas

Para una request protegida, abre:

```text
Authorization
```

Selecciona:

```text
Bearer Token
```

y usa:

```text
{{access_token}}
```

También puedes configurarlo a nivel de Collection para que las requests hereden el token.

## 4. Usuario autenticado

```http
GET {{base_url}}/api/v1/auth/me
Authorization: Bearer {{access_token}}
```

Debe devolver la identidad del usuario autenticado.

## 5. Projects y Parcels

Los recursos de proyectos están protegidos por ownership.

Punto de entrada:

```http
GET {{base_url}}/projects
Authorization: Bearer {{access_token}}
```

Para creación y edición de proyectos/parcelas utiliza los payloads definidos en:

```text
docs/frontend/api-reference.md
```

Una parcela debe cumplir los contratos geográficos definidos por VIA y estar dentro del AOI permitido.

Guarda los identificadores devueltos como:

```text
project_id
parcel_id
```

## 6. Evaluaciones

La creación de una evaluación es asíncrona.

Endpoint de creación:

```http
POST {{base_url}}/api/v1/evaluations
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

Usa el body vigente documentado en `docs/frontend/api-reference.md`.

Guarda el identificador devuelto en:

```text
evaluation_id
```

## 7. Consultar estado

```http
GET {{base_url}}/api/v1/evaluations/{{evaluation_id}}
Authorization: Bearer {{access_token}}
```

El frontend debe tratar la evaluación como un proceso asíncrono y consultar su estado hasta alcanzar un estado terminal.

Consulta `docs/frontend/async-evaluations.md` para el comportamiento esperado.

## 8. Resultado científico

```http
GET {{base_url}}/api/v1/evaluations/{{evaluation_id}}/result
Authorization: Bearer {{access_token}}
```

Cuando la evaluación se complete correctamente, la respuesta debe indicar disponibilidad final del resultado.

Un valor de suitability igual a `0` puede ser un resultado científico válido; no implica por sí mismo un error del backend.

## 9. Evidencia

```http
GET {{base_url}}/api/v1/evaluations/{{evaluation_id}}/evidence
Authorization: Bearer {{access_token}}
```

La evidencia científica debe consumirse separadamente de la recomendación generada por LLM.

## 10. Limitaciones

```http
GET {{base_url}}/api/v1/evaluations/{{evaluation_id}}/limitations
Authorization: Bearer {{access_token}}
```

Este endpoint expone los factores limitantes obtenidos a partir de la evaluación científica.

## 11. Decision Support: knowledge retrieval

```http
GET {{base_url}}/api/v1/decision-support/evaluations/{{evaluation_id}}/knowledge?crop_id={{crop_id}}&water_regime={{water_regime}}
Authorization: Bearer {{access_token}}
```

La respuesta incluye la evidencia recuperada por el componente RAG cuando está disponible.

## 12. Decision Support: recommendation

La recomendación utiliza el resultado científico y evidencia recuperada. No reemplaza al motor de viabilidad.

Utiliza el contrato actual documentado en:

```text
docs/frontend/api-reference.md
```

para el endpoint y payload de generación de recomendaciones.

La respuesta debe conservar trazabilidad hacia las fuentes/evidencias utilizadas.

## Refresh token

El refresh token se administra mediante cookie segura con atributos de producción como:

```text
HttpOnly
Secure
Path=/api/v1/auth
```

No intentes leer el refresh token desde JavaScript ni almacenarlo manualmente en `localStorage`.

En Postman, las cookies pueden administrarse desde el cookie jar de la aplicación.

## Logout

Usa el endpoint de logout definido por el contrato de autenticación vigente. Después del logout no reutilices un access token vencido o revocado.

## Swagger en producción

Los siguientes endpoints están intencionalmente deshabilitados en producción:

```text
/docs
/redoc
/openapi.json
```

Un `404` en esas rutas es esperado.

Para contratos de integración utiliza la documentación versionada bajo:

```text
docs/frontend/
```

## CORS

CORS no afecta a Postman.

Cuando exista una URL HTTPS definitiva para el frontend web, producción deberá permitir explícitamente ese origen. No debe configurarse `*` para un frontend que utilice credenciales/cookies.

## Recomendación para desarrollo frontend

Mantén la Base URL fuera del código fuente.

Ejemplo conceptual:

```text
VITE_API_BASE_URL=https://...
```

El valor real debe configurarse por entorno.

## Seguridad

- Usa un usuario de integración dedicado.
- No compartas contraseñas por commits, capturas o archivos de colección.
- No exportes environments con secretos.
- No reutilices credenciales administrativas para desarrollo frontend.
- Respeta ownership: un usuario no debe acceder a recursos de otro.

## Colección importable

Los archivos listos para importar en Postman se encuentran en:

- `docs/frontend/postman/VIA.postman_collection.json`
- `docs/frontend/postman/VIA.postman_environment.json`
- `docs/frontend/postman/README.md`