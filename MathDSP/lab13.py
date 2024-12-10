# две гармоники, фильтр, (Ханн, Хеминг, Барлей)
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.signal import freqz, lfilter

f1 = 2400
fs = 9600
wc = 2 * np.pi * f1 / fs

M_values = [7]
window_types = ['rectangular', 'hamming', 'bartlett', 'blackman', 'hanning', 'kaiser']

t = np.arange(0, 0.01, 1/fs)
signal_in = np.sin(2*np.pi*1000*t) + np.sin(2*np.pi*10000*t)

for M in M_values:
    n = np.arange(-M, M + 1)
    h_ideal = np.sin(wc * n) / (np.pi * n)
    h_ideal[M] = wc / np.pi

    # График для импульсных характеристик
    plt.figure(figsize=(15, 5))

    for i, window_type in enumerate(window_types):
        if window_type == 'rectangular':
            window = np.ones(2 * M + 1)
        elif window_type == 'kaiser':
            window = np.kaiser(2 * M + 1, beta=4)
        else:
            window = getattr(np, window_type)(2 * M + 1) # аналогично np.hanning(2 * M + 1) или другое окно

        h = h_ideal * window

        plt.subplot(2, 3, i + 1)
        plt.stem(n, h)
        plt.title(f'Импульсная х-ка ({window_type})')


    plt.tight_layout()
    plt.show()



    # График для АЧХ
    plt.figure(figsize=(15, 10))

    for i, window_type in enumerate(window_types):
        if window_type == 'rectangular':
            window = np.ones(2 * M + 1)
        elif window_type == 'kaiser':
            window = np.kaiser(2 * M + 1, beta=4)
        else:
            window = getattr(np, window_type)(2 * M + 1)

        h = h_ideal * window
        w, hf = freqz(h, worN=8000)
        f = w * fs / (2 * np.pi)

        plt.subplot(3, 2, i+1)
        plt.plot(f, 20 * np.log10(np.abs(hf)))
        plt.title(f'АЧХ (M = {M}, {window_type})')
        plt.xlim(0, fs/2)
        plt.ylim(-80, 10)

        print(f"Коэффициенты ИХ для M = {M}, {window_type}: {h}")

    plt.tight_layout()
    plt.show()


    # График сравнения АЧХ
    plt.figure(figsize=(12, 6))
    for window_type in window_types:
        if window_type == 'rectangular':
            window = np.ones(2 * M + 1)
        elif window_type == 'kaiser':
            window = np.kaiser(2 * M + 1, beta=4)
        else:
            window = getattr(np, window_type)(2 * M + 1)
        h = h_ideal * window
        w, hf = freqz(h, worN=8000)
        f = w * fs / (2 * np.pi)
        plt.plot(f, 20 * np.log10(np.abs(hf)), label=window_type)

    plt.title(f'Сравнение АЧХ (M = {M})')
    plt.xlim(0, fs/2)
    plt.ylim(-80, 10)
    plt.legend()
    plt.tight_layout()
    plt.show()