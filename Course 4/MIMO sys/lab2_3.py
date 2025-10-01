import numpy as np
import matplotlib.pyplot as plt

f1 = 1800  # МГц
hbs1 = 20  # Высота базовой станции 1 в метрах
hbs2 = 50  # Высота базовой станции 2 в метрах
hma = 2    # Высота мобильной станции в метрах

r = np.arange(1, 21, 1)

a1 = (1.11 * np.log10(f1) - 0.7) * hma - (1.56 * np.log10(f1) - 0.8)

# Модель Окумура-Хата для Hbs = 20 м
Lokh1 = 69.55 + 26.16 * np.log10(f1) - 13.83 * np.log10(hbs1) - a1 + (44.9 - 6.55 * np.log10(hbs1)) * np.log10(r)

# Модель Окумура-Хата для Hbs = 50 м
Lokh2 = 69.55 + 26.16 * np.log10(f1) - 13.83 * np.log10(hbs2) - a1 + (44.9 - 6.55 * np.log10(hbs2)) * np.log10(r)

plt.figure(figsize=(10, 6))
plt.plot(r, Lokh1, 'b-o', label='Hbs = 20 м')
plt.plot(r, Lokh2, 'm-x', label='Hbs = 50 м')

plt.title("Влияние высоты базовой станции на потери (f=1800 МГц)")
plt.xlabel('Расстояние, км')
plt.ylabel('Потери распространения, дБ')
plt.legend()
plt.grid(True)
plt.show()