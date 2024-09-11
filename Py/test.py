import numpy as np
import matplotlib.pyplot as plt

# Ваш исходный код
t = np.arange(0, 1.001, 0.0001)
y = np.sin((12 * np.pi * 4 * t) + (np.pi / 11)) + np.sin(10 * np.pi * 4 * t)

# Выполнение БПФ
Y = np.fft.fft(y)
frequencies = np.fft.fftfreq(len(t), d=t[1] - t[0])

# Определение максимальной частоты
magnitude = np.abs(Y)
max_freq = frequencies[np.argmax(magnitude)]

print(f'Максимальная частота в спектре: {max_freq} Hz')

# Визуализация сигнала
#plt.figure(figsize=(12, 6))

#plt.subplot(2, 1, 1)
plt.plot(t, y)
plt.xlabel('Время (s)')
plt.ylabel('Амплитуда')
plt.title('График сигнала')
plt.grid(True)

## Визуализация спектра
#plt.subplot(2, 1, 2)
#plt.plot(frequencies, magnitude)
#plt.xlabel('Частота (Hz)')
#plt.ylabel('Амплитуда')
#plt.title('Спектр сигнала')
#plt.grid(True)

#plt.tight_layout()
plt.show()

