import numpy as np
import matplotlib.pyplot as plt

A1 = 8
A2 = 5
f = 5
d = 1
fd = 1000
t = np.linspace(0, d, int(d * fd))

ph1 = np.pi/3
ph2 = (4*np.pi)/3

x1 = A1*np.sin(2 * np.pi * f * t + ph1)
x2 = A2*np.sin(2 * np.pi * f * t + ph2)
x3 = x1 + x2


plt.plot(t,x3)
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.title("A1={}V, A2={}V ,F={} Hz, $\phi1={}^\circ$, $\phi2={}^\circ$".format(A1,A2,f,ph1,ph2))

plt.show()
