"""Human-readable labels for stable crop identifiers."""


CROP_DISPLAY_LABELS_ES: dict[str, str] = {
    "maize": "Maíz",
    "sugarcane": "Caña de azúcar",
    "avocado": "Palta",
    "asparagus": "Espárrago",
    "mango": "Mango",
    "citrus": "Cítricos",
    "strawberry": "Fresa",
}


def crop_display_label(crop_id: str, *, raw_label: str | None = None) -> str:
    """Return the Spanish display label while preserving catalog labels as fallback."""
    return CROP_DISPLAY_LABELS_ES.get(crop_id, raw_label or crop_id)
