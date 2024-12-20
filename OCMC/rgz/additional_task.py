import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lab4.lab4 import gen_gold_seq

import matplotlib.pyplot as plt
import numpy as np
from crc import Calculator, Configuration
import crc32c

STOP_WORD = "Stop"

def ascii_encoder(text):
    text += STOP_WORD
    encoded_bits = []
    for char in text:
        ascii_val = ord(char)
        binary_val = bin(ascii_val)[2:].zfill(8)
        encoded_bits.extend([int(bit) for bit in binary_val])
    return encoded_bits

def ascii_decoder(bits):
    text = ""
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        char_code = int("".join(map(str, byte)), 2)
        text += chr(char_code)

    stop_index = text.find(STOP_WORD)
    if stop_index != -1:
        text = text[:stop_index]
    return text

def expand_bits(bits, N):
    expanded_signal = []
    for bit in bits:
        expanded_signal.extend([bit] * N)
    return expanded_signal

def calculate_ber(original_bits, received_bits):
    errors = np.sum(np.array(original_bits) != np.array(received_bits))
    return errors / len(original_bits)

def decode_signal(signal, N, threshold=0.5):
    decoded_bits = []
    for i in range(0, len(signal), N):
        bit_chunk = signal[i:i + N]
        if np.mean(bit_chunk) >= threshold:
            decoded_bits.append(1)
        else:
            decoded_bits.append(0)
    return decoded_bits

def simulate_transmission(name, N, sigma, gold_sequence, crc_bits):
    encoded_data = ascii_encoder(name)
    transmitted_sequence = gold_sequence + encoded_data + crc_bits

    expanded_signal = expand_bits(transmitted_sequence, N)

    signal_length = 2 * N * len(transmitted_sequence)
    signal = np.zeros(signal_length)
    shift = 0
    signal[shift:shift + len(expanded_signal)] = expanded_signal
    noise = np.random.normal(0, sigma, len(signal))
    received_signal = signal + noise

    decoded_bits = decode_signal(received_signal, N)
    decoded_bits = decoded_bits[:len(gold_sequence) + len(encoded_data) + len(crc_bits)]

    received_data_bits = decoded_bits[len(gold_sequence):-len(crc_bits)]
    return encoded_data, received_data_bits, signal, received_signal

def plot_ber(sigma_values, ber_values, N):
    plt.plot(sigma_values, ber_values, label=f'Group Size: {N}')
    plt.xlabel("Sigma")
    plt.ylabel("Bit Error Rate")
    plt.grid(True)
    plt.legend()


def plot_signal_with_noise(signal, received_signal, N, sigma):
    plt.figure(figsize=(10, 4))
    plt.step(range(len(signal)), signal, where='post', label='Transmitted Signal')
    plt.step(range(len(received_signal)), received_signal, where='post', label=f'Received Signal with noise (σ = {sigma})')
    plt.title(f"Signal and Received Signal with Noise for N={N}")
    plt.xlabel("Bit Index")
    plt.ylabel("Signal Value")
    plt.grid(True)
    plt.legend()

if __name__ == "__main__":
    name = "Test text"

    encoded_data_bytes = bytes(int(''.join(map(str, ascii_encoder(name)[i:i + 8])), 2) for i in range(0, len(ascii_encoder(name)), 8))
    crc32c_checksum = crc32c.crc32c(encoded_data_bytes)
    crc_bits = list(map(int, bin(crc32c_checksum)[2:].zfill(8)))

    number_st = 10
    number_st2 = number_st + 7
    polynomial1_bin = "00011"
    polynomial2_bin = "01001"
    gold_sequence = gen_gold_seq(number_st, number_st2, polynomial1_bin, polynomial2_bin)

    sigma_values = np.linspace(0.1, 1, 10)

    ber_values_n1 = []
    ber_values_n2 = []
    ber_values_n4 = []
    
    num_iterations = 5

    for sigma in sigma_values:
        ber_n1_sum = 0
        ber_n2_sum = 0
        ber_n4_sum = 0
        for _ in range(num_iterations):
            # Для N=1
            encoded_data, received_data, _, _ = simulate_transmission(name, 1, sigma, gold_sequence, crc_bits)
            ber_n1_sum += calculate_ber(encoded_data, received_data)

            # Для N=2
            encoded_data, received_data, _, _ = simulate_transmission(name, 2, sigma, gold_sequence, crc_bits)
            ber_n2_sum += calculate_ber(encoded_data, received_data)

            # Для N=4
            encoded_data, received_data, _, _ = simulate_transmission(name, 4, sigma, gold_sequence, crc_bits)
            ber_n4_sum += calculate_ber(encoded_data, received_data)

        ber_values_n1.append(ber_n1_sum / num_iterations)
        ber_values_n2.append(ber_n2_sum / num_iterations)
        ber_values_n4.append(ber_n4_sum / num_iterations)

    plot_ber(sigma_values, ber_values_n4, 4)
    plot_ber(sigma_values, ber_values_n1, 1)
    plot_ber(sigma_values, ber_values_n2, 2)
    
    sigma_noise = 0.4

    # Для N=1
    _, _, signal_n1, received_signal_n1 = simulate_transmission(name, 1, sigma_noise, gold_sequence, crc_bits)
    plot_signal_with_noise(signal_n1, received_signal_n1, 1, sigma_noise)

    # Для N=2
    _, _, signal_n2, received_signal_n2 = simulate_transmission(name, 2, sigma_noise, gold_sequence, crc_bits)
    plot_signal_with_noise(signal_n2, received_signal_n2, 2, sigma_noise)

    # Для N=4
    _, _, signal_n4, received_signal_n4 = simulate_transmission(name, 4, sigma_noise, gold_sequence, crc_bits)
    plot_signal_with_noise(signal_n4, received_signal_n4, 4, sigma_noise)

    plt.show()