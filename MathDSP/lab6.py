import numpy as np
import matplotlib.pyplot as plt

def rect_signal(width, height, t):
    signal = np.zeros(t)
    start = (t - width) // 2
    signal[start:start + width] = height
    return signal

def manual_convolution(signal1, signal2):
    len1 = len(signal1)
    len2 = len(signal2)
    
    output_len = len1 + len2 - 1
    result = np.zeros(output_len)

    for i in range(output_len):
        sum = 0
        for j in range(len2):
            if i - j >= 0 and i - j < len1:
                sum += signal1[i - j] * signal2[j]
        result[i] = sum
    return result

width1 = 75
height1 = 1
width2 = 10
height2 = 1

t = 200

signal1 = rect_signal(width1, height1, t)
signal2 = rect_signal(width2, height2, t)

#convolution = np.convolve(signal1, signal2, mode='full')
convolution = manual_convolution(signal1, signal2)

plt.figure(figsize=(10, 6))

plt.subplot(3, 1, 1)
plt.plot(signal1)
plt.title('Прямоугольный сигнал 1')
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(signal2)
plt.title('Прямоугольный сигнал 2')
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(convolution)
plt.title('Свёртка сигналов')
plt.grid(True)

plt.tight_layout()
plt.show()
