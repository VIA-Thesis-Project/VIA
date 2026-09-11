"""Spatial operations that preserve missing coverage instead of creating zeros."""
import numpy as np
from scipy.ndimage import distance_transform_edt
from skimage.transform import resize


def resample_valid(values, shape, valid, order=1):
    """Temporarily nearest-fill gaps, resample, then restore the coverage mask."""
    values = np.asarray(values, dtype=float)
    valid = np.asarray(valid, dtype=bool) & np.isfinite(values)
    shape = tuple(shape)
    if not valid.any():
        return np.full(shape, np.nan)
    if values.shape == shape:
        return np.where(valid, values, np.nan)
    indices = distance_transform_edt(~valid, return_distances=False, return_indices=True)
    filled = values[tuple(indices)]
    result = resize(filled, shape, order=order, mode='edge',
                    anti_aliasing=False, preserve_range=True)
    coverage = resize(valid, shape, order=0, mode='edge',
                      anti_aliasing=False, preserve_range=True).astype(bool)
    return np.where(coverage, result, np.nan)


def climate_coverage(temperature, precipitation, land, irrigated=False):
    """Require complete daily coverage; missing observations are not unsuitable days."""
    valid = (np.asarray(land) == 1)
    valid = valid & (np.isfinite(temperature) & (temperature != -32767)).all(axis=-1)
    if not irrigated:
        valid &= (np.isfinite(precipitation) & (precipitation >= 0)).all(axis=-1)
    return valid


def covered_gradient(values, spacing, axis):
    """Central differences inside coverage, one-sided at its boundary.

    An axis with no valid immediate neighbour uses a constant extension (0).
    An entirely isolated valid pixel has no slope estimate (handled by caller).
    """
    valid = np.isfinite(values)
    prev = np.roll(values, 1, axis=axis)
    following = np.roll(values, -1, axis=axis)
    has_prev = np.roll(valid, 1, axis=axis)
    has_next = np.roll(valid, -1, axis=axis)
    edge = [slice(None)] * values.ndim
    edge[axis] = 0
    has_prev[tuple(edge)] = False
    edge[axis] = -1
    has_next[tuple(edge)] = False
    result = np.zeros_like(values, dtype=float)
    both = valid & has_prev & has_next
    forward = valid & ~has_prev & has_next
    backward = valid & has_prev & ~has_next
    result[both] = (following[both] - prev[both]) / (2 * spacing)
    result[forward] = (following[forward] - values[forward]) / spacing
    result[backward] = (values[backward] - prev[backward]) / spacing
    result[~valid] = np.nan
    return result, valid & (has_prev | has_next)
