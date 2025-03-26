import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Параметры
fs = 24000  # Частота дискретизации (Гц)
t = np.arange(0, 0.1, 1/fs)  # Временной вектор длительностью 0.1 с
N = len(t)  # Количество отсчетов

### Генерация белого шума
np.random.seed(42)
white_noise = np.random.normal(0, 1, N)  # Белый шум с нормальным распределением

### Фильтры
# ФНЧ - эллиптический фильтр
order = 6  # Порядок фильтра
rp = 0.5   # Неравномерность в полосе пропускания, дБ
rs = 50    # Подавление в полосе заграждения, дБ
fc_lpf = 3000  # Частота среза ФНЧ, Гц
b_lpf, a_lpf = signal.ellip(order, rp, rs, fc_lpf/(fs/2), btype='low', output='ba')

# ПФ - эллиптический фильтр
f1 = 3000  # Нижняя частота среза ПФ (Гц)
f2 = 6000  # Верхняя частота среза ПФ (Гц)
b_bpf, a_bpf = signal.ellip(order, rp, rs, [f1/(fs/2), f2/(fs/2)], btype='band', output='ba')

# Фильтрация белого шума
filtered_lpf = signal.lfilter(b_lpf, a_lpf, white_noise)  # Выход ФНЧ
filtered_bpf = signal.lfilter(b_bpf, a_bpf, white_noise)  # Выход ПФ

# Вычисление АКФ и СПМ для входного белого шума
acf_white = np.correlate(white_noise, white_noise, mode='full') / N  # Полная АКФ белого шума
lags = np.arange(-N+1, N)  # Лаги от -N+1 до N-1
f_white, psd_white = signal.welch(white_noise, fs, nperseg=1024)  # СПМ белого шума

# Усреднение АКФ и СПМ по 1000 реализациям для ФНЧ и ПФ
num_realizations = 1000
acf_lpf_avg = np.zeros(2*N-1)  # От -N+1 до N-1
acf_bpf_avg = np.zeros(2*N-1)
psd_lpf_avg = np.zeros(513)
psd_bpf_avg = np.zeros(513)

for _ in range(num_realizations):
    # Генерация новой реализации белого шума
    white_noise = np.random.normal(0, 1, N)
    filtered_lpf = signal.lfilter(b_lpf, a_lpf, white_noise)
    filtered_bpf = signal.lfilter(b_bpf, a_bpf, white_noise)
    
    # Вычисление АКФ
    acf_lpf = np.correlate(filtered_lpf, filtered_lpf, mode='full') / N
    acf_bpf = np.correlate(filtered_bpf, filtered_bpf, mode='full') / N
    acf_lpf_avg += acf_lpf
    acf_bpf_avg += acf_bpf
    
    # Вычисление СПМ
    f_lpf, psd_lpf = signal.welch(filtered_lpf, fs, nperseg=1024)
    f_bpf, psd_bpf = signal.welch(filtered_bpf, fs, nperseg=1024)
    psd_lpf_avg += psd_lpf
    psd_bpf_avg += psd_bpf

# Усреднение
acf_lpf_avg /= num_realizations
acf_bpf_avg /= num_realizations
psd_lpf_avg /= num_realizations
psd_bpf_avg /= num_realizations

# Интервал корреляции для ФНЧ
max_acf_lpf = np.max(acf_lpf_avg)  # Максимальное значение АКФ
threshold = 0.05 * max_acf_lpf  # Порог 5% от максимума
tau_corr_idx = np.where(acf_lpf_avg[N-1:] < threshold)[0][0]
tau_corr = tau_corr_idx / fs  # В секундах

plt.figure(figsize=(12, 8))

# АКФ белого шума
plt.subplot(3, 2, 1)
plt.plot(lags, acf_white)
plt.title('АКФ белого шума')
plt.xlabel('Лаг')
plt.ylabel('АКФ')

# СПМ белого шума
plt.subplot(3, 2, 2)
plt.plot(f_white, psd_white)
plt.title('СПМ белого шума')
plt.xlabel('Частота (Гц)')
plt.ylabel('СПМ')

# АКФ на выходе ФНЧ
plt.subplot(3, 2, 3)
plt.plot(lags, acf_lpf_avg)
plt.title('АКФ на выходе ФНЧ')
plt.xlabel('Лаг')
plt.ylabel('АКФ')

# СПМ на выходе ФНЧ
plt.subplot(3, 2, 4)
plt.plot(f_lpf, psd_lpf_avg)
plt.title('СПМ на выходе ФНЧ')
plt.xlabel('Частота (Гц)')
plt.ylabel('СПМ')

# АКФ на выходе ПФ
plt.subplot(3, 2, 5)
plt.plot(lags, acf_bpf_avg)
plt.title('АКФ на выходе ПФ')
plt.xlabel('Лаг')
plt.ylabel('АКФ')

# СПМ на выходе ПФ
plt.subplot(3, 2, 6)
plt.plot(f_bpf, psd_bpf_avg)
plt.title('СПМ на выходе ПФ')
plt.xlabel('Частота (Гц)')
plt.ylabel('СПМ')

plt.tight_layout()

print(f"Интервал корреляции на выходе ФНЧ: {tau_corr:.4f} с")

plt.show()