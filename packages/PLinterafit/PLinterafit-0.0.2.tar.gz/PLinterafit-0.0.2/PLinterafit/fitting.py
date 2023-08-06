# Authors: Viktor Bender and Bayarjargal N.Tugchin
# Date: 16/03/2023
# Last update: 01/04/2023


from PLinterafit.models import *
from PLinterafit.statistics import *
from PLinterafit.dataPreparation import *
from PLinterafit.plotting import *
import matplotlib.pyplot as plt
from scipy.optimize import leastsq, curve_fit
import scipy.stats as stats
from matplotlib.widgets import Slider, Button
import scipy.integrate as integrate
from matplotlib.ticker import FixedLocator



# Error will be raised if the number of calls of 'curve_fit' has been reached
My_maxfav = 100000

hc = constants.physical_constants['Planck constant in eV s'][0] * \
     constants.physical_constants['speed of light in vacuum'][0] * 1e9


def create_slider(ax, label, valmin: float, valmax: float, valinit) -> Slider:
    """
    Create a slider widget with the given minimum, maximum, and initial values.

    Args:
        ax: axes
            The axes object on which to create the slider.
        label: str
            The label for the slider.
        valmin: float
            The minimum value of the slider.
        valmax: float
            The maximum value of the slider.
        valinit: float
            The initial value of the slider.

    Returns:
        slider: Slider
            The created slider widget.
    """
    slider = Slider(
        ax=ax,
        label=label,
        valmin=valmin,
        valmax=valmax,
        valinit=valinit,
    )
    ax._silderRef = slider
    return slider

def create_button(ax, label)-> Button:
    """
    Create a button widget with the given label.

    Args:
        ax: axes
            The axes object on which to create the button.
        label: str
            The label for the button.

    Returns:
        button: Button
            The created button widget.
    """
    button = Button(
        ax=ax,
        label=label,
    )
    ax._buttonRef = button
    return button

def create_slider_group_voigt(fig, seed_temp, update, voigt_order, position_yaxis0, slider_thickness):
    """
    Create a group of four sliders for a Voigt profile with the given seed values as seed_temp.

    Args:
        fig: figure 
            The figure object on which to create the slider group.
        seed_temp: list
            A list of four float values representing the seed values for the Voigt profile.
        update: function
            The function to call when any slider in the group is changed.
        voigt_order: int
            The order of the Voigt profile.
        position_yaxis0: float
            The y-axis position of the top slider in the group.
        slider_thickness: float 
            Thickness of the sliders.

    Returns:
        tuple
            A tuple of four Slider objects representing the median, amplitude, Lorenzian half-width at half-maximum (HWHM),
            and Gaussian HWHM of the Voigt profile, respectively.
    """
    
    # Creating labels for sliders
    label_median = 'median ' + str(voigt_order)
    label_amplitude = 'amplitude ' + str(voigt_order)
    label_lorenzian = 'Lorenzian HWHM ' + str(voigt_order)
    label_gaussian = 'Gaussian HWHM ' + str(voigt_order)
    
    
    # Creating sliders at given position
    med_ax = fig.add_axes([0.25, position_yaxis0, 0.65,  slider_thickness])
    # median can be adjusted between 1.5 to 2.5
    med_slider = create_slider(med_ax, label_median, 1.5, 2.5, seed_temp[0])

    amp_ax = fig.add_axes([0.25, position_yaxis0 - 0.02, 0.65, slider_thickness])
    # amplitude can be adjusted between 0 to 2000
    amp_slider = create_slider(amp_ax, label_amplitude, 0, 2000, seed_temp[1])

    lor_ax = fig.add_axes([0.25, position_yaxis0 - 0.04, 0.65, slider_thickness])
    # lorenzian hwhm can be adjusted between 0 to 0.5
    lor_slider = create_slider(lor_ax, label_lorenzian, 0, 0.5, seed_temp[2])

    gaus_ax = fig.add_axes([0.25, position_yaxis0 - 0.06, 0.65, slider_thickness])
    # gaussian can be adjusted between 0 to 0.5
    gaus_slider = create_slider(gaus_ax, label_gaussian, 0, 0.5, seed_temp[3])

    med_slider.on_changed(update)
    amp_slider.on_changed(update)
    lor_slider.on_changed(update)
    gaus_slider.on_changed(update)

    return med_slider, amp_slider, lor_slider, gaus_slider


