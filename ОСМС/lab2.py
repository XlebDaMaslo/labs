import numpy as np
import matplotlib.pyplot as plt

# Исходные данные
TxPowerBS = 46 # дБм Мощность передатчиков BS
NumSectors = 3 # Число секторов на одной BS
TxPowerUE = 24 # дБм Мощность передатчика пользовательского терминала UE
AntGainBS = 21 # дБи Коэффициент усиления антенны BS
PenetrationM = 15 # дБ Запас мощности сигнала на проникновения сквозь стены
IM = 1 # дБ Запас мощности сигнала на интерференцию
# Модель распространения сигнала для макросот: COST 231 Hata;
# Модель распространения сигнала для фемто- и микросот: UMiNLOS;
f = 1800 # МГц Диапазон частот
BW_UL = 10 # МГц Полоса частот в UL
BW_DL = 20 # МГц Полоса частот в DL
# Дуплекс UL и DL: FDD;
NoiseFigureBS = 2.4 # дБ Коэффициент шума приемника BS
NoiseFigureUE = 6 # дБ Коэффициент шума приемника пользователя
RequiredSINR_DL = 2 # дБ Требуемое отношение SINR для DL
RequiredSINR_UL = 4 # дБ Требуемое отношение SINR для UL
MIMOGain = 3 # дБ Выигрыш за счет использования MIMO (Число приемо-передающих антенн на BS (MIMO): 2)
AreaTerritory = 100 # кв.км Площадь территории, на которой требуется спроектировать сеть
AreaShoppingBusiness = 4 # кв.км Площадь торговых и бизнес центров, где требуется спроектировать сеть на базе микро- и фемтосот
FeederLoss = 2 # дБ Уровень потерь сигнала при прохождении через фидер или джампер (Базовые станции с фидерами)

#1 Расчет уровня максимально допустимых потерь в восходящем канале
ThermalNoise = -174 + 10*np.log10(BW_UL)
RxSensBS = NoiseFigureBS + ThermalNoise + RequiredSINR_UL

MAPL_UL = TxPowerUE - FeederLoss + AntGainBS + MIMOGain - IM - PenetrationM - RxSensBS

print(f"MAPL_UL: {MAPL_UL:.4f} дБ")

#2 Расчет уровня максимально допустимых потерь в нисходящем канале
ThermalNoise = -174 + 10*np.log10(BW_DL)
RxSensUE = NoiseFigureUE + ThermalNoise + RequiredSINR_DL

MAPL_DL = TxPowerBS - FeederLoss + AntGainBS + MIMOGain - IM - PenetrationM - RxSensUE
print(f"MAPL_DL: {MAPL_DL:.4f} дБ")

#3 Построение моделей распространения сигнала
d = np.linspace(10, 1000, 1000)
A = 69.55 if (f >= 150 and f <= 1500) else 46.3 if (f >= 1500 and f <= 2000) else 0
B = 26.16 if (f >= 150 and f <= 1500) else 33.9 if (f >= 1500 and f <= 2000) else 0
hBS = 50
hms = 1
w = 15
b = 25
delta_h = 5
phi = 45

# UMiNLOS(Urban Micro Non-Line-of-Sight)
PL_UMiNLOS = 26 * np.log10(f) + 22.7 + 36.7 * np.log10(d)

# COST231(Окумура-Хата) DU
a_hms = 3.2 * (np.log10(11.75 * hms))**2 - 4.97
Lclutter = 3
s = 44.9 - 6.55 * np.log10(f)
PL_COST231 = A + B * np.log10(f) - 13.82 * np.log10(hBS) - a_hms + s * np.log10(d) + Lclutter

# Walfish-Ikegami
PL_Walfish_LOS = 42.6 + 20 * np.log10(f) + 26 * np.log10(d)

phi = (-10 + 0.354*phi) if (phi >= 0 and phi < 35) else (2.5 + 0.075*phi) if (phi >= 35 and phi < 55) else (4.0 - 0.114*phi) if (phi >= 55 and phi < 90) else 0
L0 = 32.44 + 20 * np.log10(f) + 20 * np.log10(d)

