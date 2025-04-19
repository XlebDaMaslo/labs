import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Параметры
fs = 500  # Частота дискретизации, Гц
N = 10000  # Количество отсчетов

# Генерация белого шума
np.random.seed(42)
white_noise = np.random.normal(0, 1, N)

# Коэффициенты фильтра для УзкоПолосного Случайного Процесса
b = [1]
a = [1, -0.9]

# Генерация узкополосного случайного процесса
up_sp = signal.lfilter(b, a, white_noise)

# Функция для вычисления АКФ
def compute_acf(x, max_lag):
    acf = np.correlate(x, x, mode='full') / len(x)
    return acf[len(x)-1:len(x)+max_lag]  # Положительные лаги

# Вычисление АКФ УП СП
max_lag = 100
acf_up_sp = compute_acf(up_sp, max_lag)

# Вычисление СПМ УП СП
f_up_sp, psd_up_sp = signal.welch(up_sp, fs=fs, nperseg=1024)

# Импульсная характеристика канала
chnl = np.array([0.112873323983817 + 0.707197839105975j,
                 0.447066470535225 - 0.375487664593309j,
                 0.189507622364489 - 0.132430466488543j,
                 0.111178811342494 - 0.0857241111225552j])

# Генерация выходного сигнала канала
output_signal = signal.convolve(up_sp, chnl, mode='same')

# Вычисление ККФ между входным и выходным сигналами
ccf = signal.correlate(up_sp, output_signal, mode='full') / len(up_sp)
lags = np.arange(-len(up_sp)+1, len(up_sp))

# Обработка комплексных значений ККФ
ccf_real = np.real(ccf)  # Действительная часть ККФ
ccf_abs = np.abs(ccf)    # Модуль ККФ

# Визуализация
plt.figure(figsize=(15, 10))

# АКФ УП СП
plt.subplot(3, 1, 1)
plt.plot(np.arange(max_lag+1), acf_up_sp)
plt.title('АКФ УП СП')
plt.xlabel('Лаг')
plt.ylabel('АКФ')

# СПМ УП СП
plt.subplot(3, 1, 2)
plt.semilogy(f_up_sp, psd_up_sp)
plt.title('СПМ УП СП')
plt.xlabel('Частота (Гц)')
plt.ylabel('СПМ')

# ККФ (действительная часть или модуль)
plt.subplot(3, 1, 3)
plt.plot(lags, ccf_real, label='Действительная часть')
plt.plot(lags, ccf_abs, label='Модуль')
plt.title('ККФ между входом и выходом канала')
plt.xlabel('Лаг')
plt.ylabel('ККФ')
plt.legend()

plt.tight_layout()
plt.show()