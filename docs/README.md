# Documentación de VIA

Este directorio contiene la documentación mantenida del sistema. El README raíz ofrece una vista general; aquí se encuentran los detalles por área.

## Navegación

### `adr/`

Architecture Decision Records.

Documenta decisiones arquitectónicas relevantes y su contexto histórico, por ejemplo modular monolith, bounded contexts, persistencia, workers, integración con CropSuiteLite y trazabilidad científica.

Usa esta carpeta cuando necesites responder **por qué** se tomó una decisión.

### `architecture/`

Descripción del diseño actual del sistema y de sus slices.

Usa esta carpeta para entender:

- bounded contexts;
- dependencias;
- responsabilidades;
- flujos entre módulos;
- estructura del backend.

### `frontend/`

Contrato de integración para el frontend.

Incluye documentación sobre:

- API;
- evaluaciones asíncronas;
- manejo de errores;
- entorno de desarrollo;
- pruebas mediante Postman.

Punto de entrada recomendado:

```text
docs/frontend/README.md
```

### `implementation/`

Roadmap, preservación del PoC y documentación relacionada con la evolución de la implementación.

### `operations/`

Operación y releases de producción.

Debe utilizarse para procedimientos de despliegue, rollback, backups y verificación de releases.

### `scientific/`

Documentación relacionada con datos, fixtures y comportamiento científico de Huaura/CropSuiteLite.

## Otras fuentes de documentación

### Motor científico

```text
CropSuiteLite/docs/
```

Contiene documentación propia del motor y de las correcciones/adaptaciones científicas.

### Knowledge base

```text
knowledge/
```

Contiene la documentación y fuentes relacionadas con el corpus agronómico utilizado por Decision Support.

### Knowledge graph para agentes

```text
graphify-out/
```

Es un artefacto versionado de navegación estructurada del repositorio. Los agentes deben preferir consultas Graphify dirigidas antes que recorrer el código completo sin contexto.

## Regla de mantenimiento

No dupliques documentación entre varias carpetas salvo que sea estrictamente necesario.

Como guía:

- README raíz: qué es VIA y cómo navegar el repo;
- ADR: por qué se tomó una decisión;
- architecture: cómo está diseñado actualmente;
- frontend: cómo consumir los contratos;
- operations: cómo operar/desplegar;
- scientific: cómo se justifican y reproducen aspectos científicos.
