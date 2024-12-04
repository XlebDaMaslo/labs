import numpy as np
import matplotlib.pyplot as plt

def S1(omega1):
    return A * 1 / (np.sqrt(1 + (omega1 * 2 * np.pi * tau ) ** 2)) * np.cos(omega1 * t + (- np.arctan(omega1 * 2 * np.pi * tau)))

def S(omega1):
    return  A * np.cos(omega1 * t)

tau = 0.1
omega = np.linspace(0, 2/tau, 1000)
t = np.linspace(0, 10, 1000)
A = 5

ACHH = 1 / (np.sqrt(1 + (omega * 2 * np.pi * tau ) ** 2))

FCHH = - np.arctan(omega * 2 * np.pi * tau)

plt.figure(figsize=(15, 9))

plt.subplot(5, 1, 1)
plt.plot(omega, ACHH, label='АЧХ')
plt.ylabel('U(вых) / U(вход)')
plt.xlabel('Омега')
plt.title('АЧХ')
plt.grid(True)

plt.subplot(5, 1, 2)
plt.plot(omega, FCHH, label='ФЧХ', color = "r")
plt.ylabel('Гц')
plt.xlabel('Омега')
plt.title('ФЧХ')
plt.grid(True)

plt.subplot(5, 1, 3)
plt.plot(t, S(10), color = "orange")
plt.grid(True)

plt.subplot(5, 1, 3)
plt.plot(t, S1(10), color = "green")
plt.plot(t, S(10), color = "orange")
plt.title('Сигналы с частотой 10')
plt.grid(True)

plt.subplot(5, 1, 4)
plt.plot(t, S1(20), color = "green")
plt.plot(t, S(20), color = "orange")
plt.title('Сигналы с частотой 20')
plt.grid(True)

plt.subplot(5, 1, 5)
plt.plot(t, S1(50), color = "green")
plt.plot(t, S(50), color = "orange")
plt.title('Сигналы с частотой 50')
plt.grid(True)

plt.tight_layout()
plt.show()