import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

f = 5
T = 1 / f
Ts = 0.01

t = np.arange(-0.1, 0.1, Ts)

s = 2 * np.cos(2 * np.pi * f * t)
sc = np.cos(2 * np.pi * f * t)
ss = np.sin(2 * np.pi * f * t)

m1 = s * sc
m2 = s * ss

plt.subplot(2, 1, 1)
plt.plot(t, s, label='s')
plt.plot(t, ss, label='ss')
plt.plot(t, sc, label='sc')
plt.plot(t, m1, label='m1')
plt.plot(t, m2, label='m2')
plt.ylim(-2, 2)
plt.grid() 
plt.legend()


a0 = (1 / T) * np.sum(m1) * Ts
print("Amplitude (a1):", a0)

plt.subplot(2, 1, 2)
x = a0 + m1 + m2
plt.plot(t, x)
plt.grid()
plt.show()
