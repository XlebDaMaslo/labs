from scipy . fftpack import fft , ifft , fftshift
import numpy as np
import matplotlib . pyplot as plt

N = 10 # Номер по списку
fc = 10 * N # Частота синуса
fs = 32 * fc # частота дискретизации, избыточная
t = np.arange( 0, 2, 1/fs) # длительность сигнала 2 с
x = np.sin(2 * np.pi * fc * t) # формирование временного сигнала

'''
plt.figure(1)
plt.plot(t ,x)
# plt .stem(t ,x) # для отображения временных отсчетов сигнала, выбрать длительность 0.2 сек
plt.xlabel('$t=nT_s$')
plt.ylabel('$x[n]$')
plt.xlim([0, 0.2])

N = 256 # количество точек ДПФ
X = fft(x,N)/N # вычисление ДПФ и нормирование на N

plt.figure (2)
k = np.arange(0, N)
plt.stem(k,abs(X)) # выводим модуль ДПФ в точках ДПФ
plt.xlabel('k')
plt.ylabel('$x[k]$')

df = fs / N
kf = k * df
plt.figure(3)
plt.stem(kf, abs(X)) # выводим модуль ДПФ в частотах
plt.xlabel('Гц')
plt.ylabel('$x[k]$')

k2 = np.arange(-N / 2, N / 2)
kf2 = k2 * df
X2 = fftshift(X)  # сдвиг ДПФ на центр
plt.figure(4)
plt.stem(kf2, abs(X2))
plt.xlabel('Гц')
plt.ylabel('$x[k]$')

plt.figure(5)
x_ifft = N * ifft(X, N)
t = np.arange(0, len(x_ifft)) / fs
plt.plot(t, np.real(x_ifft))
# plt.stem(t, np.real(x_ifft))  # временные отсчеты колебания
plt.xlabel('c')
plt.ylabel('$x[n]$')
plt.show()
'''

## 1
multiplier = 5
fc2 = fc * multiplier
fs2 = fs * multiplier
t2 = np.arange(0, 2, 1/fs2)
x2 = np.sin(2 * np.pi * fc2 * t2)

plt.figure(1)
plt.subplot(2, 1, 1)
plt.plot(t, x)
plt.title(f'Сигнал 1: fc={fc} Гц, fs={fs} Гц')
plt.xlabel('t, c')
plt.ylabel('x[n]')
plt.xlim([0, 0.05])

plt.subplot(2, 1, 2)
plt.plot(t2, x2)
plt.title(f'Сигнал 2: fc={fc2} Гц, fs={fs2} Гц')
plt.xlabel('t, c')
plt.ylabel('x[n]')
plt.xlim([0, 0.05])

plt.tight_layout()

print("\nПервые 10 отсчетов сигнала 1:", x[:10])
print("Первые 10 отсчетов сигнала 2:", x2[:10])

print(f"Нормированная частота для сигнала 1: {fc/fs}")
print(f"Нормированная частота для сигнала 2: {fc2/fs2}")

## 2
N = 256  # Количество точек ДПФ
X = fft(x, N) / N  # Вычисление ДПФ и нормирование на N

df = fs / N
print(f"\nШаг по частоте (df): {df} Гц")

k_fc = np.round(fc / df)
print(f"Номер точки ДПФ, соответствующей fc: k = {k_fc}")

plt.figure(2)
k = np.arange(0, N)
plt.stem(k, abs(X))
plt.title("Модуль ДПФ")
plt.xlabel("k")
plt.ylabel("|X[k]|")
plt.scatter(k_fc, abs(X[int(k_fc)]), color='red', s=50, marker='o', label=f'fc = {fc} Гц')

plt.legend()

plt.figure(3)
kf = k * df
plt.stem(kf, abs(X))
plt.title("Модуль ДПФ (в частотах)")
plt.xlabel("Частота, Гц")
plt.ylabel("|X[k]|")
plt.scatter(k_fc*df, abs(X[int(k_fc)]), color='red', s=50, marker='o', label=f'fc = {fc} Гц')

plt.legend()

## 3
multiplier = 5  # Множитель для увеличения частоты
fc2 = fc * multiplier
fs2 = fs * multiplier
t2 = np.arange(0, 2, 1/fs2)
x2 = np.sin(2 * np.pi * fc2 * t2)

N = 256
X = fft(x2, N) / N

df = fs2 / N
print(f"\nШаг по частоте (df): {df} Гц")

k_fc = np.round(fc2 / df)
print(f"Номер точки ДПФ, соответствующей fc: k = {k_fc}")

plt.figure(4)
k = np.arange(0, N)
plt.stem(k, abs(X))
plt.title("Модуль ДПФ")
plt.xlabel("k")
plt.ylabel("|X[k]|")
plt.scatter(k_fc, abs(X[int(k_fc)]), color='red', s=50, marker='o', label=f'fc = {fc2} Гц')
plt.legend()

