# VIA

VIA es un sistema de apoyo a decisiones para evaluar la viabilidad agroclimática de cultivos a nivel de parcela en Huaura, Lima.

Integra procesamiento geoespacial, un motor científico determinista basado en CropSuiteLite y un módulo de Decision Support con recuperación de evidencia agronómica y generación de recomendaciones asistida por LLM.

> Estado: desarrollo pre-1.0 orientado a tesis e integración frontend.

## Arquitectura

VIA está implementado como un modular monolith con bounded contexts independientes y separación entre Domain, Application, Infrastructure e Interfaces.

Principales módulos:

- Identity & Access
- Farm Management
- Environmental Information
- Agroclimatic Evaluation
- Decision Support

La evaluación científica es ejecutada por CropSuiteLite mediante un adapter aislado. El LLM no determina la viabilidad científica de los cultivos.

## Stack

- Python 3.11+
- FastAPI
- PostgreSQL / PostGIS
- SQLAlchemy
- Alembic
- CropSuiteLite
- OpenAI API
- Docker / Docker Compose
- GitHub Actions
- GHCR
- DigitalOcean

## Estructura del repositorio

```text
.
├── backend/          Backend VIA y migraciones
├── CropSuiteLite/    Motor de evaluación científica
├── data/             Configuración y datos mínimos versionables
├── knowledge/        Corpus agronómico para Decision Support
├── docs/             Arquitectura, ADRs, frontend y operaciones
├── deploy/           Configuración de despliegue
├── infra/            Infraestructura
├── scripts/          Automatización, validación y operaciones
├── graphify-out/     Knowledge graph del repositorio para agentes IA
└── .github/          CI/CD
```

## Backend

El backend se encuentra en:

```text
backend/src/via_backend/
```

Los bounded contexts principales están en:

```text
backend/src/via_backend/contexts/
```

La dirección de dependencias arquitectónicas se valida automáticamente con Import Linter.

## Motor científico

CropSuiteLite vive en:

```text
CropSuiteLite/
```

VIA lo consume mediante adapters y procesos aislados. Los datasets originales y resultados pesados no se almacenan normalmente en Git.

La documentación específica del motor se encuentra en:

```text
CropSuiteLite/docs/
```

## Desarrollo local

Instalar el backend en modo editable:

```bash
cd backend
python -m pip install -e ".[test]"
```

Ejecutar pruebas:

```bash
python -m pytest
```

Ejecutar API local:

```bash
via-api
```

La configuración de entorno de ejemplo está disponible en:

```text
backend/.env.example
backend/.env.production.example
```

No se deben versionar secretos ni archivos `.env` reales.

## API e integración frontend

La documentación destinada a frontend se encuentra en:

```text
docs/frontend/
```

Incluye contratos de API, evaluaciones asíncronas, manejo de errores y configuración de desarrollo.

Los endpoints de producción requieren autenticación salvo aquellos explícitamente públicos, como `/health`.

Swagger/OpenAPI público está deshabilitado en producción.

## Evaluaciones

Las evaluaciones son asíncronas:

```text
Request
   ↓
PostgreSQL
   ↓
Worker
   ↓
CropSuiteLite
   ↓
Scientific result
   ↓
Decision Support
```

El resultado científico, su evidencia y sus limitaciones permanecen separados de las recomendaciones generadas por LLM.

## Persistencia

VIA utiliza PostgreSQL/PostGIS.

Las migraciones se encuentran en:

```text
backend/migrations/
```

y se administran mediante Alembic.

## CI/CD

GitHub Actions valida, entre otros aspectos:

- build del contenedor Linux;
- ejecución non-root;
- integridad de dependencias;
- migraciones PostgreSQL/PostGIS;
- almacenamiento persistente de artifacts;
- mounts científicos read-only;
- configuración Compose de producción.

Las imágenes validadas se publican en GHCR usando tags inmutables asociados al commit Git.

## Documentación

- `docs/adr/` — Architecture Decision Records
- `docs/architecture/` — arquitectura del sistema
- `docs/frontend/` — integración frontend
- `docs/implementation/` — roadmap e implementación
- `docs/operations/` — despliegue y operación
- `docs/scientific/` — aspectos científicos
- `knowledge/` — documentación del corpus RAG

## Versionado

VIA utiliza Semantic Versioning.

La etapa actual corresponde a la serie:

```text
0.x.y
```

hasta alcanzar una interfaz y comportamiento considerados estables para `1.0.0`.

## Estado del proyecto

Actualmente están implementados el backend, persistencia, ejecución agroclimática, autenticación/autorización, trazabilidad científica, Decision Support, contenerización y despliegue backend.

La interfaz web continúa en desarrollo.

## License

Pendiente de definir.
