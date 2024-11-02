def gen_gold_seq(num1, num2, poly1, poly2):
    # Определяем длину регистра
    length = max(len(poly1), len(poly2)) - 1  # Длина будет определяться по максимальной степени полинома
    x = list(bin(num1)[2:].zfill(length))  # Начальное состояние для первого регистра
    y = list(bin(num2)[2:].zfill(length))  # Начальное состояние для второго регистра

    sequence = []

    # Генерация последовательности
    for _ in range((2 ** length) - 1):  # Длина последовательности равна 2^n - 1
        out = int(x[-1]) ^ int(y[-1])  # Выходной бит

        # Обновление регистра x
        new_bit_x = sum(int(x[i]) for i in range(len(poly1)) if poly1[i] == '1' and i < len(x)) % 2
        x = [new_bit_x] + x[:-1]  # Сдвиг влево и добавление нового бита

        # Обновление регистра y
        new_bit_y = sum(int(y[i]) for i in range(len(poly2)) if poly2[i] == '1' and i < len(y)) % 2
        y = [new_bit_y] + y[:-1]  # Сдвиг влево и добавление нового бита
        
        sequence.append(out)  # Добавление выходного бита в последовательность

    return sequence

# Пример использования с полиномами и начальными значениями
number_st = 10  # Начальное значение для первого регистра
number_st2 = number_st + 7  # Начальное значение для второго регистра

# Задаём полиномы в двоичном виде
polynomial1 = '110001'  # Полином x^5 + x^4 + 1
polynomial2 = '101001'  # Полином x^5 + x^2 + 1

# Генерация последовательности Голда
sequence1 = gen_gold_seq(number_st, number_st2, polynomial1, polynomial2)
print(sequence1)
print("Количество единиц:", sequence1.count(1), "Количество нулей:", sequence1.count(0))
