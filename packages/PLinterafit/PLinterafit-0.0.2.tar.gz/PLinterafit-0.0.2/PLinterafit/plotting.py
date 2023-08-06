# Authors: Viktor Bender and Bayarjargal N.Tugchin
# Date: 16/03/2023
# Last update: 01/04/2023

from PLinterafit.models import *
from PLinterafit.dataPreparation import *
import numpy
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from matplotlib.ticker import FixedLocator

def plot_data_and_one_voigt_seed_function(data: np.array, func: callable, seed: tuple) -> object:
    """
    Plot the experimental data and the Voigt seed function.

    Args:
        data: 2D array of floats
            Experimental data, with columns for the x-values and y-values
        func: callable
            Function to plot, representing the Voigt seed function
        seed: tuple
            Initial guess for the parameters of the Voigt seed function
        
    Returns: 
        tuple
            A tuple containing the figure and axis objects.
    """
    eV = data[:, 1]   # Photon energy
    observed = data[:, 2] # Counts
    
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    cm = 1 / 2.54
    fig, ax = plt.subplots(figsize=(15 * cm, 15 * cm))
    ax.scatter(eV, observed, marker=".", s=0.5, label="Data")
    ax.plot(eV, func(eV, *seed), c="k", linestyle="-", label="Voigt Seed Function")
    ax.plot(eV, voigt_multifit_component(eV, *seed[0:4]), color='r', linestyle='-', label=truncate(seed[0], 3))
    ax.set_xlabel(r"\textrm{Photon Energy [eV]}")
    ax.set_ylabel(r"\textrm{Photon Count}")
    ax.grid(True)
    ax.legend()
    
    return fig, ax
    
def plot_fitted_results_one_voigt(eV: np.array, observed: np.array, expected: np.array, uncertainty: np.array, popt: np.array, popt_std: np.array, residuals: np.array, chi2: float, p_value: float, ndof: float,)-> None:
    
    """
    Plot the experimental data, the fitted Voigt function, the total fit, and the residual differences between the observed and fitted results.

    Args:
        eV : numpy array of floats
            The photon energies in eV at which the data was collected.
        observed : numpy array of floats
            The observed photon counts for each energy.
        expected : numpy array of floats
            The expected photon counts calculated from the fitted Voigt functions.
        uncertainty : numpy array of floats
            The uncertainties in the observed photon counts.
        popt : numpy array of floats
            The best-fit parameters for the Voigt functions.
        popt_std : numpy array of floats
            The standard deviations of the best-fit parameters.
        residuals : numpy array of floats
            The difference between the observed and expected photon counts.
        chi2 : float
            The chi-squared value of the fit.
        p_value : float
            The p-value for the fit.
        ndof : float
            The number of degrees of freedom of the fit.

    Returns:
        None
            The function saves a plot of the fitted results and residuals to a file.
    
    """
    
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    cm = 1 / 2.54
    
    fig1, ax1 = plt.subplots(2, 1, figsize=(15 * cm, 15 * cm))
    ax1[0].errorbar(eV, observed, uncertainty, marker=".", label='Data', linestyle="None", markersize=3, alpha=.5)
    ax1[0].plot(eV, expected, c='r', linestyle='-', label='Voigt Fit Function\n $\chi^2$/ndof: '+str(truncate(chi2/ndof,3))+'\n p-value: '+str(truncate(p_value, 3)))
    ax1[0].set_xlabel(r'\textrm{Photon Energy [eV]}')
    ax1[0].set_ylabel(r'\textrm{Photon Count}')
    ax1[0].grid(True)
    ax1[0].legend()

    ax1[1].errorbar(eV, residuals, uncertainty, marker=".", label='Data', linestyle="None", markersize=3, alpha=.5)
    ax1[1].plot([np.min(eV), np.max(eV)], [0, 0], c='r', linestyle='-')
    ax1[1].set_xlabel(r'\textrm{Photon Energy [eV]}')
    ax1[1].set_ylabel(r'\textrm{Residuals}')
    ax1[1].grid(True)
    ax1[1].legend()

    secAx = ax1[1].twiny()

    secAx.set_frame_on(True)
    secAx.patch.set_visible(False)
    secAx.xaxis.set_ticks_position('bottom')
    secAx.xaxis.set_label_position('bottom')
    secAx.spines['bottom'].set_position(('outward', 30))
    secAx.plot(eV, residuals, alpha=0)

    E_ticks = secAx.get_xticks()
    wl_ticks = [hc / n for n in E_ticks]
    wl_ticks = [truncate(n, 2) for n in wl_ticks]
    secAx.set_xticklabels(wl_ticks)

    secAx.set_xlabel(r'\textrm{Wavelength [nm]}')
    fig1.tight_layout()
    plt.show()
    fig1.savefig("figures/fit_results_1_voigts.svg", bbox_inches='tight', dpi=300)

