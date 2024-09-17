import numpy as np
import matplotlib.pyplot as plt

# Параметры синусоид
A1 = 1  # амплитуда первой синусоиды
A2 = 0.5  # амплитуда второй синусоиды
f = 5
phi1 = 0  # начальная фаза первой синусоиды
phi2 = np.pi / 4  # начальная фаза второй синусоиды

# Время (0 до 1 с шагом 0.001)
t = np.linspace(0, 1, 1000)

# Первая и вторая синусоиды
y1 = A1 * np.sin(2 * np.pi * f * t + phi1)
y2 = A2 * np.sin(2 * np.pi * f * t + phi2)

# Сумма синусоид
y_sum = y1 + y2

# Построение графиков
plt.figure(figsize=(10, 6))

# График первой синусоиды
plt.plot(t, y1, label='Синусоида 1')

# График второй синусоиды
plt.plot(t, y2, label='Синусоида 2')

# График суммы синусоид
plt.plot(t, y_sum, label='Сумма синусоид', linestyle='--')

# Настройки графика
plt.title('Сложение двух синусоид')
plt.xlabel('Время (с)')
plt.ylabel('Амплитуда')
plt.legend()
plt.grid(True)

# Показ графика
plt.show()
