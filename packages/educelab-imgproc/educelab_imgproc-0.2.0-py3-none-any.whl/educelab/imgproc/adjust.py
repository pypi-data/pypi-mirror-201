import numpy as np


def exposure(image, val):
    """Increase image exposure.

    :param image: Input image.
    :param val: Exposure adjustment factor (+/-).
    :return: Exposure adjusted image.
    """
    return image * 2 ** val


def shadows(image, val):
    """Image shadow adjustment.

    Adapted from an implementation by
    `HViktorTsoi <https://gist.github.com/HViktorTsoi/8e8b0468a9fb07842669aa368382a7df>`_.

    :param image: Input image.
    :param val: Shadow adjustment factor (+/-).
    :return: Exposure adjusted image.
    """
    shadow_val = 1. + val / 100. * 2
    shadow_mid = 3. / 10.
    shadow_region = np.clip(1. - image / shadow_mid, 0, 1)
    shadow_region[np.where(image >= shadow_mid)] = 0
    return (1 - shadow_region) * image + shadow_region * (
            1 - np.power(1 - image, shadow_val))
