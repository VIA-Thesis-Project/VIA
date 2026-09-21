"""Lightweight dependency checks for the modular-monolith foundation."""

from __future__ import annotations

import ast
from pathlib import Path

SOURCE_ROOT = Path(__file__).parents[1] / "src" / "via_backend"
CONTEXTS_ROOT = SOURCE_ROOT / "contexts"
EXPECTED_CONTEXTS = {
    "identity_access",
    "farm_management",
    "environmental_information",
    "agroclimatic_evaluation",
    "decision_support",
}
EXPECTED_LAYERS = {"domain", "application", "infrastructure", "interfaces"}
FORBIDDEN_DOMAIN_LAYERS = {"application", "infrastructure", "interfaces"}
FORBIDDEN_APPLICATION_LAYERS = {"infrastructure", "interfaces"}
FORBIDDEN_DOMAIN_DEPENDENCIES = {
    "alembic",
    "fastapi",
    "geoalchemy2",
    "psycopg",
    "sqlalchemy",
}


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    modules: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                modules.add(node.module)
            else:
                modules.update(alias.name for alias in node.names)

    return modules


def test_expected_context_and_layer_packages_exist() -> None:
    assert {
        path.name
        for path in CONTEXTS_ROOT.iterdir()
        if path.is_dir() and not path.name.startswith("__")
    } == EXPECTED_CONTEXTS

    for context_name in EXPECTED_CONTEXTS:
        context_path = CONTEXTS_ROOT / context_name
        assert {
            path.name
            for path in context_path.iterdir()
            if path.is_dir() and not path.name.startswith("__")
        } == EXPECTED_LAYERS
        assert (context_path / "__init__.py").is_file()
        for layer_name in EXPECTED_LAYERS:
            assert (context_path / layer_name / "__init__.py").is_file()


def test_domain_packages_do_not_import_outward_layers() -> None:
    violations: list[str] = []

    for domain_file in CONTEXTS_ROOT.glob("*/domain/**/*.py"):
        for module in _imported_modules(domain_file):
            parts = set(module.casefold().split("."))
            if parts & (FORBIDDEN_DOMAIN_LAYERS | FORBIDDEN_DOMAIN_DEPENDENCIES):
                violations.append(f"{domain_file.relative_to(SOURCE_ROOT)} imports {module}")

    assert not violations, "\n".join(violations)


def test_application_packages_do_not_import_outward_layers() -> None:
    violations: list[str] = []

    for application_file in CONTEXTS_ROOT.glob("*/application/**/*.py"):
        for module in _imported_modules(application_file):
            parts = set(module.casefold().split("."))
            if parts & (FORBIDDEN_APPLICATION_LAYERS | FORBIDDEN_DOMAIN_DEPENDENCIES):
                violations.append(f"{application_file.relative_to(SOURCE_ROOT)} imports {module}")

    assert not violations, "\n".join(violations)


def test_context_interfaces_do_not_import_infrastructure() -> None:
    violations: list[str] = []

    for interface_file in CONTEXTS_ROOT.glob("*/interfaces/**/*.py"):
        for module in _imported_modules(interface_file):
            if "infrastructure" in module.casefold().split("."):
                violations.append(f"{interface_file.relative_to(SOURCE_ROOT)} imports {module}")

    assert not violations, "\n".join(violations)


def test_only_cropsuite_infrastructure_adapters_reference_scientific_engine() -> None:
    infrastructure = (
        SOURCE_ROOT
        / "contexts"
        / "agroclimatic_evaluation"
        / "infrastructure"
    )

    allowed = {
        infrastructure / "cropsuite_adapter.py",
        infrastructure / "cropsuite_comparison_adapter.py",
        SOURCE_ROOT / "worker.py",
    }

    violations = [
        str(path.relative_to(SOURCE_ROOT))
        for path in SOURCE_ROOT.rglob("*.py")
        if path not in allowed
        and "cropsuitelite" in path.read_text(encoding="utf-8").casefold()
    ]

    assert not violations, "\n".join(violations)

    assert "cropsuitelite" in (
        infrastructure / "cropsuite_adapter.py"
    ).read_text(encoding="utf-8").casefold()

    assert "cropsuitelite" in (
        infrastructure / "cropsuite_comparison_adapter.py"
    ).read_text(encoding="utf-8").casefold()


def test_farm_management_does_not_import_other_contexts() -> None:
    farm_management = CONTEXTS_ROOT / "farm_management"
    allowed_identity_contract = (
        "via_backend.contexts.identity_access.application.public"
    )
    violations: list[str] = []

    for source_file in farm_management.rglob("*.py"):
        for module in _imported_modules(source_file):
            parts = module.casefold().split(".")
            if "contexts" not in parts:
                continue
            context_index = parts.index("contexts") + 1
            if (
                context_index < len(parts)
                and parts[context_index] != "farm_management"
                and module != allowed_identity_contract
            ):
                violations.append(f"{source_file.relative_to(SOURCE_ROOT)} imports {module}")

    assert not violations, "\n".join(violations)


