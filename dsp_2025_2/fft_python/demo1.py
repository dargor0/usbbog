#!/usr/bin/env python3

"""
Demo1: Basic use of FFT with scipy

Author: Oscar Diaz <odiaz@ieee.org>

Requirements: This script needs Python3, numpy, scipy and matplotlib.
    You can install these libraries on an existing Python environment with:

$ pip install numpy matplotlib scipy

Instructions:
* Adjust the desired parameters (sampling_rate, duration)
* Adjust the signal parameters (even change the signal components)
* Run the script and see the results in a single window subplot
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft, fftfreq, fftshift

# 1. Parameters
sampling_rate = 1000    # Sampling rate in Hz
duration = 1.0          # Duration in seconds

T = 1.0 / sampling_rate             # Sampling interval
N = int(sampling_rate * duration)   # Number of sample points
t = np.arange(0, duration, T)       # Time vector
f_raw = np.arange(0, sampling_rate, sampling_rate // N) # Freq vector (not shifted)

# 2. Create a sample signal
dcvalue = 0.2       # DC value of the singal
frequency1 = 50     # Frequency of the first sine wave in Hz
amp1 = 0.5          # Amplitude of the first sine wave in Hz
frequency2 = 300    # Frequency of the second sine wave in Hz
amp2 = 0.3          # Amplitude of the second sine wave in Hz

# Please adjust the signal to your needs
# ****
signal = dcvalue + amp1 * np.sin(2 * np.pi * frequency1 * t) + amp2 * np.sin(2 * np.pi * frequency2 * t)
# ****

# 3. Apply FFT
yf = fft(signal)  # Compute the FFT
xf = fftfreq(N, T)  # Frequency bins
yf_shifted = fftshift(yf)  # Shift the zero frequency component to the center
xf_shifted = fftshift(xf)  # Shift the frequency bins

# 4. Apply IFFT on a transformed signal
xf_recovered = ifft(yf)

# 5. Plotting
plt.figure(figsize=(12, 6))

# 5.1 Plot the original signal
plt.subplot(4, 1, 1)
plt.plot(t, signal)
plt.title('Original Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

# 5.2 Plot the FFT results
plt.subplot(4, 1, 2)
plt.plot(f_raw, np.abs(yf) / N)  # Normalize and plot
plt.title('FFT of the Signal')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')

# 5.3 Plot the shifted FFT results
plt.subplot(4, 1, 3)
plt.plot(xf_shifted, np.abs(yf_shifted) / N)  # Normalize and plot
plt.title('FFT of the Signal (Shifted)')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')

# 5.4 Plot the recovered signal
plt.subplot(4, 1, 4)
plt.plot(t, np.real(xf_recovered))
plt.title('Recovered Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

# 6. Show plot and finish
plt.tight_layout()
plt.show()
