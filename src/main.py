import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
import math
import argparse

# Function to remove NaN values from arrays
def remove_nan(x_value, y_value):
    """
    Remove NaN values from the y_value array and the corresponding x_value array.
    
    Parameters:
    x_value (array): The x-values array.
    y_value (array): The y-values array.

    Returns:
    tuple: Two numpy arrays without NaN values.
    """
    new_y = []
    new_x = []
    for i in range(len(y_value)):
        if not math.isnan(y_value[i]):
            new_y.append(y_value[i])
    for i in range(len(new_y)):
        new_x.append(x_value[i])
    return np.array(new_x), np.array(new_y)

# Function to load and plot SOC vs Voltage data
def load_and_plot_data(first_curve_filename, second_curve_filename):
    """
    Load and plot SOC vs Voltage data for 3C and 4C curves.

    Parameters:
    filename_3C (str): File path for 3C curve data.
    filename_4C (str): File path for 4C curve data.

    Returns:
    tuple: SOC and Voltage arrays for both 3C and 4C data.
    """
    # Load data
    SOC_3C, V_3C = np.loadtxt(first_curve_filename, delimiter=',', skiprows=1, unpack=True)
    SOC_4C, V_4C = np.loadtxt(second_curve_filename, delimiter=',', skiprows=1, unpack=True)

    # Plot data
    plt.figure()
    plt.plot(SOC_3C, V_3C, label='3C')
    plt.plot(SOC_4C, V_4C, label='4C')
    plt.xlabel('SOC')
    plt.ylabel('Voltage (V)')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    return SOC_3C, V_3C, SOC_4C, V_4C

# Function to interpolate and align SOC data
def interpolate_and_align(SOC_3C, V_3C, SOC_4C, V_4C):
    """
    Interpolate and align SOC data for 3C and 4C curves.

    Parameters:
    SOC_3C (array): SOC values for 3C curve.
    V_3C (array): Voltage values for 3C curve.
    SOC_4C (array): SOC values for 4C curve.
    V_4C (array): Voltage values for 4C curve.

    Returns:
    tuple: Interpolated Voltage arrays for 3C and 4C data, and new SOC array.
    """
    newX = np.linspace(0, 1, 100)
    interp_3C = interp1d(SOC_3C, V_3C, bounds_error=False)
    interp_4C = interp1d(SOC_4C, V_4C, bounds_error=False)

    newV_3C = interp_3C(newX)
    newV_4C = interp_4C(newX)

    return newX, newV_3C, newV_4C

# Function to compute resistance and open-circuit voltage
def compute_R_V_OC(newX, newV_3C, newV_4C, C):
    """
    Compute resistance and open-circuit voltage from interpolated data.

    Parameters:
    newX (array): Interpolated SOC values.
    newV_3C (array): Interpolated Voltage values for 3C curve.
    newV_4C (array): Interpolated Voltage values for 4C curve.
    C (float): Capacity factor.

    Returns:
    tuple: Arrays for SOC, Resistance, and Open-circuit voltage.
    """
    R = (newV_3C - newV_4C) / (4 * C - 3 * C)
    V_OC = newV_3C + (R * 3 * C)
    R_x_new, R_new = remove_nan(x_value=newX, y_value=R)
    V_OC_x_new, V_OC_new = remove_nan(x_value=newX, y_value=V_OC)

    return R_x_new, R_new, V_OC_x_new, V_OC_new

# Polynomial fitting function
def poly4(x, a, b, c, d, e):
    """
    Fourth-degree polynomial function.
    
    Parameters:
    x (array): Input array.
    a, b, c, d, e (float): Coefficients of the polynomial.

    Returns:
    array: Polynomial output.
    """
    return a * x**4 + b * x**3 + c * x**2 + d * x + e

# Function to fit and plot resistance and open-circuit voltage
def fit_and_plot(R_x_new, R_new, V_OC_x_new, V_OC_new):
    """
    Fit and plot resistance and open-circuit voltage against SOC.

    Parameters:
    R_x_new (array): SOC values for resistance.
    R_new (array): Resistance values.
    V_OC_x_new (array): SOC values for open-circuit voltage.
    V_OC_new (array): Open-circuit voltage values.
    """
    # Fit R(SOC)
    params_R, _ = curve_fit(poly4, R_x_new, R_new)
    fitresult_R = poly4(R_x_new, *params_R)

    plt.figure('R(SOC)')
    plt.plot(R_x_new, R_new, 'b-', label='R vs. SOC')
    plt.plot(R_x_new, fitresult_R, 'r-', label='R(SOC)')
    plt.xlabel('SOC')
    plt.ylabel('R')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Fit V_OC(SOC)
    params_V_OC, _ = curve_fit(poly4, V_OC_x_new, V_OC_new)
    fitresult_V_OC = poly4(V_OC_x_new, *params_V_OC)

    plt.figure('V_OC(SOC)')
    plt.plot(V_OC_x_new, V_OC_new, 'b-', label='V_OC vs. SOC')
    plt.plot(V_OC_x_new, fitresult_V_OC, 'r-', label='V_OC(SOC)')
    plt.xlabel('SOC')
    plt.ylabel('V_OC')
    plt.legend()
    plt.grid(True)
    plt.show()

    print("Fit results for R(SOC):", params_R)
    print("Fit results for V_OC(SOC):", params_V_OC)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Curve fit the R vs. SOC and Voc vs. SOC from the digitized datasheet discharge curves')
    parser.add_argument('--first-curve-file', type=str, help='Path to CSV file containing digitized discharge curve points for some discharge current')
    parser.add_argument('--second-curve-file', type=str, help='Path to CSV file containing digitized discharge curve points for a discharge current different from the one used in the first option')
    parser.add_argument("--battery-capacity", type=int)

    args = parser.parse_args()

    # Load and plot data
    soc_first_curve, voltage_first_curve, soc_second_curve, voltage_second_curve = load_and_plot_data(args.first_curve_file, args.second_curve_file)

    # Interpolate and align
    x_values, y_values_first_curve, y_values_second_curve = interpolate_and_align(soc_first_curve, voltage_first_curve, soc_second_curve, voltage_second_curve)

    # Compute R and V_OC
    R_x_new, R_new, V_OC_x_new, V_OC_new = compute_R_V_OC(x_values, y_values_first_curve, y_values_second_curve, args.battery_capacity)

    # Fit and plot
    fit_and_plot(R_x_new, R_new, V_OC_x_new, V_OC_new)