import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 1, 100)
A = 1
f = 5
phi = [0, 128, 256, 360]

for i in range(len(phi)):
    x = A * np.sin(2 * np.pi * f * t + phi[i] * np.pi / 180)
    plt.subplot(2, 2, i + 1)
    plt.plot(t, x)
    plt.xlabel('Time (t)')
    plt.ylabel('Amplitude (V)')
    plt.title(r'$\Phi ={}^\circ$'.format(phi[i]))

plt.tight_layout()
plt.show()
