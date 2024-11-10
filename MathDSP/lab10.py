import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
x = ([1, 2, 3, 0.5])
h = ([1, 0.3679, 0.1353, 0.0498])

y = ([])

for n in range(len(x) + len(h) - 1):
    sum_val = 0
    for k in range(len(x)):
        if 0 <= n - k < len(h):
            sum_val += x[k] * h[n - k]
    y.append(sum_val)
print(y)

plt.figure(figsize=(10, 8))

plt.subplot(3, 1, 1)
plt.stem(x, use_line_collection=True)
plt.title('Входной сигнал x(n)')
plt.xlabel('n')
plt.ylabel('x(n)')

plt.subplot(3, 1, 2)
plt.stem(h, use_line_collection=True)
plt.title('Импульсная характеристика h(n)')
plt.xlabel('n')
plt.ylabel('h(n)')


plt.subplot(3, 1, 3)
plt.stem(y, use_line_collection=True)
plt.title('Выходной сигнал y(n)')
plt.xlabel('n')
plt.ylabel('y(n)')

plt.tight_layout()
plt.show()

y= np.convolve(x,h)
plt.figure(1)
plt.stem(y)
plt.figure(2) 
w,hw=signal.freqz(h,whole=1)
plt.plot(w,20*np.log10(abs(hw)),'b')
plt.show()