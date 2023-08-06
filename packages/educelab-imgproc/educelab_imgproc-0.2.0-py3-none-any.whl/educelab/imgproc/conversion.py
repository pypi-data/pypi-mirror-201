import numpy as np
from skimage import img_as_float32, img_as_ubyte, img_as_uint


def as_dtype(image, dtype) -> np.ndarray:
    """Convert an image to a specific fundamental dtype. Automatically performs
    dynamic range adjustment.

    :param image: Input image.
    :param dtype: Numpy dtype. Must be one of: :code:`np.uint8`,
           :code:`np.uint16`, :code:`np.float32`.
    :return: Converted image.
    """
    if dtype == np.uint8:
        image = np.clip(image, a_min=-1., a_max=1.)
        return img_as_ubyte(image)
    elif dtype == np.uint16:
        image = np.clip(image, a_min=-1., a_max=1.)
        return img_as_uint(image)
    elif dtype == np.float32:
        return img_as_float32(image)
