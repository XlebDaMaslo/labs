import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc

def Q(x):
    return 0.5 * erfc(x / np.sqrt(2))

# Параметры моделирования
N_bits = 10000         # число переданных символов
fs = 1000              # частота дискретизации (Гц)
L = 100                # число отсчетов на символ
t = np.arange(L) / fs  # вектор времени для одного символа
Ts = 1 / fs            # длительность отсчета (с)

# Параметры несущих
fc = 100               # частота для AM (Гц)
f1 = 120               # частота для FM при бит=1 (Гц)
f0 = 80                # частота для FM при бит=0 (Гц)

cs_am1 = np.cos(2 * np.pi * fc * t)
cs_am0 = -cs_am1
cs_fm1 = np.cos(2 * np.pi * f1 * t)
cs_fm0 = np.cos(2 * np.pi * f0 * t)

# Диапазон SNR
SNR_dB = np.arange(0, 16)
gamma_lin = 10 ** (SNR_dB / 10)

# Теоретические BER
BER_th_am = Q(np.sqrt(2 * gamma_lin))
BER_th_fm = Q(np.sqrt(gamma_lin))

# Генерация случайных бит
bits = np.random.randint(0, 2, size=N_bits)

# Средняя мощность и энергия символа
P_am = np.mean(cs_am1 ** 2)
E_am = P_am * (L / fs)
P_fm = np.mean(cs_fm1 ** 2)
E_fm = P_fm * (L / fs)

BER_sim_am = np.zeros_like(gamma_lin)
BER_sim_fm = np.zeros_like(gamma_lin)

for idx, gamma in enumerate(gamma_lin):
    # Расчёт спектральной плотности и дисперсии шума
    N0_am = E_am / gamma
    N0_fm = E_fm / gamma
    sigma_am = np.sqrt(N0_am * fs / 2)
    sigma_fm = np.sqrt(N0_fm * fs / 2)

    s_am = cs_am1 * bits[:, None] + cs_am0 * (1 - bits)[:, None]
    s_fm = cs_fm1 * bits[:, None] + cs_fm0 * (1 - bits)[:, None]

    noise_am = np.random.normal(0, sigma_am, size=s_am.shape)
    noise_fm = np.random.normal(0, sigma_fm, size=s_fm.shape)
    cs_am_n = s_am + noise_am
    cs_fm_n = s_fm + noise_fm

    # Корреляционный приём
    sr_am1 = Ts * np.sum(cs_am_n * cs_am1, axis=1)
    sr_am0 = Ts * np.sum(cs_am_n * cs_am0, axis=1)
    sr_am = sr_am1 - sr_am0

    sr_fm1 = Ts * np.sum(cs_fm_n * cs_fm1, axis=1)
    sr_fm0 = Ts * np.sum(cs_fm_n * cs_fm0, axis=1)
    sr_fm = sr_fm1 - sr_fm0

    decisions_am = (sr_am > 0).astype(int)
    decisions_fm = (sr_fm > 0).astype(int)

    # Подсчёт ошибок
    BER_sim_am[idx] = np.mean(decisions_am != bits)
    BER_sim_fm[idx] = np.mean(decisions_fm != bits)

# Вывод симулированных BER
print("Симулированная BER AM:", BER_sim_am)
print("Симулированная BER FM:", BER_sim_fm)

# Построение графика зависимости BER от SNR
plt.figure(figsize=(8, 6))
plt.semilogy(SNR_dB, BER_sim_am, 'o', label='AM (моделирование)')
plt.semilogy(SNR_dB, BER_sim_fm, 's', label='FM (моделирование)')
plt.semilogy(SNR_dB, BER_th_am, '-', label='AM (теория)')
plt.semilogy(SNR_dB, BER_th_fm, '--', label='FM (теория)')
plt.xlabel('Отношение сигнал/шум (дБ)')
plt.ylabel('Вероятность ошибки')
plt.title('BER AM и FM корреляционного приёма')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()
plt.tight_layout()
plt.show()
