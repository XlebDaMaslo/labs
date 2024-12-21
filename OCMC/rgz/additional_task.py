import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lab4.lab4 import gen_gold_seq

import matplotlib.pyplot as plt
import numpy as np
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
        if len(byte) == 8:
            char_code = int("".join(map(str, byte)), 2)
            text += chr(char_code)
    stop_index = text.find(STOP_WORD)
    if stop_index != -1:
        text = text[:stop_index]
    return text


def phase_shift_keying(bits, N, M): # M - количество фаз
    phase_signal = []
    for i in range(0, len(bits), N):
        bit_group = bits[i:i+N]
        if len(bit_group) == N:
            val = int("".join(map(str, bit_group)), 2)
            phase = 2*np.pi * val / M
            phase_signal.extend([phase] * N)
        elif len(bit_group) < N:
            phase = 0
            phase_signal.extend([phase] * len(bit_group))
    return phase_signal

def correlation(a, b):
    result = 0
    for i in range(min(len(a), len(b))):
        result += a[i] * b[i]
    return result

def normalized_correlation(a, b):
    sum_a = sum(x*x for x in a)
    sum_b = sum(x*x for x in b)

    if sum_a == 0 or sum_b == 0:
        return 0

    return correlation(a, b) / ((sum_a * sum_b) ** (1/2))


def correlate(received_signal, gold_sequence, N, M):
    gold_expanded = phase_shift_keying(gold_sequence, N, M)
    shift = 0
    max_corr = -1
    for i in range(len(received_signal) - len(gold_expanded) + 1):
        current_corr = normalized_correlation(received_signal[i : i + len(gold_expanded)], gold_expanded)

        if current_corr > max_corr:
            max_corr = current_corr
            shift = i

    return shift


def decode_signal(signal, N, M, threshold=0.0):
    decoded_bits = []
    for i in range(0, len(signal), N):
        if i + N <= len(signal):
            phase_values = signal[i:i + N]
            avg_phase = np.mean(phase_values)
            
            if M == 2:
               decoded_bits.append(0 if abs(avg_phase - 0) < abs(avg_phase - np.pi) else 1)
            else:
                val = int(round(avg_phase / (2*np.pi) * M)) % M
                binary = bin(val)[2:].zfill(N)
                decoded_bits.extend(map(int, binary))
    return decoded_bits


def calculate_ber(transmitted_bits, received_bits):
    min_len = min(len(transmitted_bits), len(received_bits))
    errors = sum(t != r for t, r in zip(transmitted_bits[:min_len], received_bits[:min_len]))
    return errors / min_len if min_len > 0 else 0

if __name__ == "__main__":
    ## 1
    name = "Testtext!!!1234567890"

    ## 2
    encoded_data = ascii_encoder(name)

    ## 3
    encoded_data_bytes = bytes(int(''.join(map(str, encoded_data[i:i + 8])), 2) for i in range(0, len(encoded_data), 8))

    crc32c_checksum = crc32c.crc32c(encoded_data_bytes)
    crc_bits = list(map(int, bin(crc32c_checksum)[2:].zfill(8)))

    ## 4
    number_st = 10  # Номер по списку
    number_st2 = number_st + 7
    polynomial1_bin = "00011"
    polynomial2_bin = "01001"

    gold_sequence = gen_gold_seq(number_st, number_st2, polynomial1_bin, polynomial2_bin)

    transmitted_sequence = gold_sequence + encoded_data + crc_bits

    Ns = [1, 2, 4]
    snr_range = np.arange(-10, 100, 1)

    ber_results = {N: [] for N in Ns}

    for N in Ns:
       
        M = 2**N
        for snr_db in snr_range:
            snr_linear = 10 ** (snr_db / 10)

            phase_signal = phase_shift_keying(transmitted_sequence, N, M)
            signal_length = len(phase_signal)

            shift = 0
            signal = np.zeros(signal_length)
            signal[shift:shift + len(phase_signal)] = phase_signal
            signal_power = np.mean(signal**2)
            noise_power = signal_power / snr_linear
            sigma = np.sqrt(noise_power)


            noise = np.random.normal(0, sigma, len(signal))
            received_signal = signal + noise
            
            start_index = correlate(received_signal, gold_sequence, N, M)

            signal_after_sync = received_signal[start_index:]

            decoded_bits = decode_signal(signal_after_sync, N, M)
            decoded_bits = decoded_bits[:len(transmitted_sequence)]

            
            ber = calculate_ber(transmitted_sequence, decoded_bits)
            ber_results[N].append(ber)

    plt.figure(figsize=(10, 6))
    for N in Ns:
        plt.plot(snr_range, ber_results[N], label=f'Group Siza: {N}')
    
    plt.xlabel('Signal-to-Noise Ratio')
    plt.ylabel('Bit Error Rate')
    plt.yscale('log')
    plt.grid(True)
    plt.legend()
    plt.show()