def fit_one_voigt(data: np.array, median: float, amplitude: float, lorentzian_hwhm: float, gaussian_hwhm: float, offset: float = 0, mode: str = 'poisson') -> tuple:
    """
    Fit a Voigt function to data using interactive sliders to adjust parameters.
    
    Args:
        data : np.array
            The data to fit, with shape (n, 3), where the zeroth collumn contains the wavelength values, the first column contains
            the photon energy values and the second column contains the photon counts values.
        median : float
            The initial guess for the median of the Voigt function.
        amplitude : float
            The initial guess for the amplitude of the Voigt function.
        lorentzian_hwhm : float
            The initial guess for the half width of the Lorentzian component
            of the Voigt function.
        gaussian_hwhm : float
            The initial guess for the half width of the Gaussian component
            of the Voigt function.
        offset : float, optional
            The initial guess for the offset of the Voigt function. Defaults to 0.
        mode : str
            The mode of the underlying noise distribution in the data, either "poisson" or "gauss". Defaults to "poisson".

    Returns:
        tuple
            A tuple containing the fit parameters (median, amplitude, lorentzian_width,
            gaussian_width, offset), the standard errors of the fit parameters, the residuals,
            and the chi-squared value.

    """
    
    # local functions
    
    def update(val):
        seed_line.set_ydata(func(eV, med1_slider.val, amp1_slider.val, lor1_slider.val, gaus1_slider.val, offset_slider.val))
        comp1_line.set_ydata(voigt_multifit_component(eV, med1_slider.val, amp1_slider.val, lor1_slider.val, gaus1_slider.val))
        fig.canvas.draw_idle()
        
        # Update the seed array with the new slider values
        seed[:] = [med1_slider.val, amp1_slider.val, lor1_slider.val, gaus1_slider.val, offset_slider.val]
        
    def do_statistical_analysis(event):
        
        # Curve fitting and doing statisctical analysis
        popt, popt_std, expected, uncertainty, residuals, chi2, p_value, ndof = do_statistics(func, eV, observed, seed, mode, My_maxfav)

        # If successful, plot and print the results        
        plot_fitted_results_one_voigt(eV, observed, expected, uncertainty, popt, popt_std, residuals, chi2, p_value, ndof)
        
        print("--------------------------------------------------")
        print("--------------------------------------------------")
        print("Fit Results:")
        print("Voigt Parameters: [median, amplitude, lorentzian_hwhm1, gaussian_hwhm]")
        print("Voigt 1: ", popt[0:4])
        print("Offset: ", popt[4])
        print("chi2/ndof: ", chi2/ndof)
        print("p_value: ", p_value)
        
        return 
    
    # Renaming the imported data
    func = one_voigt
    seed = [median, amplitude, lorentzian_hwhm, gaussian_hwhm, offset]
    eV = data[:, 1]
    observed = data[:, 2]

    # Plotting the measured data and fit using a Voigt function with initial seed values
    fig, ax = plot_data_and_one_voigt_seed_function(data, func, seed)  
    
   
    seed_line = ax.get_lines()[0]
    comp1_line = ax.get_lines()[1]
    
    fig.subplots_adjust(bottom=.5)
    
    # Creating sliders for one Voigt function
    slider_thickness = 0.025
    med1_slider, amp1_slider, lor1_slider, gaus1_slider = create_slider_group_voigt(fig, seed, update, 1, 0.35, slider_thickness)
    
    # Creating a slider for the offset adjustment
    offset_ax = fig.add_axes([0.25, 0.27, 0.65, slider_thickness])
    # Offset can be adjusted between 0 to 50
    offset_slider = create_slider(offset_ax, 'Offset', 0, 50, seed[4])
    offset_slider.on_changed(update)
    
    
    # Creating a button for the curve fitting once the adjusted seed values are deemed good  
    prpceed_Button_ax = fig.add_axes([0.65, 0.05, 0.3, 0.05])
    proceed_Button = create_button(prpceed_Button_ax, "Go to next step.")
    proceed_Button.on_clicked(do_statistical_analysis)
    

    return