def test_environmental_information_does_not_import_other_contexts() -> None:
    environmental_information = CONTEXTS_ROOT / "environmental_information"
    allowed_identity_contract = "via_backend.contexts.identity_access.application.public"
    violations: list[str] = []

    for source_file in environmental_information.rglob("*.py"):
        for module in _imported_modules(source_file):
            parts = module.casefold().split(".")
            if "contexts" not in parts:
                continue
            context_index = parts.index("contexts") + 1
            if (
                context_index < len(parts)
                and parts[context_index] != "environmental_information"
                and module != allowed_identity_contract
            ):
                violations.append(f"{source_file.relative_to(SOURCE_ROOT)} imports {module}")

    assert not violations, "\n".join(violations)


def test_agroclimatic_evaluation_does_not_import_other_contexts() -> None:
    evaluation_context = CONTEXTS_ROOT / "agroclimatic_evaluation"
    allowed_public_imports = {
        (
            evaluation_context / "application" / "execution.py",
            "via_backend.contexts.environmental_information.application.public",
        ),
        (
            evaluation_context / "interfaces" / "http.py",
            "via_backend.contexts.identity_access.application.public",
        ),
        (
            evaluation_context / "interfaces" / "capabilities_http.py",
            "via_backend.contexts.identity_access.application.public",
        ),
    }
    violations: list[str] = []

    for source_file in evaluation_context.rglob("*.py"):
        for module in _imported_modules(source_file):
            parts = module.casefold().split(".")
            if "contexts" not in parts:
                continue
            context_index = parts.index("contexts") + 1
            if context_index < len(parts) and parts[context_index] != "agroclimatic_evaluation":
                if (source_file, module.casefold()) in allowed_public_imports:
                    continue
                violations.append(f"{source_file.relative_to(SOURCE_ROOT)} imports {module}")

    assert not violations, "\n".join(violations)


def test_postgresql_adapters_satisfy_repository_method_contracts() -> None:
    from via_backend.contexts.agroclimatic_evaluation.domain.repositories import (
        EvaluationRepository,
    )
    from via_backend.contexts.agroclimatic_evaluation.infrastructure import (
        PostgreSQLEvaluationRepository,
    )
    from via_backend.contexts.environmental_information.domain.repositories import (
        DatasetRepository,
        DatasetVersionRepository,
    )
    from via_backend.contexts.environmental_information.infrastructure import (
        PostgreSQLDatasetRepository,
        PostgreSQLDatasetVersionRepository,
    )
    from via_backend.contexts.farm_management.domain.repositories import (
        ParcelRepository,
        ProjectRepository,
    )
    from via_backend.contexts.farm_management.infrastructure import (
        PostgreSQLParcelRepository,
        PostgreSQLProjectRepository,
    )

    evaluation_methods = {
        name
        for name, value in vars(EvaluationRepository).items()
        if callable(value) and not name.startswith("_")
    }

    project_methods = {
        name
        for name, value in vars(ProjectRepository).items()
        if callable(value) and not name.startswith("_")
    }
    parcel_methods = {
        name
        for name, value in vars(ParcelRepository).items()
        if callable(value) and not name.startswith("_")
    }

    assert project_methods <= set(dir(PostgreSQLProjectRepository))
    assert parcel_methods <= set(dir(PostgreSQLParcelRepository))
    dataset_methods = {
        name
        for name, value in vars(DatasetRepository).items()
        if callable(value) and not name.startswith("_")
    }
    version_methods = {
        name
        for name, value in vars(DatasetVersionRepository).items()
        if callable(value) and not name.startswith("_")
    }

    assert dataset_methods <= set(dir(PostgreSQLDatasetRepository))
    assert version_methods <= set(dir(PostgreSQLDatasetVersionRepository))
    assert evaluation_methods <= set(dir(PostgreSQLEvaluationRepository))


def test_worker_application_code_does_not_import_cropsuite_adapter() -> None:
    worker_application = CONTEXTS_ROOT / "agroclimatic_evaluation" / "application" / "worker.py"

    assert "cropsuiteadapter" not in worker_application.read_text(encoding="utf-8").casefold()


def test_worker_operations_application_code_stays_persistence_agnostic() -> None:
    application = CONTEXTS_ROOT / "agroclimatic_evaluation" / "application"
    for filename in ("worker.py", "recovery.py"):
        modules = _imported_modules(application / filename)
        assert all("sqlalchemy" not in module.casefold() for module in modules)
        assert all("postgresql" not in module.casefold() for module in modules)


def test_evaluation_domain_does_not_import_worker_process_controls() -> None:
    domain = CONTEXTS_ROOT / "agroclimatic_evaluation" / "domain"
    forbidden = {"signal", "threading", "logging"}
    violations = [
        f"{path.name}: {module}"
        for path in domain.glob("*.py")
        for module in _imported_modules(path)
        if module.casefold().split(".")[0] in forbidden
    ]
    source = "\n".join(path.read_text(encoding="utf-8") for path in domain.glob("*.py"))

    assert not violations, "\n".join(violations)
    assert "WorkerSettings" not in source


