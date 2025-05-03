from scipy.interpolate import splprep, splev
from numpy.fft import fft, ifft
import numpy as np


# from bezier import Curve
def b_splines(contours):
    smoothed_contours = []
    for contour in contours:
        x, y = contour[:, 0], contour[:, 1]
        tck, _ = splprep([x, y], s=5)
        new_points = splev(np.linspace(0, 1, 200), tck)
        smoothed_contours.append(np.vstack(new_points).T.astype(np.int32))
    return smoothed_contours


def fourier_smooth(contour, keep_fraction=0.1):
    z = contour[:, 0] + 1j * contour[:, 1]
    Z = fft(z)
    n = len(Z)
    Z[int(n * keep_fraction) :] = 0
    z_smooth = ifft(Z).real
    return np.column_stack((z_smooth.real, z_smooth.imag)).astype(np.int32)
