import math
from scipy.stats import norm

### Раздел 1

def db_to_linear(db_value): # значение из дБ в линейную шкалу
    return 10**(db_value / 10)

def linear_to_db(linear_value): # значение из линейной шкалы в дБ
    return 10 * math.log10(linear_value)

def calculate_total_noise_figure(chain): # вычисление общего коэффициента шума каскадно-соединенных устройств по формуле Фрииса
    total_f = 0
    cumulative_g_linear = 1

    for g_db, nf_db in chain:
        g_linear = db_to_linear(g_db)
        f_linear = db_to_linear(nf_db)

        if cumulative_g_linear == 1: # Для первого элемента
            total_f += f_linear
        else: # Для последующих элементов
            total_f += (f_linear - 1) / cumulative_g_linear
        
        cumulative_g_linear *= g_linear
        
    return linear_to_db(total_f)

# Исходные данные для варианта 9
pf1 = (-2, 2)       # ПФ1, NF принят равным потерям
mshu = (4, 2)       # МШУ
smesitel = (-4, 4)  # Смеситель, NF принят равным потерям
pf2 = (-2, 2)       # ПФ2, NF принят равным потерям
upku = (23, 3)      # УПКУ
kabel = (-3, 3)     # Кабель, NF принят равным потерям

# Случай 1: Сигнал проходит через кабель перед приемником
chain_case_1 = [kabel, pf1, mshu, smesitel, pf2, upku]
nf_total_case_1 = calculate_total_noise_figure(chain_case_1)

# Случай 2: МШУ расположен непосредственно на выходе антенны
chain_case_2 = [mshu, smesitel, pf2, upku]
nf_total_case_2 = calculate_total_noise_figure(chain_case_2)

print("### Раздел 1: Коэффициент шума приемника")
print(f"Случай 1 (с кабелем): Общий коэффициент шума = {nf_total_case_1:.2f} дБ")
print(f"Случай 2 (без кабеля, МШУ первый): Общий коэффициент шума = {nf_total_case_2:.2f} дБ")

NF_RECEIVER_DB = nf_total_case_2


### Раздел 2

# Исходные данные для варианта 9
MODULATION = "KAM-64"
RB_MBPS = 48  # Скорость передачи в Мбит/с
BER = 1e-5

N0_DBM_HZ = -174  # N0 при T=290K

EB_N0_DB = 14.2 # Требуемое отношение Eb/N0 для 64-QAM при BER=10^-5
NF_DB = NF_RECEIVER_DB

# из Мбит/с в бит/с
rb_bps = RB_MBPS * 1e6

# дБм = (Eb/N0)_дБ + 10*log10(Rb) + NF_дБ + N0_дБм/Гц
p_in_min_dbm = EB_N0_DB + 10 * math.log10(rb_bps) + NF_DB + N0_DBM_HZ

print("\n### Раздел 2: Необходимая мощность сигнала на входе приемника")
print(f"Модуляция: {MODULATION}, Скорость: {RB_MBPS} Мбит/с, BER: {BER:.0e}")
print(f"Требуемое Eb/N0 (из графика): {EB_N0_DB} дБ")
print(f"Коэффициент шума приемника (из Раздела 1): {NF_DB:.2f} дБ")
print(f"Минимальная необходимая мощность сигнала на входе: {p_in_min_dbm:.2f} дБм")

P_IN_MIN_DBM_TASK2 = p_in_min_dbm

### Раздел 3

# Исходные данные для задачи 3
GT_DBI = 7       # Усиление антенны передатчика
GR_DBI = 2       # Усиление антенны приемника
HBS_M = 30       # Высота антенны базовой станции (БС) в метрах
HMS_M = 2        # Высота антенны мобильной станции (МС) в метрах
F_MHZ = 900      # Частота в МГц
RB_BPS = 48 * 1e6 # Скорость передачи данных
NF_DB = NF_RECEIVER_DB # КШ из Раздела 1

def hata_path_loss(d_km, f_mhz, hbs_m, hms_m):
    # Корректирующий фактор для высоты антенны МС
    a_hms = (1.1 * math.log10(f_mhz) - 0.7) * hms_m - (1.56 * math.log10(f_mhz) - 0.8)

    # Формула потерь
    pl_db = 69.55 + 26.16 * math.log10(f_mhz) - 13.82 * math.log10(hbs_m) - a_hms + (44.9 - 6.55 * math.log10(hbs_m)) * math.log10(d_km)
            
    return pl_db

def calculate_pr_min(eb_n0_db, rb_bps, nf_db): # Расчет минимальной мощности на входе приемника
    N0_DBM_HZ = -174
    return eb_n0_db + 10 * math.log10(rb_bps) + nf_db + N0_DBM_HZ

print("\n### Раздел 3: Параметры системы связи (модель Хата)")

# ### 3.1
print("\n# 3.1: Расчет минимальной мощности передатчика")
# Условия: BER = 10^-4, расстояние d = 1 км
d1_km = 1
ber1 = 1e-4
# Eb/N0 для 64-QAM и BER=10^-4 (из графика)
eb_n0_1_db = 14.2

pr_min_1_dbm = calculate_pr_min(eb_n0_1_db, RB_BPS, NF_DB)
pl_1_db = hata_path_loss(d1_km, F_MHZ, HBS_M, HMS_M)
pt_min_1_dbm = pr_min_1_dbm - GT_DBI - GR_DBI + pl_1_db

print(f"Для достижения BER = {ber1:.0e} на расстоянии {d1_km} км:")
print(f"  Чувствительность приемника (Pr_min): {pr_min_1_dbm:.2f} дБм")
print(f"  Потери в канале (PL): {pl_1_db:.2f} дБ")
print(f"  Минимальная мощность передатчика (Pt_min): {pt_min_1_dbm:.2f} дБм")


