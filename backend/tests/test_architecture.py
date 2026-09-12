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
            if set(module.casefold().split(".")) & FORBIDDEN_DOMAIN_LAYERS:
                violations.append(f"{domain_file.relative_to(SOURCE_ROOT)} imports {module}")

    assert not violations, "\n".join(violations)


def test_application_packages_do_not_import_outward_layers() -> None:
    violations: list[str] = []

    for application_file in CONTEXTS_ROOT.glob("*/application/**/*.py"):
        for module in _imported_modules(application_file):
            if set(module.casefold().split(".")) & FORBIDDEN_APPLICATION_LAYERS:
                violations.append(
                    f"{application_file.relative_to(SOURCE_ROOT)} imports {module}"
                )

    assert not violations, "\n".join(violations)


def test_context_interfaces_do_not_import_infrastructure() -> None:
    violations: list[str] = []

    for interface_file in CONTEXTS_ROOT.glob("*/interfaces/**/*.py"):
        for module in _imported_modules(interface_file):
            if "infrastructure" in module.casefold().split("."):
                violations.append(
                    f"{interface_file.relative_to(SOURCE_ROOT)} imports {module}"
                )

    assert not violations, "\n".join(violations)


def test_backend_source_does_not_reference_scientific_engine() -> None:
    references = [
        str(path.relative_to(SOURCE_ROOT))
        for path in SOURCE_ROOT.rglob("*.py")
        if "cropsuitelite" in path.read_text(encoding="utf-8").casefold()
    ]

    assert not references, "\n".join(references)
