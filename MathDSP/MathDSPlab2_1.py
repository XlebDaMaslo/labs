import numpy as np
import matplotlib.pyplot as plt

A = 1
f = 5
phi = 0
T = 1 / f 
Ts = 0.01

t = np.arange(-0.1, 0.1, Ts)

# Формирование гармонического колебания
s = A * np.cos(2 * np.pi * f * t + phi)

# Опорные колебания
sc = np.cos(2 * np.pi * f * t)
ss = np.sin(2 * np.pi * f * t)

# Интегрирование
m1 = s * sc
m2 = s * ss



n_max = 20

a0 = (1 / T) * np.trapezoid(s, t)
an = np.zeros(n_max + 1)
bn = np.zeros(n_max + 1)
x_t = a0

for n in range(1, n_max + 1):
    an[n] = (2 / T) * np.trapezoid(s * np.cos(2 * np.pi * n * f * t), t)
    bn[n] = (2 / T) * np.trapezoid(s * np.sin(2 * np.pi * n * f * t), t)

plt.plot(t, s, label='x(t)')
plt.plot(t, sc, label='cos(2πft)')
plt.plot(t, m1, label='s * cos(2πft)')
plt.ylim(-2, 2)
plt.title('Гармоническое колебание и опорные колебания')
plt.xlabel('Время (t)')
plt.ylabel('Амплитуда')
plt.legend()
plt.grid()
plt.show()

An = np.sqrt(an**2 + bn**2)
phi_n = -np.arctan(bn, an)

n_values = np.arange(0, n_max + 1)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.stem(n_values, An, basefmt=" ")
plt.title('Коэффициенты An')
plt.xlabel('n')
plt.ylabel('An')
plt.grid()

plt.subplot(1, 2, 2)
plt.stem(n_values, phi_n, basefmt=" ")
plt.title('Фаза φ(n)')
plt.xlabel('n')
plt.ylabel('φ(n) (радианы)')
plt.grid()


plt.tight_layout()
plt.show()