def plot_data_and_five_voigt_seed_function(data: np.ndarray, func: callable, seed: tuple) -> object:
    """
    Plot the experimental data, the Voigt seed functions, and the total sum of them.

    Args:
        data: 2D array of floats
            Experimental data, with columns for the x-values and y-values
        func: callable
            Function to plot, representing the Voigt seed function
        seed: tuple
            Initial guess for the parameters of the Voigt seed function
            
    Returns: 
        tuple
            A tuple containing the figure and axis objects.
    
    """
    eV = data[:, 1]   # Photon energy
    observed = data[:, 2] # Counts
    
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    cm = 1 / 2.54
    fig, ax = plt.subplots(1, 1, figsize=(15 * cm, 15 * cm))
    ax.scatter(eV, observed, marker=".", s=.5, label='Data')
    ax.plot(eV, func(eV, *seed), c='k', linestyle='-', label='Voigt Seed Function')
    ax.plot(eV, voigt_multifit_component(eV, *seed[0:4]), color='r', linestyle='-', label=r"Voigt 1: "+str(truncate(seed[0], 3)))
    ax.plot(eV, voigt_multifit_component(eV, *seed[4:8]), color='g', linestyle='-', label=r"Voigt 2: "+str(truncate(seed[4], 3)))
    ax.plot(eV, voigt_multifit_component(eV, *seed[8:12]), color='orange', linestyle='-', label=r"Voigt 3: "+str(truncate(seed[8], 3)))
    ax.plot(eV, voigt_multifit_component(eV, *seed[12:16]), color='purple', linestyle='-', label=r"Voigt 4: "+str(truncate(seed[12], 3)))
    ax.plot(eV, voigt_multifit_component(eV, *seed[16:20]), color='b', linestyle='-', label=r"Voigt 5: "+str(truncate(seed[16], 3)))
    ax.set_xlabel(r'\textrm{Photon Energy [eV]}')
    ax.set_ylabel(r'\textrm{Photon Count}')
    ax.grid(True)
    ax.legend() 
    
    return fig, ax

def plot_fitted_results_five_voigt(eV: np.array, observed: np.array, expected: np.array, uncertainty: np.array, popt: np.array, popt_std: np.array, residuals: np.array, chi2: float, p_value: float, ndof: float,)-> None:
    
    """
    Plot the experimental data, the fitted Voigt functions, the total sum of Voigt fit, and the residual differences between the observed and fitted results.

    Args:
        eV : numpy array of floats
            The photon energies in eV at which the data was collected.
        observed : numpy array of floats
            The observed photon counts for each energy.
        expected : numpy array of floats
            The expected photon counts calculated from the fitted Voigt functions.
        uncertainty : numpy array of floats
            The uncertainties in the observed photon counts.
        popt : numpy array of floats
            The best-fit parameters for the Voigt functions.
        popt_std : numpy array of floats
            The standard deviations of the best-fit parameters.
        residuals : numpy array of floats
            The difference between the observed and expected photon counts.
        chi2 : float
            The chi-squared value of the fit.
        p_value : float
            The p-value for the fit.
        ndof : float
            The number of degrees of freedom of the fit.

    Returns:
        None
            The function saves a plot of the fitted results and residuals to a file.
    
    """

    
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    cm = 1 / 2.54
    fig1, ax1 = plt.subplots(2, 1, figsize=(15 * cm, 15 * cm))
    ax1[0].errorbar(eV, observed, uncertainty, marker=".", label='Data', linestyle="None", markersize=3, alpha=.5)
    ax1[0].plot(eV, expected, c='r', linestyle='-', label='Voigt Fit Function\n $\chi^2$/ndof: '+str(truncate(chi2/ndof,3))+'\n p-value: '+str(truncate(p_value, 3)))
    ax1[0].fill_between(eV, voigt_multifit_component(eV, *popt[0:4]), alpha=.3, color='r', linestyle='-', label=r"$\omega_1$: "+str(truncate(popt[0], 3)))
    ax1[0].fill_between(eV, voigt_multifit_component(eV, *popt[4:8]), alpha=.3, color='g', linestyle='-', label=r"$\omega_2$: "+str(truncate(popt[4], 3))+r" $\Delta: $"+str(truncate(popt[0] - popt[4], 3)))
    ax1[0].fill_between(eV, voigt_multifit_component(eV, *popt[8:12]), alpha=.3, color='orange', linestyle='-', label=r"$\omega_3$: "+str(truncate(popt[8], 3))+r" $\Delta: $"+str(truncate(popt[4] - popt[8], 3)))
    ax1[0].fill_between(eV, voigt_multifit_component(eV, *popt[12:16]), alpha=.3, color='purple', linestyle='-', label=r"$\omega_4$: "+str(truncate(popt[12], 3))+r" $\Delta: $"+str(truncate(popt[8] - popt[12], 3)))
    ax1[0].fill_between(eV, voigt_multifit_component(eV, *popt[16:20]), alpha=.6, color='b', linestyle='-', label=r"$\omega_5$: "+str(truncate(popt[16], 3))+r" $\Delta: $"+str(truncate(popt[12] - popt[16], 3)))
    ax1[0].set_xlabel(r'\textrm{Photon Energy [eV]}')
    ax1[0].set_ylabel(r'\textrm{Photon Count}')
    ax1[0].grid(True)
    ax1[0].legend()

    ax1[1].errorbar(eV, residuals, uncertainty, marker=".", label='Data', linestyle="None", markersize=3, alpha=.5)
    ax1[1].plot([np.min(eV), np.max(eV)], [0, 0], c='r', linestyle='-')
    ax1[1].set_xlabel(r'\textrm{Photon Energy [eV]}')
    ax1[1].set_ylabel(r'\textrm{Residuals}')
    ax1[1].grid(True)
    ax1[1].legend()

    secAx = ax1[1].twiny()

    secAx.set_frame_on(True)
    secAx.patch.set_visible(False)
    secAx.xaxis.set_ticks_position('bottom')
    secAx.xaxis.set_label_position('bottom')
    secAx.spines['bottom'].set_position(('outward', 40))
    secAx.plot(eV, residuals, alpha=0)

    E_ticks = secAx.get_xticks()
    wl_ticks = [hc / n for n in E_ticks]
    wl_ticks = [truncate(n, 2) for n in wl_ticks]
    secAx.set_xticklabels(wl_ticks)

    secAx.set_xlabel(r'\textrm{Wavelength [nm]}')
    
    fig1.tight_layout()
    plt.draw()
    fig1.savefig("figures/fit_results_5_voigts.svg", bbox_inches='tight', dpi=300)
