import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 5, 1000)
A = 5
f = 5
ph = 0

x = A * np.sin(2 * np.pi * f * t + ph)

plt.plot(t,x)
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.title("A={}V ,F={} Hz, $\phi={}^\circ$".format(A,f,ph))

plt.show()
