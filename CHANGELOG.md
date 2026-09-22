# Changelog

Todos los cambios relevantes de VIA se documentan en este archivo.

El proyecto sigue [Semantic Versioning](https://semver.org/) y, mientras permanezca en la serie `0.x.y`, puede introducir cambios incompatibles entre versiones menores cuando sean necesarios para estabilizar la arquitectura y los contratos del sistema.

## [Unreleased]

## [0.1.0] - 2026-09-22

### Added

- Documentación de navegación y contribución del repositorio.
- Guía de integración y pruebas de la API mediante Postman.
- Política explícita de finales de línea multiplataforma mediante `.gitattributes`.

### Changed

- El README raíz presenta VIA como sistema completo, en lugar de describir únicamente el PoC de CropSuiteLite.
- Graphify usa `graphify-out/` como grafo canónico del repositorio para navegación asistida por agentes.
- El tooling local de agentes bajo `.codex/` queda fuera de Git y del knowledge graph del proyecto.
- La verificación del backend es independiente del directorio desde el que se invoque.

### Removed

- Grafo Graphify redundante bajo `backend/graphify-out/`.

## Convención de versiones

- `PATCH` (`0.1.1`): correcciones compatibles sin cambios funcionales relevantes de contrato.
- `MINOR` (`0.2.0`): nueva funcionalidad, cambios de contrato o evolución arquitectónica durante la etapa pre-1.0.
- `MAJOR` (`1.0.0`): primera línea considerada estable para integración y operación.

Cuando se cree una release, los elementos correspondientes se moverán desde `Unreleased` a una sección con formato:

```text
## [0.1.0] - YYYY-MM-DD
```
