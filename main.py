import seabreeze.spectrometers as sb
import numpy as np
import pandas as pd
from gpiozero import Button
import gpiozero
import time

devices = sb.list_devices()
print(devices)
spec = sb.Spectrometer.from_serial_number()

PIN = 21
button = Button(PIN)

def say_hello():
    spec.integration_time_micros(20000)

    # print(spec.wavelengths())
    # print(spec.intensities())

    wavelengths = np.array(spec.wavelengths())
    intensities = np.array(spec.intensities())

    # print(np.size(wavelengths))
    # print('Min: ' + str(np.min(wavelengths)))
    # print('Max: ' + str(np.max(wavelengths)))

    # for i in range(np.size(wavelengths)):
    #     print(str(wavelengths[i]) + ' - ' + str(intensities[i]))

    matrix_aux = np.vstack([wavelengths,intensities])
    matrix     = np.transpose(matrix_aux)
    df = pd.DataFrame(matrix)

    #specify path for export
    path = r"/home/pi/spectrometer/data.txt"

    #export DataFrame to text file
    with open(path, 'a') as f:
        df_string = df.to_string(header=False, index=False)
        f.write(df_string)
    
    print('Finished')

while True:
    time.sleep(2)
    button.when_pressed = say_hello