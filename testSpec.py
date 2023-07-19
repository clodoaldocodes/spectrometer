import seabreeze.spectrometers as sb

devices = sb.list_devices()
spec = sb.Spectrometer(devices[0])
wavelengths = spec.wavelengths()
intensities = spec.intensities()

print(len(wavelengths))
print(len(intensities))