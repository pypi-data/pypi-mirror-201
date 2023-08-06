from collections.abc import Sequence
from typing import Union

import numpy as np
from skimage import exposure

List2F = Sequence[float, float, ...]

clahe = exposure.equalize_adapthist
"""Contrast limited adaptive histogram equalization (CLAHE).

See: `skimage.exposure.equalize_adapthist() <https://scikit-image.org/docs/stable/api/skimage.exposure.html#skimage.exposure.equalize_adapthist>`_
"""

clip = np.clip
"""Clip image values to a range."""


def stretch(image, a_min, a_max, **kwargs):
    """Linearly rescale the provided min/max range to the dynamic range of the
    image.
    """
    return exposure.rescale_intensity(image, in_range=(a_min, a_max), *kwargs)


def stretch_percentile(image, min_perc, max_perc, **kwargs):
    """Linearly rescale the provided percentile range to the dynamic range of
    the image.
    """
    min_val = np.percentile(image, min_perc)
    max_val = np.percentile(image, max_perc)
    return exposure.rescale_intensity(image, in_range=(min_val, max_val), *kwargs)


def stretch_binned_percentile(image, percent: Union[float, List2F, None] = None,
                              bins=256, **kwargs):
    """Alternative version of
    :func:`~educelab.imgproc.enhance.stretch_percentile` that uses percentiles
    calculated from intensity binning.
    """
    if percent is None:
        percent = (.35, .35)
    elif isinstance(percent, float):
        percent = (percent, percent)
    elif isinstance(percent, tuple):
        pass
    else:
        raise ValueError(
            f'unsupported type {type(percent)}, must be '
            f'[float, Sequence[float, float], None]')

    # calculate histogram
    hist, edges = np.histogram(image, bins=bins)

    # find the lower and upper bins which saturate clip_% pixels low and high
    threshold = int(image.size * percent[0] / 200.)
    c = (np.cumsum(hist) < threshold).argmin()
    threshold = int(image.size * percent[1] / 200.)
    d = bins - 1 - (np.cumsum(hist[::-1]) < threshold).argmin()

    # convert the bin to a low and high pixel value
    c = edges[0] + c * (edges[1] - edges[0])
    d = edges[0] + d * (edges[1] - edges[0])

    # rescale and return
    return exposure.rescale_intensity(image, in_range=(c, d), *kwargs)
