import numpy as np
import matplotlib.pyplot as plt

f1 = 900  # МГц
hbc = 30  # Высота базовой станции в метрах
hma = 2   # Высота мобильной станции в метрах
C = 3     # Коэффициент для городской среды (в модели COST-Hata)

# от 1 до 20 км с шагом 1 км
r = np.arange(1, 21, 1)

# Поправочный коэффициент a(h_m)
a1 = (1.11 * np.log10(f1) - 0.7) * hma - (1.56 * np.log10(f1) - 0.8)

# Модель COST-Hata
Lcoh = 46.3 + 33.9 * np.log10(f1) - 13.82 * np.log10(hbc) - a1 + (44.9 - 6.55 * np.log10(hbc)) * np.log10(r) + C

# Модель Окумура-Хата
Lokh = 69.55 + 26.16 * np.log10(f1) - 13.83 * np.log10(hbc) - a1 + (44.9 - 6.55 * np.log10(hbc)) * np.log10(r)

plt.figure(figsize=(10, 6))
plt.plot(r, Lcoh, 'r-o', label='Cost-Hata')
plt.plot(r, Lokh, 'g-x', label='Okumura-Hata')

plt.title("Потери распространения (f=900 МГц, Hbs=30 м)")
plt.xlabel('Расстояние, км')
plt.ylabel('Потери распространения, дБ')
plt.legend()
plt.grid(True)
plt.show()