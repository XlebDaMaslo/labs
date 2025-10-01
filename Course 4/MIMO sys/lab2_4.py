import numpy as np
import matplotlib.pyplot as plt

def watt_to_dbm(watt):
    return 10 * np.log10(watt * 1000)

Pt1_watt = 10
Pt2_watt = 20

Gt = 8   # Усиление антенны передатчика, дБи
Gr = 3   # Усиление антенны приемника, дБи

f1 = 900
hbc = 30
hma = 2

r = np.arange(1, 21, 1)


Pt1_dbm = watt_to_dbm(Pt1_watt)
Pt2_dbm = watt_to_dbm(Pt2_watt)

# Рассчитываем потери по модели Окумура-Хата
a1 = (1.11 * np.log10(f1) - 0.7) * hma - (1.56 * np.log10(f1) - 0.8)
Lokh = 69.55 + 26.16 * np.log10(f1) - 13.83 * np.log10(hbc) - a1  + (44.9 - 6.55 * np.log10(hbc)) * np.log10(r)

Pr1_dbm = Pt1_dbm + Gt + Gr - Lokh
Pr2_dbm = Pt2_dbm + Gt + Gr - Lokh

plt.figure(figsize=(10, 6))
plt.plot(r, Pr1_dbm, 'c-o', label='Pt = 10 Вт (40 дБм)')
plt.plot(r, Pr2_dbm, 'y-x', label='Pt = 20 Вт (43 дБм)')

plt.title("Принимаемая мощность в зависимости от расстояния")
plt.xlabel('Расстояние, км')
plt.ylabel('Мощность на входе приемника, дБм')
plt.legend()
plt.grid(True)
plt.show()