# ### 3.2
print("\n# 3.2: Определение максимального расстояния")
# Условия: Pt = 35 дБм, BER = 10^-3
pt2_dbm = 35
ber2 = 1e-3
# Eb/N0 для 64-QAM и BER=10^-3 (из графика)
eb_n0_2_db = 14.2

pr_min_2_dbm = calculate_pr_min(eb_n0_2_db, RB_BPS, NF_DB)
pl_max_2_db = pt2_dbm + GT_DBI + GR_DBI - pr_min_2_dbm

# PL = C1 + C2 * log10(d) => log10(d) = (PL - C1) / C2
C1 = 69.55 + 26.16 * math.log10(F_MHZ) - 13.82 * math.log10(HBS_M) - ((1.1 * math.log10(F_MHZ) - 0.7) * HMS_M - (1.56 * math.log10(F_MHZ) - 0.8))
C2 = 44.9 - 6.55 * math.log10(HBS_M)
log10_d2 = (pl_max_2_db - C1) / C2
d2_max_km = 10**log10_d2

print(f"При мощности передатчика {pt2_dbm} дБм для BER = {ber2:.0e}:")
print(f"  Максимально допустимые потери (PL_max): {pl_max_2_db:.2f} дБ")
print(f"  Максимальное расстояние: {d2_max_km:.2f} км")

# ### 3.3
print("\n# 3.3: Определение макс. расстояния с удвоенной высотой БС")
# Условия: Pt = 35 дБм, hbs_new = 60 м, BER = 10^-4
pt3_dbm = 35
hbs3_m = 2 * HBS_M
ber3 = 1e-4
# Pr_min из 3.1(BER тот же)
pr_min_3_dbm = pr_min_1_dbm

# PL_max = Pt + Gt + Gr - Pr_min
pl_max_3_db = pt3_dbm + GT_DBI + GR_DBI - pr_min_3_dbm
C1_new = 69.55 + 26.16 * math.log10(F_MHZ) - 13.82 * math.log10(hbs3_m) - ((1.1 * math.log10(F_MHZ) - 0.7) * HMS_M - (1.56 * math.log10(F_MHZ) - 0.8))
C2_new = 44.9 - 6.55 * math.log10(hbs3_m)
log10_d3 = (pl_max_3_db - C1_new) / C2_new
d3_max_km = 10**log10_d3

print(f"При Pt={pt3_dbm} дБм, BER={ber3:.0e} и новой высоте БС {hbs3_m} м:")
print(f"  Максимально допустимые потери (PL_max): {pl_max_3_db:.2f} дБ")
print(f"  Максимальное расстояние: {d3_max_km:.2f} км")


### Раздел 4
# Исходные данные для задачи 4
PT_DBM = 35       # Мощность передатчика
GT_DB = 5         # Усиление антенны передатчика
GR_DB = 1         # Усиление антенны приемника
SIGMA_S_DB = 6    # Стандартное отклонение затенения

# Параметры модели потерь
P_EXP = 3.5       # Экспонента потерь распространения
D0_M = 100        # Опорное расстояние в метрах

# Данные из задачи 2 
pr_threshold_dbm = P_IN_MIN_DBM_TASK2

def path_loss_shadowing_model(d_m, d0_m, p_exp):
    return 74 + 10 * p_exp * math.log10(d_m / d0_m)

# Q(x) = 1 - CDF(x)
def q_function(x):
    return 1 - norm.cdf(x)

print("\n### Раздел 4: Вероятность прерывания связи с затенением")
print(f"Пороговая мощность приемника (из Раздела 2): {pr_threshold_dbm:.2f} дБм")

# 4.1
print("\n# 4.1: Расчет вероятности прерывания на разных расстояниях")
distances_km = [1, 2, 5]

for d_km in distances_km:
    d_m = d_km * 1000
    # средние потери
    pl_mean_db = path_loss_shadowing_model(d_m, D0_M, P_EXP)
    # средняя принятая мощность
    pr_mean_dbm = PT_DBM + GT_DB + GR_DB - pl_mean_db
    # аргумент Q-функции
    x = (pr_mean_dbm - pr_threshold_dbm) / SIGMA_S_DB
    # вероятность прерывания
    p_outage = q_function(x)
    
    print(f"Расстояние: {d_km} км")
    print(f"  Средняя принятая мощность: {pr_mean_dbm:.2f} дБм")
    print(f"  Вероятность прерывания связи: {p_outage:.4f} (или {p_outage*100:.2f}%)")


# 4.2 
print("\n# 4.2: Расчет мощности для заданной вероятности прерывания")
d_task2_km = 3
p_outage_target = 0.01

x_target = 2.33 # Из таблицы 

pl_task2_db = path_loss_shadowing_model(d_task2_km * 1000, D0_M, P_EXP)

# x = (Pr_mean - Pr_thresh) / sigma => Pr_mean = x * sigma + Pr_thresh
pr_mean_req_dbm = x_target * SIGMA_S_DB + pr_threshold_dbm

# Pr_mean = Pt + Gt + Gr - PL => Pt = Pr_mean - Gt - Gr + PL
pt_req_dbm = pr_mean_req_dbm - GT_DB - GR_DB + pl_task2_db

print(f"Для вероятности прерывания < {p_outage_target:.2f} на расстоянии {d_task2_km} км:")
print(f"  Потери в канале: {pl_task2_db:.2f} дБ")
print(f"  Требуемая средняя мощность на приеме: {pr_mean_req_dbm:.2f} дБм")
print(f"  Требуемая мощность передатчика должна быть больше: {pt_req_dbm:.2f} дБм\n")
