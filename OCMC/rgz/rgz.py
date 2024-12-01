import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lab5.lab5 import calculate_crc
from lab4.lab4 import gen_gold_seq

import matplotlib.pyplot as plt
import numpy as np
from crc import Calculator, Crc8

def ascii_encoder(text):
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
    return text


def visualize(bits, title="Binary Sequence Visualization"):
    plt.figure(figsize=(10, 4))
    plt.step(range(len(bits)), bits, where='post')
    plt.xlabel("Bit Index")
    plt.ylabel("Bit Value")
    plt.title(title)
    plt.grid(True)

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
    gold_expanded = expand_bits(gold_sequence,N) # Расширение gold_sequence
    shift = 0
    max_corr = 0
    for i in range(len(received_signal) - len(gold_expanded) + 1):
        current_corr = normalized_correlation(received_signal[i : i + len(gold_expanded)], gold_expanded)
        if current_corr > max_corr:
            shift = i
            max_corr = current_corr

    return shift

def decode_signal(signal, N, threshold=0.5):
    decoded_bits = []
    for i in range(0, len(signal), N):
        list = signal[i:i + N]
        if np.mean(list) >= threshold:  # Если среднее значение >= порога, то 1
            decoded_bits.append(1)
        else:
            decoded_bits.append(0)
    return decoded_bits

def plot_spectrum(signal, fs, title):
    frequencies = np.fft.fftfreq(len(signal), 1/fs)
    spectrum = np.abs(np.fft.fft(signal))

    plt.plot(frequencies, spectrum)
    plt.title(title)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Values")

## 1
name = input("Enter your first and last name in Latin characters: ")

## 2
encoded_data = ascii_encoder(name)
print("Encoded Data (ASCII):", encoded_data)
visualize(encoded_data, "Encoded Data (ASCII)")

## 3
polynomial = '11011110'  # G=x7+x6+x4+x3+x2+x
encoded_data_str = ''.join(map(str, encoded_data))
crc = calculate_crc(encoded_data_str, polynomial)
print("CRC на передатчике:", crc)
crc_bits = [int(bit) for bit in crc]

## 4
number_st = 10  # Номер по списку
number_st2 = number_st + 7
polynomial1_bin = "00011"
polynomial2_bin = "01001"

gold_sequence = gen_gold_seq(number_st, number_st2, polynomial1_bin, polynomial2_bin)

transmitted_sequence = gold_sequence + encoded_data + crc_bits

print("Gold Sequence:", gold_sequence)
print("Transmitted Sequence:", transmitted_sequence)
visualize(transmitted_sequence, "Transmitted Sequence (Gold + Data + CRC)")

## 5
N = 5
expanded_signal = expand_bits(transmitted_sequence, N)

print("Expanded Signal:", expanded_signal)
visualize(expanded_signal, f"Expanded Signal (N={N} samples/bit)")

## 6
signal_length = 2 * N * len(transmitted_sequence)
signal = np.zeros(signal_length)

shift = int(input(f"Введите сдвиг (от 0 до {N * len(transmitted_sequence)}): "))
signal[shift:shift + len(expanded_signal)] = expanded_signal

print("Signal:", signal)
visualize(signal, f"Signal with Shift = {shift}")

## 7
fs = 200

sigma = float(input("Введите значение стандартного отклонения шума (sigma): "))
noise = np.random.normal(0, sigma, len(signal))

received_signal = signal + noise

print("Received Signal (with noise):", received_signal)
visualize(received_signal, f"Received Signal (with noise: sigma = {sigma})")

## 8
start_index = correlate(received_signal, gold_sequence, N)
print("Start index of Gold sequence:", start_index)

signal_after_sync = received_signal[start_index:]

visualize(signal_after_sync, "Signal after Synchronization (everything before Gold removed)")

## 9
decoded_bits = decode_signal(signal_after_sync, N)
decoded_bits = decoded_bits[:len(gold_sequence) + len(encoded_data) + len(crc_bits)]

## 10
decoded_bits_without_gold = decoded_bits[len(gold_sequence):] 
print("Decoded bits (without gold): ", decoded_bits_without_gold)

## 11
received_data_bits = decoded_bits_without_gold[:-len(crc_bits)]
received_crc_bits = decoded_bits_without_gold[-len(crc_bits):]

received_data_str = ''.join(map(str, received_data_bits))
calculated_crc = calculate_crc(received_data_str, polynomial)
print("Received CRC:", received_crc_bits)
print("Calculated CRC:", calculated_crc)

## 12
if calculated_crc == ''.join(map(str, received_crc_bits)):
    print("CRC check: OK")

    received_data_bits = decoded_bits_without_gold[:-len(crc_bits)]
    decoded_text = ascii_decoder(received_data_bits)
    print("Decoded Text:", decoded_text)
else:
    print("CRC check: Error. Cannot decode data.")

    received_data_bits = decoded_bits_without_gold[:-len(crc_bits)]
    decoded_text = ascii_decoder(received_data_bits)
    print("Decoded Text:", decoded_text)

## 13
N_short = N // 2
N_long = N * 2

expanded_signal_short = expand_bits(transmitted_sequence, N_short)
expanded_signal_long = expand_bits(transmitted_sequence, N_long)

signal_short = np.zeros(2 * N_short * len(transmitted_sequence))
signal_short[shift:shift + len(expanded_signal_short)] = expanded_signal_short
received_signal_short = signal_short + np.random.normal(0, sigma, len(signal_short))

signal_long = np.zeros(2 * N_long * len(transmitted_sequence))
signal_long[shift:shift + len(expanded_signal_long)] = expanded_signal_long
received_signal_long = signal_long + np.random.normal(0, sigma, len(signal_long))

plot_spectrum(received_signal_long, fs, f"Received Signal Spectrum (N={N_long})")
plot_spectrum(received_signal, fs, "Received Signal Spectrum (Noisy)")
plot_spectrum(received_signal_short, fs, f"Received Signal Spectrum (N={N_short})")
#plot_spectrum(signal, fs, "Transmitted Signal Spectrum")
plt.xlim([-150, 150])

plt.legend([f"Received (N={N_long})", "Received (N)", f"Received (N={N_short})"])
plt.grid(True)

plt.show()

# добавить стоп слово, профилирование( использовать штатную библиотеку и свою) проверив разницу 