import numpy as np
import matplotlib.pyplot as plt

N = 1000
T = 1.0
t = np.linspace(-10, 10, N)
duration = 5
shift = 0

def rectangular_pulse(t, duration):
    return np.where(np.abs(t) <= duration / 2, 1.0, 0.0)

def calculate_spectrum(signal, N, T):
    spectrum = np.fft.fft(signal)
    freqs = np.fft.fftfreq(N, T)
    return freqs, spectrum

def find_zeros_in_spectrum(spectrum, freqs):
    threshold = 1e-5
    zeros_indices = np.where(np.abs(np.abs(spectrum)) < threshold)[0]
    zeros_frequencies = freqs[zeros_indices]
    return zeros_frequencies

def plot_pulse_and_spectrum(pulse, freqs, spectrum, duration, shift, subplot_index):
    plt.subplot(3, 2, subplot_index)
    plt.plot(t, pulse)
    plt.title(f'Прямоугольный импульс (Длительность {duration}, Смещение {shift})')
    plt.xlabel('Время')
    plt.ylabel('Амплитуда')
    plt.grid()

    plt.subplot(3, 2, subplot_index + 1)
    plt.plot(np.fft.fftshift(freqs), np.fft.fftshift(np.abs(spectrum)))
    plt.title(f'Амплитудный спектр (Длительность {duration}, Смещение {shift})')
    plt.xlabel('Частота')
    plt.ylabel('Амплитуда')
    plt.xlim(-0.01, 0.01)
    plt.grid()

plt.figure(figsize=(12, 12))

pulse = rectangular_pulse(t, duration)
freqs, spectrum = calculate_spectrum(pulse, N, T)
plot_pulse_and_spectrum(pulse, freqs, spectrum, duration, shift, 1)

zeros_frequencies = find_zeros_in_spectrum(spectrum, freqs)
print(f'Частоты нулей в спектре (Длительность {duration}):', zeros_frequencies)

duration = 10
pulse = rectangular_pulse(t, duration)
freqs, spectrum = calculate_spectrum(pulse, N, T)
plot_pulse_and_spectrum(pulse, freqs, spectrum, duration, shift, 3)

zeros_frequencies = find_zeros_in_spectrum(spectrum, freqs)
print(f'Частоты нулей в спектре (Длительность {duration}):', zeros_frequencies)

shift = 2.5
duration = 5
pulse_shifted = rectangular_pulse(t - shift, duration)
freqs, spectrum = calculate_spectrum(pulse_shifted, N, T)
plot_pulse_and_spectrum(pulse_shifted, freqs, spectrum, duration, shift, 5)

zeros_frequencies = find_zeros_in_spectrum(spectrum, freqs)
print(f'Частоты нулей в спектре (Длительность {duration}, Смещение {shift}):', zeros_frequencies)

plt.tight_layout()
plt.show()