L2 = -16.9 - 10 * np.log10(w) + 10 * np.log10(f) + 20 * np.log10(delta_h - hms) + phi

L11 = (-18*np.log10(1+hBS-delta_h)) if (hBS > delta_h) else 0 
Ka = (54-0.8*(hBS-delta_h)) if (hBS <= delta_h and d > 0.5) else (54-0.8*(hBS-delta_h)*(d/0.5)) if (hBS <= delta_h and d <= 0.5) else 0
Kd = 18 if (hBS > delta_h) else (18-15*((hBS-delta_h)/delta_h)) if (hBS <= delta_h) else 0
Kf = -4 + 0.7 * (f/925 - 1)
L1 = L11 + Ka + Kd * np.log10(d) + Kf * np.log10(f) - 9 * np.log10(b)
PL_Walfish_NLOS = np.where((L1 + L2) <= 0, L0, L0 + L1 + L2)

plt.figure(figsize=(10, 5))
plt.plot(d, PL_UMiNLOS, label="UMiNLOS")
plt.plot(d, PL_COST231, label="COST231(DU)")
plt.plot(d, PL_Walfish_LOS, label="Walfish-Ikegami (LOS)")
plt.plot(d, PL_Walfish_NLOS, label="Walfish-Ikegami (NLOS)")
plt.axhline(MAPL_UL, color='blue', label=f'MAPL_UL = {MAPL_UL:.2f} дБ')
plt.axhline(MAPL_DL, color='green', linestyle='--', label=f'MAPL_DL = {MAPL_DL:.2f} дБ')
plt.xlabel("Расстояние (м)")
plt.ylabel("Потери сигнала (дБ)")
plt.title("Зависимость величины входных потерь радиосигнала от расстояния между приемником и передатчиком")
plt.legend()
plt.grid(True)
plt.ylim(0, 250)
plt.show()

#4 Определение радиусов, площадей и количество базовых станций для макросот и микросот
d_UL_Macro = d[np.where(PL_COST231 <= MAPL_UL)[0][-1]] if np.any(PL_COST231 <= MAPL_UL) else 0
d_DL_Macro = d[np.where(PL_COST231 <= MAPL_DL)[0][-1]] if np.any(PL_COST231 <= MAPL_DL) else 0

print(f"Радиус базовой станции для макросот UL: {d_UL_Macro:.4f} м")
print(f"Радиус базовой станции для макросот DL: {d_DL_Macro:.4f} м")

R_Macro = min(d_UL_Macro, d_DL_Macro)
print(f"Минимальный радиус макросоты: {R_Macro:.4f} м")

d_UL_Femto = d[np.where(PL_UMiNLOS <= MAPL_UL)[0][-1]] if np.any(PL_UMiNLOS <= MAPL_UL) else 0
d_DL_Femto = d[np.where(PL_UMiNLOS <= MAPL_DL)[0][-1]] if np.any(PL_UMiNLOS <= MAPL_DL) else 0

print(f"Радиус базовой станции для фемто- и микросот UL: {d_UL_Femto:.4f} м")
print(f"Радиус базовой станции для фемто- и микросот DL: {d_DL_Femto:.4f} м")

R_Femto = min(d_UL_Femto, d_DL_Femto)
print(f"Минимальный радиус фемто- и микросоты: {R_Femto:.4f} м")

S_Macro = 1.95 * R_Macro**2
print(f"Площадь макросоты: {S_Macro:.4f} кв.м")
NumBS_Macro = np.ceil((AreaTerritory*1000000) / S_Macro)
print(f"Необходимое количество базовых станций (сайтов): {NumBS_Macro}")

S_Femto = 1.95 * R_Femto**2
print(f"Площадь фемто- и микросоты: {S_Femto:.4f} кв.м")
NumBS_Femto = np.ceil((AreaShoppingBusiness*1000000) / S_Femto)
print(f"Необходимое количество базовых станций (сайтов): {NumBS_Femto}")