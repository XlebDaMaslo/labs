import numpy as np
import matplotlib.pyplot as plt

f = 1
A1 = 4 / np.pi
A2 = 4 / (3 * np.pi)
phi1 = -np.pi / 2
phi2 = -np.pi / 2

t = np.linspace(0, 5, 1000)

x = A1 * np.cos(2 * np.pi * f * t + phi1) + A2 * np.cos(2 * np.pi * 3 * f * t + phi2)

plt.plot(t, x)
plt.title('Результирующее колебание')
plt.xlabel('Время (с)')
plt.ylabel('Амплитуда')
plt.grid(True)
plt.show()

f = 0.25
N = 5
t = np.linspace(0, 5, 1000)

x_total = np.zeros_like(t)

plt.figure(figsize=(10, 8))

for n in range(1, N+1):
    x = (4 / ((2*n - 1) * np.pi)) * np.cos(2 * np.pi * (2*n - 1) * f * t - np.pi / 2)
    
    x_total += x
    
    plt.plot(t, x_total, label=f'Слагаемых: {n}')

plt.title('Результирующее колебание при увеличении числа гармоник')
plt.xlabel('Время (с)')
plt.ylabel('Амплитуда')
plt.grid(True)
plt.legend()
plt.show()
