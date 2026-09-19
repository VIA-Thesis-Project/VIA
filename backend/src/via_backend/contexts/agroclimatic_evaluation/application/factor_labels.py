"""Human-readable labels for stable agroclimatic factor codes."""


FACTOR_DISPLAY_LABELS_ES: dict[str, str] = {
    "temperature": "Temperatura",
    "precipitation": "Precipitación",
    "parameter_base_saturation": "Saturación de bases",
    "parameter_coarse_fragments": "Fragmentos gruesos",
    "parameter_gypsum": "Contenido de yeso",
    "parameter_ph": "pH del suelo",
    "parameter_salinity": "Salinidad del suelo",
    "parameter_texture": "Textura del suelo",
    "parameter_soil_organic_carbon": "Carbono orgánico del suelo",
    "parameter_sodicity": "Sodicidad del suelo",
    "parameter_soildepth": "Profundidad efectiva del suelo",
    "parameter_slope": "Pendiente del terreno",
}


def factor_display_label(factor_code: str, *, raw_label: str | None = None) -> str:
    """Return the Spanish display label while preserving raw labels as fallback."""
    return FACTOR_DISPLAY_LABELS_ES.get(factor_code, raw_label or factor_code)
