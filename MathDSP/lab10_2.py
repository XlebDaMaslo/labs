import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

## 1 Вычисление ДВПФ
n1 = np.arange(0, 10)
n2 = np.arange(0, 50)

x1_10 =  3 + np.sin(n1 * 3 * np.pi / 4)
x2_10 = np.zeros_like(n1, dtype=float)
x2_10[n1 != 0] = np.sin(0.2 * np.pi * n1[n1 != 0]) / (0.1 * np.pi * n1[n1 != 0])
x2_10[n1 == 0] = 1
x3_10 = np.exp(-1.2 * n1)

x1_50 =  3 + np.sin(n2 * 3 * np.pi / 4)
x2_50 = np.zeros_like(n2, dtype=float)
x2_50[n2 != 0] = np.sin(0.2 * np.pi * n2[n2 != 0]) / (0.1 * np.pi * n2[n2 != 0])
x2_50[n2 == 0] = 1
x3_50 = np.exp(-1.2 * n2)

# Вычисление ДВПФ для случая 10 отсчетов
w1_10, x1w_10 = signal.freqz(x1_10, 1, whole=1)
w2_10, x2w_10 = signal.freqz(x2_10, 1, whole=1)
w3_10, x3w_10 = signal.freqz(x3_10, 1, whole=1)

# Вычисление ДВПФ для случая 50 отсчетов
w1_50, x1w_50 = signal.freqz(x1_50, 1, whole=1)
w2_50, x2w_50 = signal.freqz(x2_50, 1, whole=1)
w3_50, x3w_50 = signal.freqz(x3_50, 1, whole=1)

## 2 Численная проверка свойств ДВПФ
# Линейность

x_sum_10 = x1_10 + x3_10
w_sum_10, x_sumw_10 = signal.freqz(x_sum_10, 1, whole=1)

x_sumw_check_10 = x1w_10 + x3w_10

plt.figure()
plt.plot(w_sum_10, np.abs(x_sumw_10), label='Спектр суммы сигналов (x1_10 + x3_10)')
plt.plot(w_sum_10, np.abs(x_sumw_check_10), '--', label='Сумма спектров (x1w_10 + x3w_10)')
plt.legend()
plt.title('Сравнение спектров суммы сигналов и суммы спектров')


# Частотный сдвиг

k = 0.3 * np.pi  # Сдвиг
x1_shifted_10 = x1_10 * np.exp(1j * k * n1)
w_shift_10, x1_shiftedw_10 = signal.freqz(x1_shifted_10, 1, whole=1)

plt.figure()
plt.plot(w1_10, np.abs(x1w_10), label='Оригинальный спектр')
plt.plot(w_shift_10, np.abs(x1_shiftedw_10), label='Смещенный спектр')
plt.legend()


# Временная задержка

n0 = 3  # количество отсчетов для задержки
x1_delayed_10 = x1_10 * np.exp(-1j * 2 * np.pi * n0 * n1 / len(n1))  # Задержка на n0 отсчетов
w_delay_10, x1_delayedw_10 = signal.freqz(x1_delayed_10, 1, whole=1)

plt.figure()
plt.subplot(2, 1, 1)
plt.plot(w1_10, np.angle(x1w_10), label='Оригинальный фазовый спектр')
plt.plot(w_delay_10, np.angle(x1_delayedw_10), label='Фазовый спектр с задержкой')
plt.legend()
plt.title("Влияние временной задержки на фазовый спектр")

plt.subplot(2, 1, 2)
plt.plot(w1_10, np.abs(x1w_10), label='Оригинальный амплитудный спектр')
plt.plot(w_delay_10, np.abs(x1_delayedw_10), label='Амплитудный спектр с задержкой')
plt.legend()
plt.title("Амплитудный спектр после временной задержки")

# ДВПФ свертки сигналов

y_10 = np.convolve(x1_10, x2_10, mode='full')
y_50 = np.convolve(x1_50, x2_50, mode='full')

w_y_10, yw_10 = signal.freqz(y_10, 1, whole=1)
w_y_50, yw_50 = signal.freqz(y_50, 1, whole=1)

prod_spectra_10 = x1w_10 * x2w_10
prod_spectra_50 = x1w_50 * x2w_50

plt.figure()
plt.subplot(2, 1, 1)
plt.plot(w_y_10, np.abs(yw_10), label='Спектр свертки (10 отсчетов)')
plt.plot(w_y_10, np.abs(prod_spectra_10), '--', label='Произведение спектров (10 отсчетов)')
plt.legend()
plt.title('Свертка сигналов и сравнение спектров (10 отсчетов)')

plt.subplot(2, 1, 2)
plt.plot(w_y_50, np.abs(yw_50), label='Спектр свертки (50 отсчетов)')
plt.plot(w_y_50, np.abs(prod_spectra_50), '--', label='Произведение спектров (50 отсчетов)')
plt.legend()
plt.title('Свертка сигналов и сравнение спектров (50 отсчетов)')

plt.tight_layout()
plt.show()