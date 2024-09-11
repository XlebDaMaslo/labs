import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

#1
t_lim = 2
fd = 1000
t = np.arange(0, t_lim+(1/fd), (1/fd))
print(t)
f = 4

y = np.sin((12 * np.pi * f * t) + (np.pi / 11)) + np.sin(10 * np.pi * f * t)


plt.plot(t, y)
plt.xlabel('Время (s)')
plt.ylabel('Амплитуда')
plt.title('График сигнала')
plt.grid(True)
plt.show()

#2
spectr = fft(y)
f_arr = fftfreq(len(t), 1/fd)
a_spectr = np.abs(spectr) / len(t)

positive_fs = f_arr[:len(f_arr)//2]
positive_spectr = a_spectr[:len(a_spectr)//2]

max_idx = np.argmax(positive_spectr)
max_f = positive_fs[max_idx]

print(f'Максимальная частота в спектре: {round(max_f, 6)} Hz')

#3