def test_other_contexts_only_use_identity_access_public_contract() -> None:
    allowed_module = "via_backend.contexts.identity_access.application.public"
    violations: list[str] = []

    for context_path in CONTEXTS_ROOT.iterdir():
        if not context_path.is_dir() or context_path.name == "identity_access":
            continue
        for source_file in context_path.rglob("*.py"):
            for module in _imported_modules(source_file):
                parts = module.casefold().split(".")
                if "identity_access" not in parts:
                    continue
                if module != allowed_module:
                    violations.append(f"{source_file.relative_to(SOURCE_ROOT)} imports {module}")

    assert not violations, "\n".join(violations)


def test_identity_access_public_contract_does_not_expose_infrastructure() -> None:
    public_contract = CONTEXTS_ROOT / "identity_access" / "application" / "public.py"
    modules = _imported_modules(public_contract)

    assert all("infrastructure" not in module.casefold().split(".") for module in modules)
    assert all("interfaces" not in module.casefold().split(".") for module in modules)


def test_evaluation_query_path_does_not_reference_engine_or_worker_control() -> None:
    application = CONTEXTS_ROOT / "agroclimatic_evaluation" / "application"
    query_files = [
        application / "queries.py",
        application / "read_models.py",
        application / "public.py",
        application / "service.py",
    ]

    forbidden = {
        "cropsuiteadapter",
        "icropsuitabilityengine",
        "listevaluationsqueued",
        "list_queued_ids",
        "worker",
    }
    violations = [
        f"{path.name}: {term}"
        for path in query_files
        for term in forbidden
        if term in path.read_text(encoding="utf-8").casefold()
    ]

    assert not violations, "\n".join(violations)


def test_evaluation_http_read_resources_do_not_expose_persistence_types() -> None:
    http = CONTEXTS_ROOT / "agroclimatic_evaluation" / "interfaces" / "http.py"
    modules = _imported_modules(http)

    assert all("infrastructure" not in module.casefold() for module in modules)
    assert all("orm" not in module.casefold() for module in modules)
    assert all("sqlalchemy" not in module.casefold() for module in modules)
    assert "cropsuiteadapter" not in http.read_text(encoding="utf-8").casefold()


def test_finalized_result_public_contract_has_no_internal_storage_dependency() -> None:
    public_contract = CONTEXTS_ROOT / "agroclimatic_evaluation" / "application" / "public.py"
    modules = _imported_modules(public_contract)
    source = public_contract.read_text(encoding="utf-8").casefold()

    assert all("repositories" not in module.casefold() for module in modules)
    assert all("infrastructure" not in module.casefold() for module in modules)
    assert all("orm" not in module.casefold() for module in modules)
    assert "evaluationrepository" not in source
    assert "postgresqlevaluationrepository" not in source


def test_environmental_information_public_contract_uses_only_stdlib_imports() -> None:
    public_contract = CONTEXTS_ROOT / "environmental_information" / "application" / "public.py"
    modules = _imported_modules(public_contract)
    allowed_modules = {"__future__", "dataclasses", "datetime", "typing", "uuid"}

    unexpected_modules = modules - allowed_modules

    assert not unexpected_modules, "\n".join(sorted(unexpected_modules))

def test_decision_support_does_not_read_evaluation_internals() -> None:
    decision_support = CONTEXTS_ROOT / "decision_support"
    forbidden = {
        "evaluationrepository",
        "postgresqlevaluationrepository",
        "evaluationrecord",
        "cropoutcomerecord",
        "agroclimatic_evaluation.infrastructure",
    }
    violations = [
        f"{path.relative_to(SOURCE_ROOT)}: {term}"
        for path in decision_support.rglob("*.py")
        for term in forbidden
        if term in path.read_text(encoding="utf-8").casefold()
    ]

    assert not violations, "\n".join(violations)


def test_decision_support_domain_does_not_depend_on_agroclimatic_evaluation() -> None:
    decision_support_domain = CONTEXTS_ROOT / "decision_support" / "domain"
    violations = [
        f"{path.relative_to(SOURCE_ROOT)} imports {module}"
        for path in decision_support_domain.rglob("*.py")
        for module in _imported_modules(path)
        if "agroclimatic_evaluation" in module.casefold().split(".")
    ]

    assert not violations, "\n".join(violations)


def test_decision_support_application_uses_only_evaluation_public_contract() -> None:
    decision_support_application = CONTEXTS_ROOT / "decision_support" / "application"
    allowed_module = (
        "via_backend.contexts.agroclimatic_evaluation.application.public"
    )
    violations = [
        f"{path.relative_to(SOURCE_ROOT)} imports {module}"
        for path in decision_support_application.rglob("*.py")
        for module in _imported_modules(path)
        if "agroclimatic_evaluation" in module.casefold().split(".")
        and module != allowed_module
    ]

    assert not violations, "\n".join(violations)
