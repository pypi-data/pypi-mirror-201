# Authors: Viktor Bender and Bayarjargal N.Tugchin
# Date: 16/03/2023
# Last update: 01/04/2023

from PLinterafit.dataPreparation import *
from PLinterafit.statistics import *
from PLinterafit.fitting import *
from PLinterafit.plotting import *
import scipy.integrate as integrate
import numpy
import matplotlib.pyplot as plt
from PLinterafit.models import *

def run_one_voigt_fitting():
    
    """
    Performs a Voigt fitting on photoluminescence spectral data.

    Returns:
        int: 0 on successful completion of function.
    """

    # Importing data and preparing the data for analysis
    # Data has the first column as wavelengths in nanometers and the second column as photon counts
    data1 = load_data('example_data/ExampleData_monolayerMoS2onSi02.asc', 0, 1)
    data1 = get_fit_data(data1, 1.5, 2.15)
    plotData1 = data1
    
    # Example of calling fit_one_voigt function
    # We pass the data, initial values for the Voigt function, and the underlying noise distribution type
    fit_one_voigt(plotData1, median=1.85, amplitude=10, lorentzian_hwhm=.001, gaussian_hwhm=.035,
                              offset=26, mode="poisson")
    
 

    return 0

def run_five_voigt_fitting():
    """
    Performs five Voigt functions fitting on photoluminescence spectral data.

    Returns:
        int: 0 on successful completion of function.
    """
    
    # Importing data and preparing the data for analysis
    # Data has the first column as wavelengths in nanometers and the second column as photon counts
    data1 = load_data('example_data/ExampleData_monolayerMoS2onSi02.asc', 0, 1)
    data1 = get_fit_data(data1, 1.5, 2.15)
    plotData1 = data1
    

    # Example of calling fit_five_voigts function
    # We pass the data, initial values for each Voigt function, and the underlying noise distribution type
    fit_five_voigts(plotData1, median1=2.033, amplitude1=10, lorentzian_hwhm1=.001, gaussian_hwhm1=.035, 
                              median2=1.89, amplitude2=18, lorentzian_hwhm2=.001, gaussian_hwhm2=.03,
                              median3=1.85, amplitude3=180, lorentzian_hwhm3=.0015, gaussian_hwhm3=.053, 
                              median4=1.81, amplitude4=1, lorentzian_hwhm4=5.56e-05, gaussian_hwhm4=.024,
                              median5=1.63, amplitude5=4.2, lorentzian_hwhm5=.000007, gaussian_hwhm5=.036, 
                              offset=26, mode="poisson")



    return 0