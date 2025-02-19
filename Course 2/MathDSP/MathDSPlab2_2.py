import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

f = [15, 5, 20]
A = 4 / np.pi
phi = np.pi / 2
t = np.linspace(1, 2, 500)
dt = t[1] - t[0]

x_total = np.zeros_like(t)


plt.figure(figsize=(10, 8))
plt.subplot(3, 1, 1)
for n in range(1, 4):
    xn = A*np.cos(2*np.pi* f[n-1] *t + phi)
    plt.plot(t, xn, label=f'x{n}')
    x_total += xn
plt.xlabel('Время (с)')
plt.ylabel('Амплитуда')
plt.grid(True)
plt.legend()


plt.subplot(3, 1, 2)
plt.plot(t, x_total, label='Total', linewidth=2)
plt.title('Результирующее колебание')
plt.xlabel('Время (с)')
plt.ylabel('Амплитуда')
plt.grid(True)
plt.legend()

N = len(t)
xf = fftfreq(N, dt)[:N//2]
yf = fft(x_total)
amplitude_spectrum = 2.0/N * np.abs(yf[:N//2])

plt.subplot(3, 1, 3)
plt.stem(xf, amplitude_spectrum)
plt.title('Спектр сигнала')
plt.xlabel('Частота (Гц)')
plt.ylabel('Амплитуда')
plt.grid(True)
plt.xlim(0,50)

plt.tight_layout()
plt.show()