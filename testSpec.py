
from seabreeze.spectrometers import Spectrometer, list_devices
devices = list_devices()
print(devices)
spec = Spectrometer.from_first_available()

spec.integration_time_micros(20000)

wavelengths = spec.wavelengths()
print(wavelengths)

intensities = spec.intensities()
print(intensities)