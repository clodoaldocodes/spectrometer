import time
import numpy as np
import seabreeze.spectrometers as sb
from scipy.optimize import curve_fit
from gpiozero import Button, LED

def get_dark_current(spec, integration_time):
    spec.integration_time_micros(integration_time)
    dark_spectrum = spec.spectrum(correct_dark_counts=True, correct_nonlinearity=True)
    return dark_spectrum

def get_signal_spectrum(spec, integration_time, dark_spectrum):
    spec.integration_time_micros(integration_time)
    signal_spectrum = spec.spectrum(correct_dark_counts=True, correct_nonlinearity=True) - dark_spectrum
    return signal_spectrum

def calculate_snr(signal_spectrum):
    # Neste exemplo, calculamos o SNR simplesmente como a razão entre o valor máximo e o desvio padrão do espectro.
    # Você pode usar outras métricas de SNR, dependendo dos requisitos do seu experimento.
    return np.max(signal_spectrum) / np.std(signal_spectrum)

def gaussian_fit(x, a, b, c):
    return a * np.exp(-0.5 * ((x - b) / c) ** 2)

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

def save_spectrum_to_txt(filename, spectrum, integration_time):
    wavelengths = spec.wavelengths()  # Obter os comprimentos de onda correspondentes aos pixels
    intensities = spec.intensities()

    # if len(wavelengths) != len(spectrum):
    #     raise ValueError("Os arrays de comprimento de onda e intensidade devem ter o mesmo tamanho.")

    data = np.column_stack((wavelengths, intensities))
    header = f"Integration Time (micros): {integration_time}\nWavelength (nm), Intensity (Counts)"
    np.savetxt(filename, data, delimiter=',', header=header, comments='')


def obtain_measurement():
    led19 = LED(19)
    led16 = LED(16)

    blink(led19,1)
    print('Começou')

    optimal_integration_time = find_optimal_integration_time(spec, fov_degrees, min_integration_time, max_integration_time, step)
    print(f"Tempo ótimo de integração: {optimal_integration_time} microssegundos")

    dark_spectrum = get_dark_current(spec, optimal_integration_time)
    signal_spectrum = get_signal_spectrum(spec, optimal_integration_time, dark_spectrum)

    # Remove valores fora do range de saturação
    signal_spectrum[signal_spectrum < saturation_min] = saturation_min
    signal_spectrum[signal_spectrum > saturation_max] = saturation_max

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"spectrum_{timestamp}_{measurement_num}_{optimal_integration_time}.txt"
    path = '/home/pi/spectrometer/measurements/'
    # save_spectrum_to_txt(path + filename, signal_spectrum, optimal_integration_time)
    save_spectrum_to_txt(path + filename, signal_spectrum, optimal_integration_time)

    time.sleep(5)  # Intervalo de espera entre medições (em segundos)
    print('Finalizou')
    blink(led16,2)

def blink(led,times):
    it = 0
    while it <= times:
        led.on()
        time.sleep(1)
        led.off()
        it = it + 1

if __name__ == "__main__":
    devices = sb.list_devices()

    if not devices:
        print("Nenhum espectrômetro encontrado.")
    else:
        spec = sb.Spectrometer(devices[0])
        fov_degrees = 25
        min_integration_time = 1000
        max_integration_time = 100000
        step = 1000
        PIN = 21
        button = Button(PIN)

        try:
            measurement_num = 1
            saturation_min, saturation_max = get_saturation_range(spec, fov_degrees)

            while True:
                button.when_pressed = obtain_measurement
                measurement_num += 1
                
        except KeyboardInterrupt:
            print("Medições interrompidas pelo usuário.")
