import seabreeze.spectrometers as sb

spec = sb.Spectrometer.from_serial_number()
spec.integration_time_micros(2000)

spec.wavelengths()

spec.intensities()