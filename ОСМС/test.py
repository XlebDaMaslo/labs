import random
import math
import matplotlib.pyplot as plt

def correlation(a, b):
    return sum(x * y for x, y in zip(a, b))

def normalized_correlation(a, b):
    sum_a = sum(x * x for x in a)
    sum_b = sum(x * x for x in b)
    if sum_a == 0 or sum_b == 0:
        return 0
    return correlation(a, b) / math.sqrt(sum_a * sum_b)

def sample_normal():
    while True:
        u = random.uniform(-1.0, 1.0)
        v = random.uniform(-1.0, 1.0)
        r = u * u + v * v
        if r != 0 and r < 1:
            break
    c = math.sqrt(-2.0 * math.log(r) / r)
    return u * c

random.seed()

n = 10
a = [sample_normal() for _ in range(n)]
b = [sample_normal() for _ in range(n)]

a_corr = []
b_corr = []

for j in range(n):
    a_shifted = a[1:] + a[:1]
    b_shifted = b[1:] + b[:1]
    a_corr.append(normalized_correlation(a, a_shifted))
    b_corr.append(normalized_correlation(b, b_shifted))

plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(a_corr)
plt.title("автокорреляция a")
plt.xlabel("сдвиг")
plt.ylabel("значение")

plt.subplot(2, 1, 2)
plt.plot(b_corr)
plt.title("автокорреляция b")
plt.xlabel("сдвиг")
plt.ylabel("значение")

plt.tight_layout()
plt.show()

