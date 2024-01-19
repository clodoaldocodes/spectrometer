import seabreeze.spectrometers as sb
import matplotlib.pyplot as plt
import numpy as np

def perform_calibration(spec):
    # Realize a calibração aqui, ajustando os parâmetros conforme necessário
    # Isso pode envolver a correção da resposta espectral, a influência da iluminação, etc.

    # Exemplo: Normalizar o espectro para uma referência conhecida
    reference_spectrum = spec.intensities()
    normalized_spectrum = [intensity / max(reference_spectrum) for intensity in reference_spectrum]

    return normalized_spectrum

def measure_target(spec):
    # Obter espectro do alvo
    wavelengths = spec.wavelengths()
    spectrum = spec.intensities()

    # Realizar a correção usando os valores de calibração
    calibrated_spectrum = np.divide(spectrum, calibration_spectrum)

    # Plotar o espectro corrigido
    plt.plot(wavelengths, calibrated_spectrum)
    plt.title('Espectro do Alvo Calibrado')
    plt.xlabel('Comprimento de Onda (nm)')
    plt.ylabel('Intensidade Calibrada')
    plt.savefig("foog.png")
    plt.show()

# Encontrar e inicializar o espectrômetro
devices = sb.list_devices()
if not devices:
    print("Nenhum espectrômetro encontrado.")
    exit()

spec = sb.Spectrometer(devices[0])
spec.integration_time_micros(1000)  # Ajustar o tempo de integração conforme necessário

# Calibrar o espectrômetro
calibration_spectrum = perform_calibration(spec)

# Medir alvo claro
print("Medindo alvo claro:")
measure_target(spec)

# Medir alvo escuro
print("Medindo alvo escuro:")
measure_target(spec)

# Desconectar o espectrômetro
spec.close()