plt.figure(5)
kf = k * df
plt.stem(kf, abs(X))
plt.title("Модуль ДПФ (в частотах)")
plt.xlabel("Частота, Гц")
plt.ylabel("|X[k]|")
plt.scatter(k_fc*df, abs(X[int(k_fc)]), color='red', s=50, marker='o', label=f'fc = {fc2} Гц')
plt.legend()


## 4
N = 512
X = fft(x, N) / N
df = fs / N
print(f"\nШаг по частоте (df): {df} Гц")

k_fc = np.round(fc / df)
print(f"Номер точки ДПФ, соответствующей fc: k = {k_fc}")

plt.figure(6)
k = np.arange(0, N)
plt.stem(k, abs(X))
plt.title("Модуль ДПФ")
plt.xlabel("k")
plt.ylabel("|X[k]|")
plt.scatter(k_fc, abs(X[int(k_fc)]), color='red', s=50, marker='o', label=f'fc = {fc} Гц')
plt.legend()

plt.figure(7)
kf = k * df
plt.stem(kf, abs(X))
plt.title("Модуль ДПФ (в частотах)")
plt.xlabel("Частота, Гц")
plt.ylabel("|X[k]|")
plt.scatter(k_fc*df, abs(X[int(k_fc)]), color='red', s=50, marker='o', label=f'fc = {fc} Гц')
plt.legend()

## 5
N = 10
fc1 = 10 * N
fc2 = 50 * N

fs = 32 * max(fc1, fc2)
t = np.arange(0, 2, 1/fs)

x = np.sin(2 * np.pi * fc1 * t) + np.sin(2 * np.pi * fc2 * t)

N = 512
X = fft(x, N) / N

df = fs / N
print(f"Шаг по частоте (df): {df} Гц")

k_fc1 = np.round(fc1 / df)
k_fc2 = np.round(fc2 / df)
print(f"Номер точки ДПФ, соответствующей fc1: k = {k_fc1}")
print(f"Номер точки ДПФ, соответствующей fc2: k = {k_fc2}")

plt.figure(8)
k = np.arange(0, N)
plt.stem(k, abs(X))
plt.title("Модуль ДПФ")
plt.xlabel("k")
plt.ylabel("|X[k]|")
plt.scatter(k_fc1, abs(X[int(k_fc1)]), color='red', s=50, marker='o', label=f'fc1 = {fc1} Гц')
plt.scatter(k_fc2, abs(X[int(k_fc2)]), color='green', s=50, marker='o', label=f'fc2 = {fc2} Гц')
plt.legend()

plt.figure(9)
kf = k * df
plt.stem(kf, abs(X))
plt.title("Модуль ДПФ (в частотах)")
plt.xlabel("Частота, Гц")
plt.ylabel("|X[k]|")
plt.scatter(k_fc1*df, abs(X[int(k_fc1)]), color='red', s=50, marker='o', label=f'fc1 = {fc1} Гц')
plt.scatter(k_fc2*df, abs(X[int(k_fc2)]), color='green', s=50, marker='o', label=f'fc2 = {fc2} Гц')
plt.legend()

## 6
def plot_odpf(X, title):
    x = np.fft.ifft(X) * len(X)
    N = len(X)
    n = np.arange(N)
    
    plt.figure(figsize=(10, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(n, np.real(x))
    plt.title(f"{title} (Реальная часть)")
    plt.xlabel("n")
    plt.ylabel("Re(x[n])")


    plt.subplot(1, 2, 2)
    plt.plot(n, np.imag(x))
    plt.title(f"{title} (Мнимая часть)")
    plt.xlabel("n")
    plt.ylabel("Im(x[n])")

    plt.tight_layout()

X1 = np.array([0, 0, 1, 0, 0, 0, 0, 0])
X2 = np.array([0, 0, 0, 0, 1, 0, 0, 0])

X3 = np.array([0, 0, 1j, 0, 0, 0, 0, 0])
X4 = np.array([0, 0, -1j, 0, 0, 0, 0, 0])

X5 = np.array([0, 0, 2-1j, 0, 0, 0, 0, 0])
X6 = np.array([0, 0, 2+1j, 0, 0, 0, 0, 0])

X7 = np.zeros(16, dtype=complex)
X7[5] = 1

plot_odpf(X1, 'X1: ненулевой элемент в позиции 2')
plot_odpf(X2, 'X2: ненулевой элемент в позиции 4')
plot_odpf(X3, 'X3: 1j в позиции 2')
plot_odpf(X4, 'X4: -1j в позиции 2')
plot_odpf(X5, 'X5: 2-1j в позиции 2')
plot_odpf(X6, 'X6: 2+1j в позиции 2')
plot_odpf(X7, 'X7: 16 точек, ненулевой элемент в позиции 5')

plt.show()