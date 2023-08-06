from functools import partial

import numpy as np
from skimage import exposure


def flatfield_correction(image, lf, df):
    """Apply `flatfield correction <https://en.wikipedia.org/wiki/Flat-field_correction>`_
    to an image.

    :param image: Input image.
    :param lf: Light-field image.
    :param df: Dark-field image.
    :return: Flatfield-corrected image.
    """
    fd_diff = lf - df
    return (image - df) * np.mean(fd_diff) / fd_diff


gamma_correction = exposure.adjust_gamma
"""Apply gamma correction to an image.

See: `skimage.exposure.adjust_gamma() <https://scikit-image.org/docs/stable/api/skimage.exposure.html#skimage.exposure.adjust_gamma>`_
"""

normalize = partial(exposure.rescale_intensity, out_range=(0., 1.))
"""Rescale an image's effective dynamic range (min and max values) to the 
range [0, 1]."""
