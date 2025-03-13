import numpy as np
import matplotlib.pyplot as plt

## 1
m = 0
s1 = 1

t = np.linspace(0, 3, 1000)
xn = np.random.uniform(m, s1, len(t))

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.hist(xn, bins=30, density=True, color='blue', alpha=0.7)
plt.title('Гистограмма распределения xn')
plt.xlabel('Значения')
plt.ylabel('Плотность')
plt.grid(True)

n = 1000
num_samples = 1000
yn = np.sum(np.random.uniform(0, 1, (num_samples, n)), axis=1)

plt.subplot(1, 2, 2)
plt.hist(yn, bins=30, density=True, color='green', alpha=0.7)
plt.title('Гистограмма распределения Yn')
plt.xlabel('Значения')
plt.ylabel('Плотность')
plt.grid(True)

plt.tight_layout()
#plt.show()

## 2
num_realizations = 1000
realization_length = 200

normal_sp_realizations = []
for _ in range(num_realizations):
    xn_normal = np.random.normal(m, s1, realization_length)
    normal_sp_realizations.append(xn_normal)

correlated_sp_realizations = []
for xn in normal_sp_realizations:
    xn1 = np.convolve(xn, [1, 0.7, 0.3, 0.1, 0.05], mode='full')[:realization_length]
    correlated_sp_realizations.append(xn1)

plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
time_segment = np.linspace(0, 1, realization_length)
plt.plot(time_segment, correlated_sp_realizations[0])
plt.title('Временная диаграмма реализации коррелированного СП')
plt.xlabel('Время')
plt.ylabel('Значение')
plt.grid(True)

time_index_t0 = 50
section_values_t0 = [realization[time_index_t0] for realization in correlated_sp_realizations]

plt.subplot(3, 1, 2)
plt.hist(section_values_t0, bins=30, density=True, color='purple', alpha=0.7)
plt.title(f'Гистограмма распределения сечения СП в момент времени t0={time_index_t0}')
plt.xlabel('Значения')
plt.ylabel('Плотность')
plt.grid(True)

acf_values = []
taus = [0, 1, 2, 3, 5, 7, 10, 15, 20, 30, 40, 50]
t1_index = 50

for tau in taus:
    products = []
    for realization in correlated_sp_realizations:
        if t1_index + tau < realization_length:
            products.append(realization[t1_index] * realization[t1_index + tau])
    if products:
        acf_values.append(np.mean(products))
    else:
        acf_values.append(0)

plt.subplot(3, 1, 3)
representative_realization = correlated_sp_realizations[0]
max_lags = 50
plt.acorr(representative_realization - np.mean(representative_realization), maxlags=max_lags)
#plt.plot(taus, acf_values, marker='o', linestyle='-')
plt.title('Автокорреляционная функция (АКФ)')
plt.xlabel('Lag')
plt.ylabel('Значение АКФ')
plt.grid(True)

plt.tight_layout()
#plt.show()

acf_0 = acf_values[0]
correlation_interval_tau0 = 0

integral_approx = 0
for i in range(1, len(taus)):
    tau_diff = taus[i] - taus[i-1]
    integral_approx += (acf_values[i-1] + acf_values[i]) / 2 * tau_diff

if acf_0 != 0:
    correlation_interval_tau0 = integral_approx / acf_0

print(f"Оценка интервала корреляции tau0: {correlation_interval_tau0}")

## 3
single_realization = correlated_sp_realizations[0]
N = len(single_realization)

max_lag = 50
lags = np.arange(0, max_lag + 1)
acf_single = []

for n in lags:
    sum_products = 0.0
    for k in range(n, N):
        sum_products += single_realization[k] * single_realization[k - n]
    if N - n > 0:
        acf_value = sum_products / (N - n)
    else:
        acf_value = 0  # Избегание деления на ноль
    acf_single.append(acf_value)

acf_single_normalized = acf_single / acf_single[0]

plt.figure(figsize=(10, 5))
plt.stem(lags, acf_single_normalized)
plt.title('Автокорреляционная функция (АКФ) по одной реализации')
plt.xlabel('Лаг (n)')
plt.ylabel('Значение АКФ')
plt.grid(True)
plt.show()