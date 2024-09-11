import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0, 2.001, 0.0001)

y = np.sin((12 * np.pi * 4 * t) + (np.pi / 11)) + np.sin(10 * np.pi * 4 * t)

plt.plot(t, y)
plt.xlabel('Время (s)')
plt.ylabel('Амплитуда')
plt.title('График сигнала')
plt.grid(True)
plt.show()
