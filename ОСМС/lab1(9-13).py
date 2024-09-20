import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.io import wavfile
from scipy.io.wavfile import write
import pyaudio

#9
Fs, y = wavfile.read('G:/Documents/labs/labs/ОСМС/lab1.wav')

#10
num_samples = len(y)
duration = num_samples / Fs
calc_Fs = num_samples / duration

print(f"Определенная частота дискретизации: {calc_Fs} Hz")
print(f"Частота дискретизации, полученная из файла: {Fs} Hz")

#11
def downsample(y, factor):
    return y[::factor]
factor = 30
y1 = downsample(y, factor)
Fs_new = Fs // factor

write('G:/Documents/labs/labs/ОСМС/lab1_downsampled.wav', Fs_new, y1.astype(np.int16))

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=Fs_new,
                output=True)

stream.write(y1.astype(np.int16).tobytes())

stream.stop_stream()
stream.close()
p.terminate()

#12
def plot_fft(signal, fs, title, pos):
    N = len(signal)
    T = 1 / fs
    yf = fft(signal)
    xf = fftfreq(N, T)[:N // 2]
    A_spectr = 2 / N * np.abs(yf[:N // 2])

    plt.subplot(2, 1, pos)
    plt.plot(xf, A_spectr)
    plt.title(title)
    plt.xlabel('Частота (Hz)')
    plt.ylabel('Амплитуда')
    plt.grid(True)

    max_i = np.argmax(A_spectr)
    max_f = xf[max_i]
    f_min = xf[0]
    f_max = max_f
    width = f_max - f_min

    print(f"Ширина спектра для '{title}': {width:.2f} Hz")

plt.figure(figsize=(12, 10))

plot_fft(y, Fs, 'Амплитудный спектр оригинального сигнала', 1)

plot_fft(y1, Fs_new, 'Амплитудный спектр прореженного сигнала', 2)

plt.tight_layout()
plt.show()

#13
def quantize(signal, num_bits):
    max_value = 2**num_bits - 1
    return np.clip(signal, 0, max_value)

def plot_spectr(signal, fs, title):
    N = len(signal)
    T = 1/fs
    yf = fft(signal)
    xf = fftfreq(N, T)[:N//2]
    plt.plot(xf, 2/N * np.abs(yf[:N//2]))
    plt.xlabel('Частота (Гц)')
    plt.ylabel('Амплитуда')
    plt.title(title)
    plt.grid(True)

num_bits_list = [3, 4, 5, 6]

plt.figure(figsize=(12, 8))
plt.subplot(5, 1, 1)
plot_spectr(y, Fs, 'Исходный сигнал')


for i, num_bits in enumerate(num_bits_list):
    quantized_signal = quantize(y, num_bits)
    

    plt.subplot(5, 1, i+2)
    plot_spectr(quantized_signal, Fs, f'Квантованный сигнал ({num_bits} бит)')
    print(f'Пример значений после квантования для {num_bits} бит:')
    for i in range(5800, 5826):
        print(quantized_signal[i])
    #plt.ylim(0, 1)
    error = np.mean(np.abs(y - quantized_signal))
    print(f"Средняя ошибка квантования для {num_bits} бит: {error}")

plt.tight_layout()
plt.show()
