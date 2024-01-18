import seabreeze
seabreeze.use('pyseabreeze')
from seabreeze.spectrometers import Spectrometer, list_devices
devices = list_devices()
print(devices)
spec = Spectrometer.from_first_available()