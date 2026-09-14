---
type: "query"
date: "2026-09-14T01:48:51.598352+00:00"
question: "Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation"
contributor: "graphify"
outcome: "useful"
source_nodes: ["run_migrations_online()", "create_database()", "Settings", "PostgreSQL/PostGIS integration tests for Agroclimatic Evaluation.", "PostgreSQL/PostGIS integration tests for Environmental Information.", "Farm Management schema ownership"]
---

# Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation

## Answer

Expanded from original query via graph vocab: [database, url, test, postgre, sql, settings, create, schema, post, gis, migration, repositories]. Graphify located duplicated guards in the four PostgreSQL/PostGIS integration modules, run_migrations_online in backend/migrations/env.py, create_database in backend/src/via_backend/infrastructure/database.py, Settings in backend/src/via_backend/config.py, and schema/PostGIS ownership in ADR-011. The compatibility guard belongs in shared test support before Alembic and cleanup; application configuration and migrations remain unchanged.

## Outcome

- Signal: useful

## Source Nodes

- run_migrations_online()
- create_database()
- Settings
- PostgreSQL/PostGIS integration tests for Agroclimatic Evaluation.
- PostgreSQL/PostGIS integration tests for Environmental Information.
- Farm Management schema ownership