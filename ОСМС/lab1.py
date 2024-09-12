import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

#1
t_lim = 1
n = 1000
#t = np.arange(0, t_lim+(1/n), (1/n))
t = np.linspace(0, t_lim, n, endpoint=False)
f = 4

y = np.sin((12 * np.pi * f * t) + (np.pi / 11)) + np.sin(10 * np.pi * f * t)

plt.plot(t, y)
plt.xlabel('Время (s)')
plt.ylabel('Амплитуда')
plt.title('График сигнала')
plt.grid(True)
plt.show()

#2
spectr = fft(y)
f_arr = fftfreq(len(t), 1/n)
a_spectr = np.abs(spectr) / len(t)

positive_fs = f_arr[:len(f_arr)//2]
positive_spectr = a_spectr[:len(a_spectr)//2]

max_idx = np.argmax(positive_spectr)
max_f = positive_fs[max_idx]

print(f'Максимальная частота в спектре: {round(max_f,6)} Hz')

#3
min_fd = 2 * max_f

print(f"Минимальная частота дискретизации: {round(min_fd,6)} Гц")

#4
sampling_frequency = min_fd

num_samples = int(sampling_frequency * t_lim)

t_digitized = np.linspace(0, t_lim, num_samples, endpoint=False)

y_digitized = np.sin((12 * np.pi * f * t_digitized) + (np.pi / 11)) + np.sin(10 * np.pi * f * t_digitized)

digitized_signal = y_digitized

plt.stem(t_digitized, y_digitized)
plt.xlabel('Время (s)')
plt.ylabel('Амплитуда')
plt.title('Оцифрованный сигнал')
plt.grid(True)
plt.show()

print("Оцифрованный сигнал:")
print(digitized_signal)
