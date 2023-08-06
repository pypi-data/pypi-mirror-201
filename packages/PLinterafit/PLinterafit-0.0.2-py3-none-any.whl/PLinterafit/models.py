# Authors: Viktor Bender and Bayarjargal N.Tugchin
# Date: 16/03/2023
# Last update: 01/04/2023

import numpy as np
from scipy.special import voigt_profile


def voigt_multifit_component(x: np.ndarray, median: float, amplitude: float, lorentzian_hwhm: float,
                             gaussian_hwhm: float) -> np.ndarray:
    """
    Returns the Voigt line shape at 'x' with median 'median', normalisation 'amplitude', Lorentzian component HWHM 'lorentzian_hwhm'
    and Gaussian component HWHM 'gaussian_hwhm'. Uses Voig profile from Python in-build library.
    
    
    Args:
        x : numpy.ndarray
            The x-coordinates at which to compute the Voigt line shape.
        median : float
            The median (center) of the Voigt line shape.
        amplitude : float
            The normalisation of the Voigt line shape.
        lorentzian_hwhm : float
            The half-width at half-maximum (HWHM) of the Lorentzian component of the Voigt line shape.
        gaussian_hwhm : float
            The half-width at half-maximum (HWHM) of the Gaussian component of the Voigt line shape.

    Returns:
        numpy.ndarray
            The Voigt line shape at 'x'.

    """
    return np.abs(amplitude) * np.abs(voigt_profile((x - np.abs(median)), np.abs(lorentzian_hwhm), np.abs(gaussian_hwhm)))


def one_voigt(x: np.ndarray, median: float, amplitude: float, lorentzian_hwhm: float,
              gaussian_hwhm: float, offset: float = 0) -> np.ndarray:
    """
    Returns the line shape of a single Voigt distribution at 'x'.
    
    Args:
        x : numpy.ndarray
            The x-coordinates at which to compute the Voigt line shape.
        median : float
            The median (center) of the Voigt line shape.
        amplitude : float
            The normalisation of the Voigt line shape.
        lorentzian_hwhm : float
            The half-width at half-maximum (HWHM) of the Lorentzian component of the Voigt line shape.
        gaussian_hwhm : float
            The half-width at half-maximum (HWHM) of the Gaussian component of the Voigt line shape.
        offset: float
            The offset value of the Voigt function. Defaults to 0.

    Returns:
        numpy.ndarray
            The Voigt line shape at 'x'.

    """
    return voigt_multifit_component(x, median, amplitude, lorentzian_hwhm, gaussian_hwhm) + np.abs(offset)

    
def five_voigt(x: np.ndarray, median1: float, amplitude1: float, lorentzian_hwhm1: float, gaussian_hwhm1: float,
               median2: float, amplitude2: float, lorentzian_hwhm2: float, gaussian_hwhm2: float,
               median3: float, amplitude3: float, lorentzian_hwhm3: float, gaussian_hwhm3: float,
               median4: float, amplitude4: float, lorentzian_hwhm4: float, gaussian_hwhm4: float,
               median5: float, amplitude5: float, lorentzian_hwhm5: float, gaussian_hwhm5: float, offset: float = 0) -> np.ndarray:

    """
    Return the line shape of five Voigt distributions at 'x'.
    
       
    Args:
        x : numpy.ndarray
            The x-coordinates at which to compute the Voigt line shape.
        median1-5: float
            The median (center) of respective Voigt line shape.
        amplitude1-5: float
            The normalisation of respective Voigt line shape.
        lorentzian_hwhm1-5: float
            The half-width at half-maximum (HWHM) of the Lorentzian component of respective Voigt line shape.
        gaussian_hwhm1-5: float
            The half-width at half-maximum (HWHM) of the Gaussian component of respective Voigt line shape.
        offset: float
            The offset value of the sum of five Voigt function. Defaults to 0.

    Returns:
        numpy.ndarray
            The line shape of five Voigt distributions at 'x'.

    """
    return voigt_multifit_component(x, median1, amplitude1, lorentzian_hwhm1, gaussian_hwhm1) + \
           voigt_multifit_component(x, median2, amplitude2, lorentzian_hwhm2, gaussian_hwhm2) + \
           voigt_multifit_component(x, median3, amplitude3, lorentzian_hwhm3, gaussian_hwhm3) + \
           voigt_multifit_component(x, median4, amplitude4, lorentzian_hwhm4, gaussian_hwhm4) + \
           voigt_multifit_component(x, median5, amplitude5, lorentzian_hwhm5, gaussian_hwhm5) + \
           np.abs(offset)

