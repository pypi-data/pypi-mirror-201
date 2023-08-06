# Authors: Viktor Bender and Bayarjargal N.Tugchin
# Date: 16/03/2023
# Last update: 01/04/2023

from PLinterafit.models import *
from PLinterafit.dataPreparation import *
from PLinterafit.plotting import *
import matplotlib.pyplot as plt
from scipy.optimize import leastsq, curve_fit
import scipy.stats as stats
from matplotlib.widgets import Slider, Button
import scipy.integrate as integrate
from matplotlib.ticker import FixedLocator


hc = constants.physical_constants['Planck constant in eV s'][0] * \
     constants.physical_constants['speed of light in vacuum'][0] * 1e9

def do_statistics(func, eV, observed, seed, mode, My_maxfav):
    
    """
    Performs statistical analysis on a given data set using the specified function and the mode of noise distribution.

    Args:
        func: str
            A callable function representing the fitting model.
        eV: np.array
            A numpy array containing the x-values of the data set.
        observed: np.array
            A numpy array containing the y-values of the observed data set.
        seed: list
            A list of four float values representing the seed values for the Voigt profile.
        mode: str
            A string specifying the mode of the underlying noise distribution of the data.
        My_maxfav: int
            An integer representing the maximum number of function evaluations for the fitting routine.

    Returns:
        tuple: A tuple containing the chi-squared test statistic and p-value.

    Raises:
        ValueError: If the mode of the underlying noise distribution neither "poisson" nor "gauss".
    """
    
    if mode == "poisson":
        popt, pcov = curve_fit(func, eV, observed, sigma=np.sqrt(observed), p0=[*seed], absolute_sigma=True, maxfev=My_maxfav)
    elif mode == "gauss":
        popt, pcov = curve_fit(func, eV, observed, p0=[*seed], maxfev=My_maxfav)
        err = np.ones(len(observed)) * np.std(observed - func(eV, *popt))
        popt, pcov = curve_fit(func, eV, observed, sigma=err, p0=[*seed], absolute_sigma=True, maxfev=My_maxfav)
    else:
        raise ValueError('You need to specify a valid mode in fitting: poisson or gauss')
    expected = func(eV, *popt)

    expected, uncertainty, popt, popt_std, residuals = prepare_data_for_stat_test(observed, expected, popt, pcov, mode, func, eV)
    ndof = getNDOF(observed, popt)
    chi2, p_value = compute_chisquare(observed=observed, expected=expected, uncertainty=uncertainty, ndof=ndof)
    
    return popt, popt_std, expected, uncertainty, residuals, chi2, p_value, ndof 

def compute_chisquare(observed: np.ndarray, expected: np.ndarray, uncertainty: np.ndarray, ndof: float):
    """
    Calculates the chi-squared test statistic and p-value given observed and expected values,
    their uncertainties, and the number of degrees of freedom.

    Args:
        observed: array
            Observed values.
        expected: array
            Expected values.
        uncertainty: array
            Uncertainties of observed values.
        ndof: float
            Degrees of freedom.

    Returns: tuple
        A tuple containing the chi-squared test statistic and p-value.

    Raises:
        ValueError: If the shapes of the input arrays are not compatible.
    """
    observed = np.asarray(observed)
    expected = np.asarray(expected)
    uncertainty = np.asarray(uncertainty)
    if observed.shape != expected.shape or observed.shape != uncertainty.shape:
        raise ValueError("Shapes of observed, expected, and uncertainty arrays are not compatible.")
    chi2 = np.sum(((observed - expected) / uncertainty) ** 2)
    p_value = 1 - stats.chi2.cdf(chi2, ndof)
    return chi2, p_value


def getNDOF(data: np.ndarray, popt: np.ndarray):
    """
    Returns the number of degrees of freedom given a data array and a parameter array.

    Args:
        data: array 
            Data array.
        popt: array 
            Array of fitted parameter values.

    Returns: float
        Degrees of freedom.
        
    Raises:
        ValueError: If the shapes of the input arrays are not compatible.

    """
    
    # data = np.asarray(data)
    # popt = np.asarray(popt)
    # if data.ndim != 1 or popt.ndim != 1 or data.shape != popt.shape:
    #     raise ValueError("Shapes of data and popt arrays are not compatible.")
        
        
    return data.size - popt.size - 1
