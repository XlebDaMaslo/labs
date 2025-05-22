import numpy as np
import matplotlib.pyplot as plt

### 1
G = np.array([
    [1, 0, 0, 0, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 1],
    [0, 0, 1, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 1, 1]
])

H = np.array([
    [1, 1, 0, 1, 1, 0, 0],
    [1, 0, 1, 1, 0, 1, 0],
    [0, 1, 1, 1, 0, 0, 1]
])

info_vectors = []
for i in range(16):
    bin_str = format(i, '04b')
    vec = [int(bit) for bit in bin_str]
    info_vectors.append(vec)

code_words = []
for u in info_vectors:
    c = np.zeros(7, dtype=int)
    for i in range(4):
        if u[i]:
            c = (c + G[i]) % 2
    code_words.append(c)

print("Таблица разрешенных кодовых слов кода Хэмминга (7,4):")
print("Информационные биты : Кодовый вектор")
for i in range(16):
    print(f"{info_vectors[i]} : {code_words[i]}")

print("\nПроверочная матрица H:")
for row in H:
    print(row)

GHt = np.dot(G, H.T) % 2
print("\nПроверка GH^T:")
print(GHt)



### 2
errors = []
for i in range(7):
    e = np.zeros(7, dtype=int)
    e[i] = 1
    errors.append(e)

syndromes = []
for e in errors:
    s = (H @ e) % 2
    syndromes.append(s)

print("Таблица синдромов ошибок:")
print("Вектор ошибки : Синдром")
for i in range(7):
    print(f"{errors[i]} : {syndromes[i]}")



### 3
syndrome_table = {
    (1, 1, 0): 0,
    (1, 0, 1): 1,
    (0, 1, 1): 2,
    (1, 1, 1): 3,
    (1, 0, 0): 4,
    (0, 1, 0): 5,
    (0, 0, 1): 6
}

def hamming_encode(u):
    # Кодирование информационного вектора u (4 бита) в кодовое слово (7 бит)
    return (G.T @ u) % 2

def hamming_decode(r_bits):
    #Декодирование принятого вектора r_bits (7 бит) с исправлением одиночной ошибки
    s = (H @ r_bits) % 2
    s_tuple = tuple(s)
    if s_tuple in syndrome_table:
        idx = syndrome_table[s_tuple]
        r_bits[idx] ^= 1  # Исправление ошибки
    return r_bits[:4]

def bpsk_modulate(bits):
    # Модуляция битов в BPSK символы (+1/-1)
    return 1 - 2 * bits

def bpsk_demodulate(received_signal):
    # Демодуляция BPSK сигналов в биты (жесткие решения)
    return (received_signal <= 0).astype(int)

def calculate_sigma(EbN0_dB):
    # Вычисление дисперсии шума для заданного Eb/N0 в дБ
    k = 4
    n = 7
    EbN0_linear = 10 ** (EbN0_dB / 10)
    EcN0_linear = EbN0_linear * (k / n)
    sigma = np.sqrt(1 / (2 * EcN0_linear))
    return sigma

def simulate_ecc_performance(EbN0_dB_values, num_trials):
    ber = []
    for EbN0 in EbN0_dB_values:
        sigma = calculate_sigma(EbN0)
        error_count = 0
        total_bits = 0
        for _ in range(num_trials):
            # Генерация случайного информационного вектора (4 бита)
            u = np.random.randint(0, 2, 4)
            # Кодирование
            c = hamming_encode(u)
            # BPSK модуляция
            s = bpsk_modulate(c)
            # Добавление шума
            noise = sigma * np.random.randn(7)
            r = s + noise
            # Демодуляция
            r_bits = bpsk_demodulate(r)
            # Декодирование
            decoded_u = hamming_decode(r_bits)
            # Подсчет ошибок
            error_count += np.sum(u != decoded_u)
            total_bits += 4
        ber.append(error_count / total_bits)
    return ber

# Параметры моделирования
EbN0_dB_values = np.arange(0, 10, 1)
num_trials = 10000  # Увеличьте для более точных результатов
ber = simulate_ecc_performance(EbN0_dB_values, num_trials)

# Построение графика
plt.semilogy(EbN0_dB_values, ber, 'o-', label='Код Хэмминга (7,4)')
plt.xlabel('Eb/N0 (dB)')
plt.ylabel('Вероятность битовой ошибки (BER)')
plt.title('BER для кода Хэмминга (7,4) с BPSK и жестким декодированием')
plt.grid(True)
plt.legend()
plt.show()



### 4
import numpy as np
import matplotlib.pyplot as plt

def generate_code_words():
    info_vectors = [np.array([int(b) for b in format(i, '04b')]) for i in range(16)]
    code_words = []
    for u in info_vectors:
        c = (G @ u) % 2
        code_words.append(c)
    return np.array(code_words)

code_words = generate_code_words()
code_words_bpsk = 1 - 2 * code_words  # 16x7 матрица BPSK символов

def calculate_sigma(EbN0_dB):
    k, n = 4, 7
    EbN0_linear = 10 ** (EbN0_dB / 10)
    EcN0_linear = EbN0_linear * (k / n)  # Учет избыточности кода
    sigma = np.sqrt(1 / (2 * EcN0_linear))  # σ² = N0/2
    return sigma

def soft_decode(received_signal):
    distances = np.sum((received_signal[None, :, :] - code_words_bpsk[:, None, :]) ** 2, axis=2)
    min_indices = np.argmin(distances, axis=0)
    decoded_cw = code_words_bpsk[min_indices]
    return (decoded_cw[:, :4] == -1).astype(int)

def simulate_ecc_performance(EbN0_dB_values, num_trials):
    ber = []
    for EbN0 in EbN0_dB_values:
        sigma = calculate_sigma(EbN0)
        error_count = 0
        total_bits = 0
        
        # Генерация множества случайных информационных векторов
        u_batch = np.random.randint(0, 2, size=(num_trials, 4))
        
        # Кодирование всех информационных векторов
        c_indices = [int(''.join(map(str, u)), 2) for u in u_batch]
        s_batch = code_words_bpsk[c_indices]
        
        # Добавление шума
        noise = sigma * np.random.randn(num_trials, 7)
        r_batch = s_batch + noise
        
        # Мягкое декодирование
        decoded_u_batch = soft_decode(r_batch)
        
        # Подсчет ошибок
        error_count += np.sum(u_batch != decoded_u_batch)
        total_bits += num_trials * 4
        
        ber.append(error_count / total_bits)
    return ber

EbN0_dB_values = np.arange(0, 10, 1)
num_trials = 10000

ber = simulate_ecc_performance(EbN0_dB_values, num_trials)

plt.semilogy(EbN0_dB_values, ber, 'o-', label='Код Хэмминга (7,4) с мягким декодированием')
plt.xlabel('Eb/N0 (dB)')
plt.ylabel('Вероятность битовой ошибки (BER)')
plt.title('BER для кода Хэмминга (7,4) с BPSK и мягким декодированием')
plt.grid(True)
plt.legend()
plt.show()