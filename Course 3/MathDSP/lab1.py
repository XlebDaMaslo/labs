import numpy as np
import matplotlib.pyplot as plt

parameters = [
    (0, 1),
    (0, np.sqrt(3)),
    (0, np.sqrt(0.2)),
    (-1, 1)
]

t = np.linspace(0, 3, 1000)

fig, axs = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle('Гистограммы распределения и плотности распределения')

def normal_pdf(x, m_x, sigma_squared):
    return (1 / np.sqrt(2 * np.pi * sigma_squared)) * np.exp(-((x - m_x) ** 2) / (2 * sigma_squared))

for i, (m_x, s1) in enumerate(parameters):
    xn = np.random.normal(m_x, s1, len(t))
    
    bin_width = 0.1
    bins = np.arange(m_x - 4*s1, m_x + 4*s1 + bin_width, bin_width)
    
    hist, bin_edges = np.histogram(xn, bins=bins, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    x_values = np.linspace(m_x - 4*s1, m_x + 4*s1, 1000)
    y_values = normal_pdf(x_values, m_x, s1**2)
    
    row = i // 2
    col = i % 2
    axs[row, col].bar(bin_centers, hist, width=bin_width, alpha=0.6, label='Гистограмма', color='blue')
    axs[row, col].plot(x_values, y_values, label='Плотность', color='red')
    axs[row, col].set_title(f'm_x={m_x}, σ={s1:.2f}')
    axs[row, col].set_xlabel('Значения')
    axs[row, col].set_ylabel('Плотность')
    axs[row, col].legend()
    axs[row, col].grid(True)

for m_x, s1 in parameters:
    xn = np.random.normal(m_x, s1, len(t))
    
    bin_width = 0.1
    bins = np.arange(m_x - 4*s1, m_x + 4*s1 + bin_width, bin_width)
    hist, bin_edges = np.histogram(xn, bins=bins, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    m_x_estimated = np.sum(bin_centers * hist) * bin_width
    sigma_squared_estimated = np.sum(bin_centers**2 * hist) * bin_width - m_x_estimated**2
    
    print(f"Параметры моделирования: m_x={m_x}, σ²={s1**2}")
    print(f"Оцененные параметры через эмпирическую плотность: m_x={m_x_estimated:.4f}, σ²={sigma_squared_estimated:.4f}")
    print()

plt.tight_layout()
plt.show()