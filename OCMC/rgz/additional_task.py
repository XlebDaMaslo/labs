import sys
import os
import math
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

def visualize(bits, title="Binary Sequence Visualization"):
    plt.figure(figsize=(10, 4))
    plt.step(range(len(bits)), bits, where='post')
    plt.xlabel("Index")
    plt.ylabel("Bit")
    plt.title(title)
    plt.grid(True)

def grouped_encoder(bits, group_size):
    encoded_signal = []
    for i in range(0, len(bits), group_size):
        group = bits[i:i + group_size]
        if len(group) < group_size:
            group.extend([0] * (group_size - len(group)))

        value = int("".join(map(str, group)), 2) / (2 ** group_size - 1)
        encoded_signal.append(value)
    return encoded_signal

def grouped_decoder(signal, group_size):
    decoded_bits = []
    for value in signal:
        group_value = int(round(value * (2**group_size-1)))
        group_bits = bin(group_value)[2:].zfill(group_size)
        decoded_bits.extend(list(map(int,group_bits)))
    return decoded_bits

def expand_bits(bits, N):
    expanded_signal = []
    for bit in bits:
        expanded_signal.extend([bit] * N)
    return expanded_signal

def correlation(a, b):
    result = 0
    for i in range(len(a)):
        result += a[i] * b[i]
    return result

def normalized_correlation(a, b):
    sum_a = 0
    sum_b = 0
    for i in range(len(a)):
        sum_a += a[i] * a[i]
        sum_b += b[i] * b[i]
    return correlation(a, b) / ((sum_a * sum_b) ** (1/2))

def correlate(received_signal, gold_sequence, N):
    gold_expanded = expand_bits(gold_sequence,N)
    shift = 0
    max_corr = 0
    for i in range(len(received_signal) - len(gold_expanded) + 1):
        current_corr = normalized_correlation(received_signal[i : i + len(gold_expanded)], gold_expanded)
        if current_corr > max_corr:
            shift = i
            max_corr = current_corr
    return shift

def decode_signal(signal, N):
    threshold = np.mean(signal)
    decoded_bits = []
    for i in range(0, len(signal), N):
        list = signal[i:i + N]
        if np.mean(list) >= threshold:
            decoded_bits.append(1)
        else:
            decoded_bits.append(0)

    return decoded_bits

def plot_spectrum(signal, fs, title):
    signal_without_dc = signal - np.mean(signal)
    frequencies = np.fft.fftfreq(len(signal_without_dc), 1/fs)
    spectrum = np.abs(np.fft.fft(signal_without_dc))

    plt.plot(frequencies, spectrum)
    plt.title(title)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")


if __name__ == "__main__":
    ## 1
    name = input("Enter your first and last name in Latin characters: ")
    ## 2
    encoded_data = ascii_encoder(name)
    print("Encoded Data (ASCII):", encoded_data)
    #visualize(encoded_data, "Encoded Data (ASCII)")
    ## 3
    encoded_data_bytes = bytes(int(''.join(map(str, encoded_data[i:i + 8])), 2) for i in range(0, len(encoded_data), 8))
    crc32c_checksum = crc32c.crc32c(encoded_data_bytes)
    crc_bits = list(map(int, bin(crc32c_checksum)[2:].zfill(8)))
    print("CRC32 на передатчике:", crc32c_checksum)
    ## 4
    number_st = 10  # Номер по списку
    number_st2 = number_st + 7
    polynomial1_bin = "00011"
    polynomial2_bin = "01001"
    gold_sequence = gen_gold_seq(number_st, number_st2, polynomial1_bin, polynomial2_bin)
    transmitted_sequence = gold_sequence + encoded_data + crc_bits
    print("Gold Sequence:", gold_sequence)
    print("Transmitted Sequence:", transmitted_sequence)
    #visualize(transmitted_sequence, "Transmitted Sequence (Gold + Data + CRC)")

    N = 5
    signal_length = 2 * N * len(transmitted_sequence)
    shift = int(input(f"Enter the offset (от 0 до {N * len(transmitted_sequence)}): "))
    fs = 200
    sigma = 0.4
    group_sizes = [1, 2, 4]
    num_trials = 10
    
    sigma_values = np.linspace(0.01, 1, 20)
    crc_error_probabilities = {group_size: [] for group_size in group_sizes}

    for group_size in group_sizes:
        for current_sigma in sigma_values:
            error_count = 0
            for _ in range(num_trials): # Повторяем симуляции для каждого значения sigma
                # Group encoding
                grouped_signal = grouped_encoder(transmitted_sequence, group_size)
                #print(f"Grouped encoded signal (size={group_size}):", grouped_signal)

                expanded_grouped_signal = []
                for val in grouped_signal:
                    expanded_grouped_signal.extend([val] * N)
                
                signal = np.zeros(signal_length)
                signal[shift:shift + len(expanded_grouped_signal)] = expanded_grouped_signal
                noise = np.random.normal(0, current_sigma, len(signal))
                received_signal = signal + noise
                
                # Decoding part:
                start_index = correlate(received_signal, gold_sequence, N)
                signal_after_sync = received_signal[start_index:]
                decoded_grouped_signal = decode_signal(signal_after_sync, N)

                decoded_bits = grouped_decoder(decoded_grouped_signal,group_size)
                decoded_bits = decoded_bits[:len(gold_sequence) + len(encoded_data) + len(crc_bits)]

                received_bits_without_gold = decoded_bits[len(gold_sequence):]
                received_data_bits = received_bits_without_gold[:-len(crc_bits)]
                received_crc_bits = received_bits_without_gold[-len(crc_bits):]
                
                received_data_bytes = bytes(int(''.join(map(str, received_data_bits[i:i + 8])), 2) for i in range(0, len(received_data_bits), 8))
                calculated_crc = crc32c.crc32c(received_data_bytes)
                calculated_crc_bits = list(map(int, bin(calculated_crc)[2:].zfill(8)))

                crc_error = calculated_crc != int(''.join(map(str, received_crc_bits)), 2)
                if crc_error:
                  error_count+=1
            crc_error_probabilities[group_size].append(error_count/num_trials)
            print(crc_error_probabilities)
        visualize(grouped_signal, f"Group size={group_size}")
    
    plt.figure(figsize=(10, 6))
    for group_size, error_probs in crc_error_probabilities.items():
        plt.plot(sigma_values, error_probs, label=f"Group Size: {group_size}")
    
    plt.xlabel("Sigma")
    plt.ylabel("CRC Error Probability")
    plt.legend()
    plt.grid(True)

    plt.show()