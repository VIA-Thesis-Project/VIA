# Contribuir a VIA

Este documento define las reglas básicas para modificar VIA sin romper sus contratos arquitectónicos, científicos u operativos.

## Flujo de trabajo

Crea una rama desde `main` con un nombre que describa el propósito del cambio:

```text
feat/...
fix/...
docs/...
chore/...
test/...
refactor/...
```

Ejemplos:

```text
feat/frontend-handoff
fix/evaluation-status
docs/postman-guide
chore/repository-cleanup
```

Evita trabajar directamente sobre `main`.

## Commits

VIA utiliza Conventional Commits.

Ejemplos:

```text
feat(auth): add refresh token rotation
fix(worker): recover stale evaluation execution
docs(frontend): document Postman integration workflow
chore(repo): clean generated development artifacts
test(api): cover unauthorized project access
```

Usa commits pequeños y coherentes. No mezcles cambios científicos, refactors, documentación y despliegue en un mismo commit si pueden separarse razonablemente.

## Staging

Haz staging explícito de los archivos que pertenecen al cambio.

Ejemplo:

```powershell
git add README.md CHANGELOG.md CONTRIBUTING.md
```

Evita usar staging masivo cuando existan archivos locales, resultados científicos o tooling de agentes que no deban versionarse.

Antes de un commit:

```powershell
git status --short
git diff --check
git diff --cached --check
git diff --cached
```

## Secretos y archivos locales

Nunca subas:

- `.env` reales;
- tokens;
- contraseñas;
- llaves SSH;
- credenciales de proveedores;
- dumps de producción;
- datasets descargados o resultados pesados que estén excluidos por `.gitignore`;
- `.codex/`.

Los ejemplos de configuración deben usar valores ficticios y seguros.

## Arquitectura del backend

El backend es un modular monolith organizado en bounded contexts:

```text
backend/src/via_backend/contexts/
```

Cada contexto mantiene separación entre:

```text
domain/
application/
infrastructure/
interfaces/
```

Las reglas de dependencia se validan con Import Linter. No elimines ni debilites esos contratos para hacer pasar un cambio.

Antes de integrar cambios de backend ejecuta, como mínimo:

```powershell
python -m pytest backend/tests -q
```

Cuando el entorno esté preparado, ejecuta también las verificaciones de lint, tipos y arquitectura definidas por el proyecto.

## Cambios científicos

`CropSuiteLite/` contiene el motor científico utilizado por VIA.

No modifiques lógica científica únicamente para adaptar una respuesta de API o hacer pasar un smoke test. Los cambios científicos deben:

1. tener una justificación reproducible;
2. conservar trazabilidad de insumos y parámetros;
3. incluir o actualizar pruebas;
4. distinguir claramente lógica científica de Decision Support y generación LLM.

El LLM no determina la viabilidad científica de un cultivo.

## Migraciones de base de datos

Todo cambio persistente de esquema debe realizarse mediante Alembic.

No edites migraciones ya aplicadas en producción. Agrega una nueva revisión y valida que el repositorio tenga un único Alembic head.

## Docker y producción

La imagen de producción debe conservar, entre otros contratos:

- ejecución non-root;
- fuentes y configuraciones científicas de solo lectura;
- almacenamiento persistente de artifacts;
- workspace descartable;
- API sin exposición directa insegura;
- migraciones ejecutadas de forma controlada.

Los outputs de Graphify y tooling local de desarrollo no forman parte de la imagen Docker.

## Documentación

Si un cambio modifica un contrato visible para frontend, operaciones o despliegue, actualiza la documentación correspondiente en `docs/`.

Principales ubicaciones:

```text
docs/adr/
docs/architecture/
docs/frontend/
docs/implementation/
docs/operations/
docs/scientific/
```

## Pull requests

Antes de solicitar revisión:

```powershell
git status --short
git diff main...HEAD --check
```

La rama debe estar libre de archivos locales no intencionales y las pruebas relevantes deben pasar.
