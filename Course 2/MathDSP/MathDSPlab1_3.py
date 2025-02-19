import numpy as np
import matplotlib.pyplot as plt

f = 3
A1 = 2
phi1 = np.pi/2
A2 = 5
phi2 = 3*np.pi/4
A3 = 0.5
phi3 = 5*np.pi/3

t = np.linspace(0, 2, 1000)

x1 = A1 * np.cos(2 * np.pi * f * t + phi1)
x2 = A2 * np.cos(2 * np.pi * f * t + phi2)
x3 = A3 * np.cos(2 * np.pi * f * t + phi3)

x_sum = x1 + x2 + x3

plt.plot(t, x1, label='x1')
plt.plot(t, x2, label='x2')
plt.plot(t, x3, label='x3')
plt.plot(t, x_sum, label='x1 + x2 + x3')
plt.xlabel('Время')
plt.ylabel('Амплитуда')
plt.legend()
plt.grid(True)
plt.show()