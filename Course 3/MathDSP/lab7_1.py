import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc

def Q(x):
    return 0.5 * erfc(x / np.sqrt(2))

# Параметры
N_bits = 50000
fs = 1000
ts = 1 / fs
L = 100
t = np.arange(L) * ts
T_symbol = L * ts

# Амплитуда и частоты
U = 1.0
fc = 100
f1 = 120
f0 = 80

# Образцы
cs_am1 = U * np.cos(2 * np.pi * fc * t)
cs_am0 = -cs_am1
cs_fm1 = np.cos(2 * np.pi * f1 * t)
cs_fm0 = np.cos(2 * np.pi * f0 * t)

# Теоретические BER
SNR_dB = np.arange(0, 16)
gamma = 10 ** (SNR_dB / 10)
BER_th_am = Q(np.sqrt(2 * gamma))
BER_th_fm = Q(np.sqrt(gamma))

bits = np.random.randint(0, 2, N_bits)

# Мощности и энергии
P_am = np.mean(cs_am1**2)
P_fm = np.mean(cs_fm1**2)
E_am = P_am * T_symbol
E_fm = P_fm * T_symbol

BER_sim_am = np.zeros_like(gamma)
BER_sim_fm = np.zeros_like(gamma)

# Цикл по SNR
for idx, g in enumerate(gamma):
    N0_am = E_am / g
    N0_fm = E_fm / g
    sigma_am = np.sqrt(N0_am * fs / 2)
    sigma_fm = np.sqrt(N0_fm * fs / 2)

    # Модулированные сигналы
    s_am = np.where(bits[:, None] == 1, cs_am1, cs_am0)
    s_fm = np.where(bits[:, None] == 1, cs_fm1, cs_fm0)

    # Добавление шума
    r_am = s_am + np.random.normal(0, sigma_am, s_am.shape)
    r_fm = s_fm + np.random.normal(0, sigma_fm, s_fm.shape)

    # Корреляционный приём
    sr_am1 = ts * np.sum(r_am * cs_am1, axis=1)
    sr_am0 = ts * np.sum(r_am * cs_am0, axis=1)
    # Для разности кореляторов и порога Vt=0
    sr_am = sr_am1 - sr_am0
    dec_am = (sr_am > 0).astype(int)

    sr_fm1 = ts * np.sum(r_fm * cs_fm1, axis=1)
    sr_fm0 = ts * np.sum(r_fm * cs_fm0, axis=1)
    sr_fm = sr_fm1 - sr_fm0
    # Порог для ФМ Vt=0
    dec_fm = (sr_fm > 0).astype(int)

    # Подсчёт BER
    BER_sim_am[idx] = np.mean(dec_am != bits)
    BER_sim_fm[idx] = np.mean(dec_fm != bits)

print("Симулированная BER ДАМ:", BER_sim_am)
print("Симулированная BER ДФМ:", BER_sim_fm)

plt.figure(figsize=(8, 6))
plt.semilogy(SNR_dB, BER_sim_am, 'o', label='ДАМ (моделирование)')
plt.semilogy(SNR_dB, BER_sim_fm, 's', label='ДФМ (моделирование)')
plt.semilogy(SNR_dB, BER_th_am, '-', label='ДАМ (теория)')
plt.semilogy(SNR_dB, BER_th_fm, '--', label='ДФМ (теория)')
plt.xlabel('SNR, дБ')
plt.ylabel('BER')
plt.title('Помехоустойчивость ДАМ и ДФМ')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()
plt.tight_layout()
plt.show()
