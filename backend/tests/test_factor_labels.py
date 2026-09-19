from __future__ import annotations

import pytest

from via_backend.contexts.agroclimatic_evaluation.application.factor_labels import (
    factor_display_label,
)


@pytest.mark.parametrize(
    ("factor_code", "expected"),
    (
        ("temperature", "Temperatura"),
        ("precipitation", "Precipitación"),
        ("parameter_base_saturation", "Saturación de bases"),
        ("parameter_coarse_fragments", "Fragmentos gruesos"),
        ("parameter_gypsum", "Contenido de yeso"),
        ("parameter_ph", "pH del suelo"),
        ("parameter_salinity", "Salinidad del suelo"),
        ("parameter_texture", "Textura del suelo"),
        ("parameter_soil_organic_carbon", "Carbono orgánico del suelo"),
        ("parameter_sodicity", "Sodicidad del suelo"),
        ("parameter_soildepth", "Profundidad efectiva del suelo"),
        ("parameter_slope", "Pendiente del terreno"),
    ),
)
def test_factor_display_label_uses_spanish_application_labels(
    factor_code: str,
    expected: str,
) -> None:
    assert factor_display_label(factor_code, raw_label="raw") == expected


def test_factor_display_label_preserves_raw_label_for_unmapped_factor() -> None:
    assert (
        factor_display_label("crop_failure_frequency", raw_label="climate variability")
        == "climate variability"
    )
