import time
import numpy as np
import seabreeze.spectrometers as sb
from scipy.optimize import curve_fit
from gpiozero import Button, LED

# pip install seabreeze numpy scipy matplotlib gpiozero

def get_dark_current(spec, integration_time):
    spec.integration_time_micros(integration_time)
    dark_spectrum = spec.spectrum(correct_dark_counts=True, correct_nonlinearity=True)
    return dark_spectrum

def get_signal_spectrum(spec, integration_time, dark_spectrum):
    spec.integration_time_micros(integration_time)
    signal_spectrum = spec.spectrum(correct_dark_counts=True, correct_nonlinearity=True) - dark_spectrum
    return signal_spectrum

def calculate_snr(signal_spectrum):
    return np.max(signal_spectrum) / np.std(signal_spectrum)

# def gaussian_fit(x, a, b, c):
#     return a * np.exp(-0.5 * ((x - b) / c) ** 2)

def find_optimal_integration_time(spec, fov_degrees=25, min_integration_time=1000, max_integration_time=100000, step=1000):
    optimal_integration_time = min_integration_time
    max_snr = 0

    dark_spectrum = get_dark_current(spec, optimal_integration_time)

    for integration_time in range(min_integration_time, max_integration_time + 1, step):
        signal_spectrum = get_signal_spectrum(spec, integration_time, dark_spectrum)
        snr = calculate_snr(signal_spectrum)

        if snr > max_snr:
            max_snr = snr
            optimal_integration_time = integration_time

    return optimal_integration_time

def get_saturation_range(spec, fov_degrees, saturation_percentage=90):
    full_spectrum = get_signal_spectrum(spec, 1000, np.zeros(spec.pixels))
    saturation_threshold = np.percentile(full_spectrum, saturation_percentage)
    saturation_min = np.min(full_spectrum[full_spectrum < saturation_threshold])
    saturation_max = np.max(full_spectrum[full_spectrum < saturation_threshold])
    return saturation_min, saturation_max

def save_spectrum_to_txt(filename, spectrum, integration_time, saturation_min, saturation_max):
    wavelengths = spec.wavelengths() 
    intensities = spec.intensities()

    data = np.column_stack((wavelengths, intensities))
    header = f"Integration Time (micros): {integration_time} \
        \nMin saturation: {saturation_min} \
        \nMax saturation: {saturation_max} \
        \nWavelength (nm), Intensity (Counts)"
    np.savetxt(filename, data, delimiter=',', header=header, comments='')

def obtain_calibration():
    global signal_spectrum, dark_spectrum, optimal_integration_time, measurement_num
    led19 = LED(19)
    led16 = LED(16)

    blink(led19,2)
    print('Começou')

    optimal_integration_time = find_optimal_integration_time(spec, fov_degrees, min_integration_time, max_integration_time, step)
    print(f"Tempo ótimo de integração: {optimal_integration_time} microssegundos")

    dark_spectrum = get_dark_current(spec, optimal_integration_time)
    signal_spectrum = get_signal_spectrum(spec, optimal_integration_time, dark_spectrum)

    signal_spectrum[signal_spectrum < saturation_min] = saturation_min
    signal_spectrum[signal_spectrum > saturation_max] = saturation_max

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"spectrum_calibration_{timestamp}_{measurement_num}_{optimal_integration_time}.txt"
    path = '/home/pi/spectrometer/measurements/'
    # save_spectrum_to_txt(path + filename, signal_spectrum, optimal_integration_time)
    save_spectrum_to_txt(path + filename, signal_spectrum, optimal_integration_time, saturation_min, saturation_max)

    time.sleep(5)  
    print('Finalizou')
    blink(led16,2)
    measurement_num += 1
    return

def obtain_measurement():
    global signal_spectrum, dark_spectrum, optimal_integration_time, measurement_num
    led19 = LED(19)
    led16 = LED(16)

    blink(led19,1)
    print('Começou')
    print(f"Usando o tempo de integração: {optimal_integration_time} microssegundos")

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"spectrum_measurement_{timestamp}_{measurement_num}_{optimal_integration_time}.txt"
    path = '/home/pi/spectrometer/measurements/'
    # save_spectrum_to_txt(path + filename, signal_spectrum, optimal_integration_time)
    save_spectrum_to_txt(path + filename, signal_spectrum, optimal_integration_time, saturation_min, saturation_max)

    time.sleep(5)  
    print('Finalizou')
    blink(led16,1)
    measurement_num += 1
    return

def blink(led,times):
    it = 1
    while it <= times:
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)
        it = it + 1

if __name__ == "__main__":
    devices = sb.list_devices()

    if not devices:
        print("Nenhum espectrômetro encontrado.")
    else:
        timeToObtainMeasu = 5*60
        spec = sb.Spectrometer(devices[0])
        fov_degrees = 25
        min_integration_time = 10
        max_integration_time = 10000
        step = 10
        button21 = Button(21)
        button13 = Button(13)
        global signal_spectrum, dark_spectrum, optimal_integration_time, measurement_num
        measurement_num = 1

        try:
            saturation_min, saturation_max = get_saturation_range(spec, fov_degrees)

            while True:
                if measurement_num == 1:
                    time.sleep(timeToObtainMeasu)
                    obtain_calibration()
                else:
                    obtain_measurement()
                    time.sleep(2)
                
                print(measurement_num)
                
        except KeyboardInterrupt:
            print("Medições interrompidas pelo usuário.")
