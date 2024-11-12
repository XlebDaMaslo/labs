import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

N = 10

x = np.array([1, 2, 3, 0.5])
h = np.array([np.exp(-0.1 * N * 0), np.exp(-0.1 * N * 1), np.exp(-0.1 * N * 2), np.exp(-0.1 * N * 3)])
print()

y = np.convolve(x, h)
#print(y)

plt.figure()

# Входной сигнал
plt.subplot(3, 1, 1)
plt.stem(x)
plt.title('Входной сигнал x(n)')
plt.xlabel('n')
plt.ylabel('x(n)')

# Импульсная характеристика
plt.subplot(3, 1, 2)
plt.stem(h)
plt.title('Импульсная характеристика h(n)')
plt.xlabel('n')
plt.ylabel('h(n)')

# Выходной сигнал
plt.subplot(3, 1, 3)
plt.stem(y)
plt.title('Выходной сигнал y(n)')
plt.xlabel('n')
plt.ylabel('y(n)')

plt.tight_layout()

plt.figure(figsize=(8, 6))
w, hw = signal.freqz(h, whole=True)
plt.plot(w, 20 * np.log10(abs(hw)), 'b')
plt.xlabel('Частота')
plt.ylabel('Амплитуда')
plt.grid(True)

plt.show()