import numpy as np
import matplotlib.pyplot as plt

np.random.seed(45)
d = np.random.randint(0, 2, 10)
n = 100
s1 = 1
s2 = -1
sigma2 = 1.5

signal = np.array([s1 if bit == 0 else s2 for bit in d]).repeat(n)

noise = np.random.normal(0, np.sqrt(sigma2), len(signal))

noisy_signal = signal + noise

integral = np.cumsum(signal * noise)

t = np.arange(len(signal))
plt.figure(figsize=(12, 8))

# Исходный сигнал
plt.subplot(3, 1, 1)
plt.step(t, signal, where='post')
plt.title('Исходный сигнал')
plt.grid(True)
plt.ylim(-2, 2)
plt.ylabel('Амплитуда')

# Сигнал с шумом
plt.subplot(3, 1, 2)
plt.plot(t, noisy_signal)
plt.title('Сигнал с шумом')
plt.grid(True)
plt.ylabel('Амплитуда')

# Интеграл (нада свертку с прямоугольником)
plt.subplot(3, 1, 3)
plt.plot(t, integral, 'r')
plt.title('Интеграл ∫σ(t)s(t)dt')
plt.grid(True)
plt.xlabel('Время')
plt.ylabel('Значение интеграла')

plt.tight_layout()
plt.show()