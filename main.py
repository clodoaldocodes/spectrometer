import seabreeze.spectrometers as sb
import numpy as np

devices = sb.list_devices()
print(devices)

spec = sb.Spectrometer.from_serial_number()
spec.integration_time_micros(20000)

# print(spec.wavelengths())
# print(spec.intensities())

wavelengths = np.array(spec.wavelengths())
intensities = np.array(spec.intensities())

print(np.size(wavelengths))
print('Min: ' + str(np.min(wavelengths)))
print('Max: ' + str(np.max(wavelengths)))

for i in range(np.size(wavelengths)):
    print(str(wavelengths[i]) + ' - ' + str(intensities[i]))