# Intended backend structure

The accepted internal direction is to give every bounded context its own Domain, Application, Infrastructure, and Interfaces layers. The directory names illustrate responsibility; enforceability comes from dependency direction and public contracts.

## Layers

### Domain

Owns aggregates, entities, value objects, domain events, domain services, and repository abstractions needed to protect invariants. It has no dependency on HTTP, ORM models, queue clients, CropSuiteLite, or filesystem integration.

### Application

Coordinates use cases. It loads and persists aggregates through ports, invokes domain behavior, obtains public information from other contexts, and requests background execution. Commands and Queries belong here under the current recommendation because they express use-case intent. This placement is **recommended pending confirmation** of any academic convention. A different folder convention must not reverse the dependency direction.

### Infrastructure

Implements persistence, messaging, storage, anti-corruption adapters, and external integrations. It contains implementations such as `EvaluationRepository`, `EnvironmentalDataAdapter`, and the future `CropSuiteAdapter`.

### Interfaces

Receives REST or other inputs, checks interface-level structure, maps resources to Commands or Queries, delegates to Application, and maps results to public DTOs. Controllers contain neither scientific logic nor direct CropSuiteLite calls.

## Dependency direction

```text
Interfaces ------> Application ------> Domain
                         ^                ^
                         |                |
Infrastructure implements internal ports and repository contracts

Cross-context use: consumer Application port -> consumer Infrastructure ACL
                  -> provider public contract
```

Domain is the innermost policy layer. Application depends on Domain. Interfaces and Infrastructure depend inward through contracts. Composition or dependency injection connects implementations at startup.

## Illustrative directory structure

This tree is illustrative documentation only; it does not create backend code or settle the implementation language.

```text
backend/
  modules/
    evaluation/
      Domain/
        Model/
          Aggregates/
          Entities/
          ValueObjects/
          Events/
        Repositories/
          IEvaluationRepository
        Services/
      Application/
        Commands/
        Queries/
        Services/
          IEvaluationCommandService
          EvaluationCommandService
          IEvaluationQueryService
          EvaluationQueryService
        Ports/
          ICropSuitabilityEngine
          IEnvironmentalDataProvider
      Infrastructure/
        Repositories/
        CropSuite/
          CropSuiteAdapter
        Messaging/
        ACL/
      Interfaces/
        REST/
          Resources/
          Transform/
          EvaluationController
```

Names such as `Evaluation`, `ScientificRun`, or `SuitabilityEvidence` are model candidates from the source, not finalized class or table definitions. Repositories are proposed per aggregate, not mechanically per table. Read queries may use projections without turning them into mutation paths.

## Cross-context constraints

- A module must not write another context's tables or use its internal entities.
- Shared PostgreSQL infrastructure may use context-delimited schemas and migrations.
- Public facades or contract packages may be invoked locally in the monolith.
- An anti-corruption layer is warranted when models require translation; it is not required for a small stable contract with identical meaning.
- Do not hold a database transaction open while a long scientific calculation runs.

## Open decisions

The backend language and framework, exact aggregate boundaries, repository shapes, database schema, public contract packaging, and definitive command/query names remain open. FastAPI is a proposal based on Python affinity, not an accepted choice.

## Source

See sections 6 through 10 of [`Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx`](../Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx).