def fit_five_voigts(data: np.array, median1: float, amplitude1: float, lorentzian_hwhm1: float, gaussian_hwhm1: float, 
                  median2: float, amplitude2: float, lorentzian_hwhm2: float, gaussian_hwhm2: float,
                  median3: float, amplitude3: float, lorentzian_hwhm3: float, gaussian_hwhm3: float, 
                  median4: float, amplitude4: float, lorentzian_hwhm4: float, gaussian_hwhm4: float,
                  median5: float, amplitude5: float, lorentzian_hwhm5: float, gaussian_hwhm5: float, offset: float = 0, mode: str = 'poisson'):
    """
    Fit five Voigt functions to data using interactive sliders to adjust parameters.
    
    Args:
        data : np.array
            The data to fit, with shape (n, 3), where the zeroth collumn contains the wavelength values, the first column contains
            the Photon energy values and the second column contains the Ph0ton counts values.
        median1-5 : float
            The initial guess for the median of each Voigt function 1-5.
        amplitude1-5: float
            The initial guess for the amplitude of each Voigt function 1-5.
        lorentzian_hwhm1-5 : float
            The initial guess for the half width of the Lorentzian component
            of the Voigt function 1-5.
        gaussian_hwhm1-5 : float
            The initial guess for the half width of the Gaussian component
            of each Voigt function 1-5.
        offset : float, optional
            The initial guess for the offset of each Voigt function. Defaults to 0.
        mode : str
            The mode of the underlying noise distribution in the data, either "poisson" or "gauss". Defaults to "poisson".

    Returns:
        tuple
            A tuple containing the fit parameters (median, amplitude, lorentzian_width,
            gaussian_width, offset), the standard errors of the fit parameters, the residuals,
            and the chi-squared value.

    """
    
    # Local functions
    def update(val):
        
        seed_line.set_ydata(func(eV,
                                 med1_slider.val, amp1_slider.val, lor1_slider.val, gaus1_slider.val,
                                 med2_slider.val, amp2_slider.val, lor2_slider.val, gaus2_slider.val,
                                 med3_slider.val, amp3_slider.val, lor3_slider.val, gaus3_slider.val,
                                 med4_slider.val, amp4_slider.val, lor4_slider.val, gaus4_slider.val,
                                 med5_slider.val, amp5_slider.val, lor5_slider.val, gaus5_slider.val,
                                 offset_slider.val))
        comp1_line.set_ydata(voigt_multifit_component(eV, med1_slider.val, amp1_slider.val, lor1_slider.val, gaus1_slider.val))
        comp2_line.set_ydata(voigt_multifit_component(eV, med2_slider.val, amp2_slider.val, lor2_slider.val, gaus2_slider.val))
        comp3_line.set_ydata(voigt_multifit_component(eV, med3_slider.val, amp3_slider.val, lor3_slider.val, gaus3_slider.val))
        comp4_line.set_ydata(voigt_multifit_component(eV, med4_slider.val, amp4_slider.val, lor4_slider.val, gaus4_slider.val))
        comp5_line.set_ydata(voigt_multifit_component(eV, med5_slider.val, amp5_slider.val, lor5_slider.val, gaus5_slider.val))

        fig.canvas.draw_idle()
        
        # Update the seed array with the new slider values
        seed[:] = [med1_slider.val, amp1_slider.val, lor1_slider.val, gaus1_slider.val,
                   med2_slider.val, amp2_slider.val, lor2_slider.val, gaus2_slider.val,
                   med3_slider.val, amp3_slider.val, lor3_slider.val, gaus3_slider.val,
                   med4_slider.val, amp4_slider.val, lor4_slider.val, gaus4_slider.val,
                   med5_slider.val, amp5_slider.val, lor5_slider.val, gaus5_slider.val,
                   offset_slider.val]
    
    def do_statistical_analysis(event):
        
        # Curve fitting and doing statisctical analysis
        popt, popt_std, expected, uncertainty, residuals, chi2, p_value, ndof = do_statistics(func, eV, observed, seed, mode, My_maxfav)
        
        # If successful, plot and print the results  
        plot_fitted_results_five_voigt(eV, observed, expected, uncertainty, popt, popt_std, residuals, chi2, p_value, ndof)
        
        print("--------------------------------------------------")
        print("--------------------------------------------------")
        print("Fit Results:")
        print("Voigt Parameters: [median, amplitude, lorentzian_hwhm1, gaussian_hwhm]")
        print("Voigt 1: ", popt[0:4])
        print("Voigt 2: ", popt[4:8])
        print("Voigt 3: ", popt[8:12])
        print("Voigt 4: ", popt[12:16])
        print("Voigt 5: ", popt[16:20])
        print("Offset: ", popt[20])
        print("chi2/ndof: ", chi2/ndof)
        print("p_value: ", p_value)
        
        return
    
    # Renaming the imported data
    func = five_voigt
    # seed = med1, amp1, lor1, gaus1, med2, amp2, lor2, gaus2, med3, amp3, lor3, gaus3, med4, amp4, lor4, gaus4, med5, amp5, lor5, gaus5, offset
    seed = [median1, amplitude1, lorentzian_hwhm1, gaussian_hwhm1, 
            median2, amplitude2, lorentzian_hwhm2, gaussian_hwhm2,
            median3, amplitude3, lorentzian_hwhm3, gaussian_hwhm3, 
            median4, amplitude4, lorentzian_hwhm4, gaussian_hwhm4,
            median5, amplitude5, lorentzian_hwhm5, gaussian_hwhm5, offset]
    eV = data[:, 1]
    observed = data[:, 2]

    # Plotting the measured data and fit using 5 Voigt functions with initial seed values
    fig, ax = plot_data_and_five_voigt_seed_function(data, func, seed)  

    seed_line = ax.get_lines()[0]
    comp1_line = ax.get_lines()[1]
    comp2_line = ax.get_lines()[2]
    comp3_line = ax.get_lines()[3]
    comp4_line = ax.get_lines()[4]
    comp5_line = ax.get_lines()[5]

    fig.subplots_adjust(bottom=.7)

    # Creating sliders for 5 Voigt functions
    slider_thickness = 0.01
    med1_slider, amp1_slider, lor1_slider, gaus1_slider = create_slider_group_voigt(fig, seed[0:4], update, 1, 0.6, slider_thickness)
    med2_slider, amp2_slider, lor2_slider, gaus2_slider = create_slider_group_voigt(fig, seed[4:8], update, 2, 0.52, slider_thickness)
    med3_slider, amp3_slider, lor3_slider, gaus3_slider = create_slider_group_voigt(fig, seed[8:12], update, 3, 0.44, slider_thickness)
    med4_slider, amp4_slider, lor4_slider, gaus4_slider = create_slider_group_voigt(fig, seed[12:16], update, 4, 0.36, slider_thickness)
    med5_slider, amp5_slider, lor5_slider, gaus5_slider = create_slider_group_voigt(fig, seed[16:20], update, 5, 0.28, slider_thickness)
    
    # Creating a slider for the offset adjustment
    offset_ax = fig.add_axes([0.25, 0.2, 0.65, slider_thickness])
    # Offset can be adjusted between 0 to 50
    offset_slider = create_slider(offset_ax, 'Offset', 0, 50, seed[-1])
    offset_slider.on_changed(update)
    
   
    # Creating a button for the curve fitting once the adjusted seed values are deemed good
    prpceed_Button_ax = fig.add_axes([0.65, 0.1, 0.3, 0.05])
    proceed_Button = create_button(prpceed_Button_ax, "Go to next step.")
    proceed_Button.on_clicked(do_statistical_analysis)
     
    
   
    return



