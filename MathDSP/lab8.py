import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

sampling_rate = 10000
t = np.arange(0, 0.1, 1/sampling_rate)

signal = (np.cos(2*np.pi*200*t) + 0.5*np.sin(2*np.pi*50*t) + 
          0.3*np.cos(2*np.pi*100*t) + 0.2*np.sin(2*np.pi*150*t) + 
          0.1*np.cos(2*np.pi*150*t)+ 0.7*np.cos(2*np.pi*50*t))

N = len(signal)
yf = fft(signal)
xf = fftfreq(N, 1 / sampling_rate)

max_freq = np.abs(xf[np.argmax(np.abs(yf))])
print(f"Максимальная частота: {max_freq} Гц")

plt.subplot(2, 2, 1)
plt.plot(t, signal)
plt.title('Оригинальный сигнал')
plt.xlabel('Время')
plt.ylabel('Амплитуда')

sampling_rate_1 = max_freq
t1 = np.arange(0, 0.1, 1/sampling_rate_1)
signal1 = signal[::int(sampling_rate / sampling_rate_1)]

plt.subplot(2, 2, 2)
plt.plot(t1, signal1)
plt.title(f'Сигнал с частотой дискретизации {sampling_rate_1} Гц')
plt.xlabel('Время')
plt.ylabel('Амплитуда')

sampling_rate_2 = 2 * max_freq
t2 = np.arange(0, 0.1, 1/sampling_rate_2)
signal2 = signal[::int(sampling_rate / sampling_rate_2)]

plt.subplot(2, 2, 3)
plt.plot(t2, signal2)
plt.title(f'Сигнал с частотой дискретизации {sampling_rate_2} Гц')
plt.xlabel('Время')
plt.ylabel('Амплитуда')

sampling_rate_3 = 5 * max_freq
t3 = np.arange(0, 0.1, 1/sampling_rate_3)
signal3 = signal[::int(sampling_rate / sampling_rate_3)]

plt.subplot(2, 2, 4)
plt.plot(t3, signal3)
plt.title(f'Сигнал с частотой дискретизации {sampling_rate_3} Гц')
plt.xlabel('Время')
plt.ylabel('Амплитуда')

plt.show()
