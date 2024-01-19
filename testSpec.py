from seabreeze.spectrometers import Spectrometer, list_devices
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

devices = list_devices()
print(devices)
spec = Spectrometer.from_first_available()

signal_spectrum = spec.spectrum(correct_dark_counts=True, correct_nonlinearity=True)

wavelengths = signal_spectrum.wavelengths()
print(wavelengths)

intensities = signal_spectrum.intensities()
print(intensities)

sns.set()
plt.plot(wavelengths, intensities)
plt.savefig("/home/pi/spectrometer/foo.png")