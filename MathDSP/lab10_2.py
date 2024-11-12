import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

## 1 Вычисление ДВПФ
n1 = np.arange(0, 10)
n2 = np.arange(0, 50)

x1_10 =  3 + np.sin(n1 * 3 * np.pi / 4)
x2_10 = np.sin(0.2 * np.pi * n1) / (0.1 * np.pi * n1)
x3_10 = np.exp(-1.2 * n1)

x1_50 =  3 + np.sin(n2 * 3 * np.pi / 4)
x2_50 = np.sin(0.2 * np.pi * n2) / (0.1 * np.pi * n2)
x3_50 = np.exp(-1.2 * n2)

# Вычисление ДВПФ для случая 10 отсчетов
w1_10, x1w_10 = signal.freqz(x1_10, 1, whole=1)
w2_10, x2w_10 = signal.freqz(x2_10, 1, whole=1)
w3_10, x3w_10 = signal.freqz(x3_10, 1, whole=1)

# Вычисление ДВПФ для случая 50 отсчетов
w1_50, x1w_50 = signal.freqz(x1_50, 1, whole=1)
w2_50, x2w_50 = signal.freqz(x2_50, 1, whole=1)
w3_50, x3w_50 = signal.freqz(x3_50, 1, whole=1)

