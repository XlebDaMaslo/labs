import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc

# ============================
# Параметры моделирования
# ============================
N = 10**5             # количество бит (символов)
Fs = 1000             # частота дискретизации (отсчетов в секунду)
T_sym = 0.01          # длительность символа, сек
t_sym = np.linspace(0, T_sym, int(Fs * T_sym), endpoint=False)   # вектор отсчетов для одного символа

# Параметры несущей
fc = 200              # базовая несущая для BASK (Гц)

# --- Параметры для BASK (амплитудная модуляция) ---
A0 = 1.0              # амплитуда для бита 0
A1 = 2.0              # амплитуда для бита 1

# --- Параметры для BFSK (частотная модуляция) ---
fc0 = 200             # несущая для бита 0 (Гц)
fc1 = 240             # несущая для бита 1 (Гц)
A_fm = 1.0            # одинаковая амплитуда для BFSK

# Диапазон SNR в dB (от 0 до 15 дБ)
SNR_dB_range = np.arange(0, 16, 2)

# ============================
# Генерация последовательности битов
# ============================
bits = np.random.randint(0, 2, N)

# ============================
# Функции формирования сигналов
# ============================
def modulate_BASK(bits, t_sym, A0, A1, fc):
    """ Формирование сигнала BASK (амплитудная модуляция)
        Для каждого бита генерируется отрезок сигнала A*cos(2π·fc·t),
        где амплитуда A зависит от бита.
    """
    Ns = len(t_sym)
    signal = np.zeros(N * Ns)
    # Сохранить шаблоны (без шума) для корреляционного приемника
    template = np.cos(2 * np.pi * fc * t_sym)
    energy_template = np.sum(template**2)
    for i, b in enumerate(bits):
        A = A1 if b == 1 else A0
        signal[i*Ns:(i+1)*Ns] = A * template
    return signal, template, energy_template

def modulate_BFSK(bits, t_sym, fc0, fc1, A):
    """ Формирование сигнала BFSK (частотная модуляция)
        Для каждого бита генерируется отрезок сигнала cos(2π·f·t),
        где f = fc0 для 0 и f = fc1 для 1.
    """
    Ns = len(t_sym)
    signal = np.zeros(N * Ns)
    # Запомним шаблоны для обоих сигналов
    template0 = np.cos(2 * np.pi * fc0 * t_sym)
    template1 = np.cos(2 * np.pi * fc1 * t_sym)
    energy_template0 = np.sum(template0**2)
    energy_template1 = np.sum(template1**2)
    for i, b in enumerate(bits):
        f = fc1 if b == 1 else fc0
        signal[i*Ns:(i+1)*Ns] = A * np.cos(2 * np.pi * f * t_sym)
    return signal, template0, template1, energy_template0, energy_template1

# Модуляция
signal_BASK, template_am, E_t_am = modulate_BASK(bits, t_sym, A0, A1, fc)
signal_BFSK, template0_fm, template1_fm, E_t_fm0, E_t_fm1 = modulate_BFSK(bits, t_sym, fc0, fc1, A_fm)

# Определяем количество отсчетов на символ
Ns = len(t_sym)

# Функция для добавления шума с требуемым SNR
def add_AWGN(signal, SNR_dB):
    """ Добавление аддитивного белого гауссовского шума к сигналу.
        SNR_dB – отношение сигнал/шум в дБ.
        Мощность сигнала вычисляется по усреднению квадратов.
    """
    sig_power = np.mean(signal**2)
    SNR_linear = 10**(SNR_dB/10)
    noise_power = sig_power / SNR_linear
    noise = np.sqrt(noise_power) * np.random.randn(len(signal))
    return signal + noise

# ============================
# Моделирование приёмников и подсчет ошибок
# ============================
BER_sim_BASK = []
BER_sim_BFSK = []

# Для корреляционного приемника BASK: используем шаблон cos(2π·fc·t)
# Оптимальный порог (при известной энергии) равен половине суммы корреляционных результатов 
# для сигналов с амплитудами A0 и A1. Если E = energy(template), то
# decision threshold = (A0*E + A1*E)/2 = (A0+A1)*E/2.
threshold_am = (A0 + A1) * E_t_am / 2

for snr_db in SNR_dB_range:
    # Для BASK
    rx_BASK = add_AWGN(signal_BASK, snr_db)
    decisions_am = np.zeros(N, dtype=int)
    errors_am = 0
    for i in range(N):
        segment = rx_BASK[i*Ns:(i+1)*Ns]
        # Корреляционный интеграл
        corr = np.sum(segment * template_am)
        # Решающее правило: если интеграл больше порога, решаем 1, иначе 0
        decided_bit = 1 if corr > threshold_am else 0
        if decided_bit != bits[i]:
            errors_am += 1

    BER_sim_BASK.append(errors_am/N)

    # Для BFSK – корреляционный приемник с двумя фильтрами
    rx_BFSK = add_AWGN(signal_BFSK, snr_db)
    errors_fm = 0
    for i in range(N):
        segment = rx_BFSK[i*Ns:(i+1)*Ns]
        # Корреляционные интегралы с двумя шаблонами
        corr0 = np.sum(segment * template0_fm)
        corr1 = np.sum(segment * template1_fm)
        decided_bit = 1 if corr1 > corr0 else 0
        if decided_bit != bits[i]:
            errors_fm += 1

    BER_sim_BFSK.append(errors_fm/N)

# ============================
# Теоретические кривые вероятности ошибки
# ============================
# Для вычислений воспользуемся определенными формулами:
# AM: BER = Q(sqrt(2*gamma)) = 0.5*erfc(sqrt(2*gamma)/sqrt2) = 0.5*erfc(sqrt(gamma))
# BFSK: BER = Q(sqrt(gamma)) = 0.5*erfc( sqrt(gamma)/sqrt2 )
gamma_lin = 10**(SNR_dB_range/10)   # предполагаем, что gamma = Es/N0, а Es определяется мощностью сигнала
theory_BER_AM = 0.5 * erfc(np.sqrt(gamma_lin))
theory_BER_FM = 0.5 * erfc(np.sqrt(gamma_lin)/np.sqrt(2))

# ============================
# Построение графиков
# ============================
plt.figure(figsize=(8, 6))
plt.semilogy(SNR_dB_range, theory_BER_AM, 'b.-', label='Теоретическая BER BASK')
plt.semilogy(SNR_dB_range, BER_sim_BASK, 'mx-', label='Моделирование BASK')
plt.semilogy(SNR_dB_range, theory_BER_FM, 'g.-', label='Теоретическая BER BFSK')
plt.semilogy(SNR_dB_range, BER_sim_BFSK, 'ko-', label='Моделирование BFSK')
plt.xlabel('Отношение сигнал/шум, dB')
plt.ylabel('Вероятность ошибки')
plt.title('Зависимость вероятности ошибки от SNR для BASK и BFSK')
plt.grid(True, which='both')
plt.legend()
plt.ylim(1e-5, 1)
plt.show()
