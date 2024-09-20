import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

#1
t_lim = 1
n = 10000
#t = np.arange(0, t_lim+(1/n), (1/n))
t = np.linspace(0, t_lim, n, endpoint=False)
f = 16
T = 1/n
n_points = t_lim * n
#phi = 8

y = np.sin((12 * np.pi * f * t) + (np.pi / 11)) + np.sin(10 * np.pi * f * t) 

plt.subplot(3, 1, 1)
plt.plot(t, y, label='Исходный сигнал')
plt.xlabel('Время (s)')
plt.ylabel('Амплитуда')
plt.title('Исходный сигнал')
plt.ylim(-2, 2)
plt.xlim(0, t_lim)
plt.grid(True)
plt.legend()

#2
yf = fft(y)
xf = fftfreq(n_points, T)[:n_points // 2]

A_spectr = 2 / n_points * np.abs(yf[:n_points//2])

max_i = np.argmax(A_spectr)
max_f = xf[max_i]

print(f"Максимальная частота: {max_f} Hz")

#3
min_fd = 2 * max_f

print(f"Минимальная частота дискретизации: {min_fd} Гц")

#4
dig_n = int(min_fd * t_lim)
dig_T = 1 / min_fd
dig_t = np.linspace(0, t_lim, dig_n, endpoint=False)

dig_y = np.sin((12 * np.pi * f * dig_t) + (np.pi / 11)) + np.sin(10 * np.pi * f * dig_t)

plt.subplot(3, 1, 2)
plt.stem(dig_t, dig_y, label='Оцифрованный сигнал')
plt.xlabel('Время (s)')
plt.ylabel('Амплитуда')
plt.title('Оцифрованный сигнал')
plt.ylim(-2, 2)
plt.xlim(0, t_lim)
plt.grid(True)
plt.legend()
plt.tight_layout()

print("Оцифрованные значения сигнала:")
dig_y = dig_y.astype(float)
print(dig_y)
#print(type(dig_y[0]))

#5
dig_yf = fft(dig_y)
dig_xf = fftfreq(dig_n, dig_T)[:dig_n // 2]
A_spectr_dig = 2 / dig_n * np.abs(dig_yf[:dig_n // 2])

max_i_dig = np.argmax(A_spectr_dig)
max_f_dig = dig_xf[max_i_dig]

f_min = dig_xf[0]
f_max = max_f_dig

print(f"Ширина спектра: {f_max - f_min} Гц")
print(f"Объем памяти для хранения массива dig_y: {dig_y.nbytes / 1024:.3f} КБ")


#6
plt.subplot(3, 1, 3)
plt.plot(dig_t, dig_y, label='Оцифрованный сигнал')
plt.xlabel('Время (s)')
plt.ylabel('Амплитуда')
plt.title('Оцифрованный сигнал')
plt.ylim(-2, 2)
plt.xlim(0, t_lim)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

#nn
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
    plt.xlim(0, 50)
    plt.grid(True)

    max_i = np.argmax(A_spectr)
    max_f = xf[max_i]
    f_min = xf[0]
    f_max = max_f
    width = f_max - f_min

    print(f"Ширина спектра для '{title}': {width:.2f} Hz")

plt.figure(figsize=(12, 10))

plot_fft(y, n, 'Амплитудный спектр оригинального сигнала', 1)

plot_fft(dig_y, dig_n, 'Амплитудный спектр дискретного сигнала', 2)

plt.tight_layout()
plt.show()

#13
n = 10000
y = np.sin((12 * np.pi * f * t) + (np.pi / 11)) + np.sin(10 * np.pi * f * t)

def quantize(signal, num_bits):
    max_value = 2**num_bits - 1
    return np.clip(signal, 0, max_value)

def plot_spectrum(signal, fs, title):
    N = len(signal)
    T = 1/fs
    yf = fft(signal)
    xf = fftfreq(N, T)[:N//2]
    plt.plot(xf, 2/N * np.abs(yf[:N//2]))
    plt.xlabel('Частота (Гц)')
    plt.ylabel('Амплитуда')
    plt.xlim(0, 100)
    plt.title(title)
    plt.grid(True)

num_bits_list = [3, 4, 5, 1]

plt.figure(figsize=(12, 8))
plt.subplot(5, 1, 1)
plot_spectrum(y, n, 'Исходный сигнал')

for i, num_bits in enumerate(num_bits_list):
    signal_quantz = quantize(y, num_bits)

    plt.subplot(5, 1, i+2)
    plot_spectrum(signal_quantz, n, f'Квантованный сигнал ({num_bits} бит)')
    plt.xlim(0, 100)
    error = np.mean(np.abs(y - signal_quantz))
    print(f"Средняя ошибка квантования для {num_bits} бит: {error}")

plt.tight_layout()
plt.show()