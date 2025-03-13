import numpy as np
import matplotlib.pyplot as plt
from math import pi

def generate_bit_sequence(length):
    return np.random.randint(0, 2, length)

def psk_modulate(bits, m):
    symbol_map = np.exp(1j * 2 * pi * np.arange(m) / m)
    symbols = []
    bits = list(bits)
    
    while bits:
        if m == 2: # 2PSK
            index = bits.pop(0)
            symbols.append(symbol_map[index])
        elif m == 4 and len(bits) >= 2: # 4PSK
            bits_pair = bits.pop(0), bits.pop(0)
            index = bits_pair[0] * 2 + bits_pair[1]
            symbols.append(symbol_map[index])
        elif m == 16 and len(bits) >= 4: # 16PSK
            bits_quartet = [bits.pop(0) for _ in range(4)]
            index = (bits_quartet[0] * 8 + bits_quartet[1] * 4 + bits_quartet[2] * 2 + bits_quartet[3])
            symbols.append(symbol_map[index])
        else:
            break
    return np.array(symbols)

def add_awgn(signal, sigma):
    noise = np.random.normal(0, sigma, len(signal)) + 1j * np.random.normal(0, sigma, len(signal))
    return signal + noise

def psk_demodulate(received_signal, m, expected_bits_len):
    received_bits = []
    for symbol in received_signal:
        if m == 2: # 2PSK
           received_bits.append(0 if symbol.real > 0 else 1)
        elif m == 4: # 4PSK
            phase = np.angle(symbol)
            phase = (phase + 2*pi) % (2*pi)
            index = round(phase / (2*pi) * 4) % 4
            received_bits.extend([index // 2, index % 2])
        elif m == 16: # 16PSK
            phase = np.angle(symbol)
            phase = (phase + 2*pi) % (2*pi)
            index = round(phase / (2 * pi) * 16) % 16
            received_bits.extend([index // 8, (index % 8) // 4, (index % 4) // 2, index % 2])
    return np.array(received_bits, dtype=int)[:expected_bits_len]

def calculate_ber(original_bits, demodulated_bits):
    return np.sum(original_bits != demodulated_bits) / len(original_bits)

def plot_modulated_signal(signal, title, sample_rate=100):
    time = np.arange(len(signal)) / sample_rate  # Создаем временную шкалу
    plt.figure(figsize=(10, 4))
    plt.plot(time, np.angle(signal), linestyle='-')
    plt.xlabel("Time")
    plt.ylabel("Phase (rad)")
    plt.title(title)
    plt.grid(True)

def plot_ber_vs_sigma(sigmas, ber_values, title, ax, label):
    ax.plot(sigmas, ber_values, marker='o', linestyle='-', label=label)
    ax.set_xlabel("Sigma")
    ax.set_ylabel("Bit Error Rate")
    ax.set_title(title)
    ax.set_yscale('log')
    ax.grid(True)
    ax.legend()


if __name__ == "__main__":
    num_bits = 1000
    sigmas = np.linspace(0, 2, 100)
    modulations = [2, 4, 16]
    ber_results = {m: [] for m in modulations}

    fig, ax = plt.subplots(figsize=(10, 6))

    for i, m in enumerate(modulations):
        original_bits = generate_bit_sequence(num_bits)
        modulated_signal = psk_modulate(original_bits.copy(), m)
        
        plot_modulated_signal(modulated_signal, f"{m}PSK Modulated Signal")
        
        for sigma in sigmas:
            noisy_signal = add_awgn(modulated_signal, sigma)
            demodulated_bits = psk_demodulate(noisy_signal, m, len(original_bits))
            ber = calculate_ber(original_bits, demodulated_bits)
            ber_results[m].append(ber)

    for m in modulations:
        plot_ber_vs_sigma(sigmas, ber_results[m], "BER vs Sigma", ax, f"{m}PSK")

    plt.tight_layout()
    plt.show()