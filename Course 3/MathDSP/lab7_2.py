import numpy as np
import matplotlib.pyplot as plt

# 1. Опорные последовательности
code1 = np.array([1, 1, 1, -1, 1])
code2 = np.array([1, 1, 1, -1, -1, 1, -1])
code3 = np.array([1, -1, 1, 1, -1, 1, 1, 1, -1, -1, -1, -1])

# 2. Импульсные характеристики согласованного фильтра
h1 = code1[::-1]

# 3. Функция вывода отклика фильтра
def plot_response(signal, h, label, ax):
    y = np.convolve(signal, h)
    ax.plot(y, label=label)
    # Установка общих атрибутов для каждого подграфика внутри функции
    ax.set_xlabel('Отсчёт')
    ax.set_ylabel('Амплитуда')
    ax.legend()
    ax.grid(True)

fig, axes = plt.subplots(3, 1, figsize=(8, 12))

# Без шума и искажений
plot_response(code1, h1, 'matched (code1)', axes[0])
plot_response(code2, h1, 'mismatch (code2)', axes[0])
plot_response(-code1, h1, 'inverted (code1)', axes[0])
axes[0].set_title('Отклики согласованного фильтра (без искажений)')


# 4. Искажение одного элемента в code1
code1_dist = code1.copy()
code1_dist[2] *= -1  # смена знака центрального элемента

plot_response(code1, h1, 'оригинал', axes[1])
plot_response(code1_dist, h1, 'искажённый (один бит)', axes[1])
axes[1].set_title('Влияние искажения одного элемента')


# 5. Влияние аддитивного шума
SNR_dB_list = [0, 5, 10]
signal_clean = code1.astype(float)
power_signal = np.mean(signal_clean**2)

for snr_db in SNR_dB_list:
    snr_lin = 10**(snr_db / 10)
    # Проверка на нулевую мощность сигнала
    if power_signal > 1e-10:
         noise_var = power_signal / snr_lin
    else:
         noise_var = 1.0
         print(f"Предупреждение: Мощность сигнала близка к нулю. Установлена дисперсия шума={noise_var}")

    noise = np.random.normal(0, np.sqrt(noise_var), size=signal_clean.shape)
    noisy_signal = signal_clean + noise
    plot_response(noisy_signal, h1, f'SNR={snr_db} дБ', axes[2])
axes[2].set_title('Отклик при шуме')

plt.tight_layout()

plt.show()