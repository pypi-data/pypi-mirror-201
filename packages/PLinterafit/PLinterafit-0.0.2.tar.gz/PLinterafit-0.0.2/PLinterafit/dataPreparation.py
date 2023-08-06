# Authors: Viktor Bender and Bayarjargal N.Tugchin
# Date: 16/03/2023
# Last update: 01/04/2023

import csv
import numpy as np
import scipy.constants as constants
import matplotlib.pyplot as plt
import math
from matplotlib.widgets import Slider, Button
from PLinterafit.models import *

hc = constants.physical_constants['Planck constant in eV s'][0] * \
     constants.physical_constants['speed of light in vacuum'][0] * 1e9


def load_CSV_data(datafile: str) -> np.ndarray:
    """
    Load CSV data and return numpy array.
    
    Args:
        datafile: str
            File location is given as string.
        
    Returns:
        data: array
            Data array loaded from the file location.
        
    """
    file_rows = []
    with open(datafile) as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            file_rows.append(row)

    results = np.zeros((len(file_rows), 2))
    for k, row in enumerate(file_rows):
        results[k, 0] = float(row[0])
        results[k, 1] = float(row[1])

    results = np.flip(results, axis=0)
    return results

def add_photon_energy(data: np.ndarray) -> np.ndarray:
    """
    Add photon energy computed from vacuum wavelength.
    
    Args:
        data: array
            Data array to be processed.
        
    Returns:
        data: array
            Data array with an additional dimension as photon energy. 
    """
    results = np.empty((data.shape[0], 3))
    results[:, 0] = data[:, 0]
    results[:, 1] = hc / data[:, 0]
    results[:, 2] = data[:, 1]
    return results


def subtract_background(data: np.ndarray, background: float) -> np.ndarray:
    """
    Subtract background from data.
    
    Args:
        data: array
            Data array to be processed.
        background: float
            Background to be removed.
        
    Returns:
        data: array
            Background subtracted data array.
        
    """
    data[:, 2] -= background
    return data

def normalise_data(data: np.ndarray, factor: float) -> np.ndarray:
    """
    Normalise data.
    
    Args:
        data: array
            Data array to be normalized.
        factor: float
            Normalization factor.
        
    Returns:
        data: array
            Normalized data array.
        
    """
    data[:, 2] *= factor
    return data

def load_data(filepath: str, background: float, normalisation: float) -> np.ndarray:
    """
    Load data files.
    
    Args:
        filepath: str
            Filepath given as a string.
        background: float
            Background level to be removed from the data.
        normalisation: float
            Value by which the data is normalized with.
        
    Returns:
        data: array
            Processed data array: renormalized, background removed, new dimension is added as photon energy.

    """
    data = load_CSV_data(filepath)
    data = add_photon_energy(data)
    data = subtract_background(data, background)
    data = normalise_data(data, normalisation)
    return data

def get_fit_data(data: np.ndarray, lower_cutoff: float, upper_cutoff: float) -> np.ndarray:
    """
    Return data within the interest range bound by lower_cutoff and upper_cutoff.
    
    Args:
        data: array
            Data array of interest.
        lower_cutoff: float
            Lower cutoff range
        upper_cutoff: float
            Upper cutoff range
        
    Returns:
        data: array
            Data array within the selected cutoff range.

    """
    
    
    min_idx = np.argmin(abs(data[:, 1] - lower_cutoff))
    max_idx = np.argmin(abs(data[:, 1] - upper_cutoff))
    return data[min_idx:max_idx, :]

def order_of_magnitude(number: float) -> int:
    """
    Returns the order of magnitude of a given number.
    
    Args:
        number: float
            The float value.

    Returns:
        integer: 
            The order of magnituge.
    """
    
    return math.floor(math.log10(number))


def truncate(number: float, decimals: int = 0) -> float:
    """
    Truncates a float value to a specific number of decimal places.

    Args:
        number: float
            The float value to truncate.
        decimals: int, optional
            The number of decimal places to keep. Defaults to 0.

    Returns:
        float: 
            The truncated float value.

    Raises:
        TypeError: 
            If the decimals argument is not an integer.
        ValueError: 
            If the decimals argument is negative.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimals argument must be an integer.")
    elif decimals < 0:
        raise ValueError("decimals argument must be a non-negative integer.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor

def prepare_data_for_stat_test(observed: np.ndarray, expected: np.ndarray, popt: np.ndarray, pcov: np.ndarray, mode: str, function_name, eV: np.ndarray):
    """
    Prepare data for statistical test by normalizing expected counts, calculating uncertainties,
    and correcting parameters.

    Args:
        observed: array 
            Observed counts.
        expected: array
            Expected counts.
        popt: array
            Best-fit parameters.
        pcov: array
            Covariance matrix of popt.
        mode: str
            "poisson" or "gauss" mode.
        func: function
            Model function to use.
        eV: array
            Energy values.

    Returns:
        expected: array
            Normalized expected counts.
        uncertainty: array
            Uncertainties.
        popt: array
            Corrected best-fit parameters.
        popt_std: array
            Corrected standard deviations of popt.
        residuals: array
            Residuals.
    
    
    Raises:
        ValueError: 
            If the mode is invalid.
            If the function_name is invalid.
            If the tolerance level has not reached the value atol.

    """
    normfactor = (sum(observed) / sum(expected))
    expected *= normfactor
    popt_std = np.sqrt(np.diag(pcov))
    residuals = observed - expected

    if mode == "poisson":
        uncertainty = np.sqrt(expected)
    elif mode == "gauss":
        uncertainty = np.ones(len(residuals)) * np.std(residuals)
    else:
        raise ValueError('Invalid mode: must be "poisson" or "gauss"')

    idx_to_correct = []
    if function_name == one_voigt:
        idx_to_correct = [1, -1]
    elif function_name == five_voigt:
        idx_to_correct = [1, 5, 9, 13, 17, -1]
    else:
        raise ValueError('Invalid model function')

    popt[idx_to_correct] *= normfactor
    popt_std[idx_to_correct] *= normfactor

    if np.allclose(function_name(eV, *popt), expected, atol=1e-20):  
        print('prepare_data_for_stat_test: no errors')
    else:
        raise ValueError('Incorrect parameter correction in prepare_data_for_stat_test')

    return expected, uncertainty, popt, popt_std, residuals
