"""Water-regime scenarios owned by Agroclimatic Evaluation."""

from enum import StrEnum


class WaterRegime(StrEnum):
    """Scientific water-regime assumption used for one CropSuite execution."""

    RAINFED = "rainfed"
    IRRIGATED = "irrigated"
