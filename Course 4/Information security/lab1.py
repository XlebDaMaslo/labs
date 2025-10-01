import random


def modular_pow(base, exp, modulus): # возведение числа в степень по модулю (y = a^x mod p)
    result = 1
    base %= modulus
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % modulus
        exp //= 2
        base = (base * base) % modulus
    return result

def is_prime_fermat(n, k=10): # тест простоты Ферма
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    for _ in range(k):
        a = random.randint(2, n - 2)
        
        if modular_pow(a, n - 1, n) != 1: # a^(n-1) ≡ 1 (mod n)
            return False
            
    return True

def extended_gcd(a, b): # обобщённый алгоритм Евклида
    if a == 0:
        return b, 0, 1
    
    gcd, x1, y1 = extended_gcd(b % a, a)
    
    x = y1 - (b // a) * x1
    y = x1
    
    return gcd, x, y

def generate_prime_in_range(min_val, max_val):
    while True:
        num = random.randint(min_val, max_val)
        if num % 2 != 0 and is_prime_fermat(num):
            return num

def menu():
    print("\n--- Криптографическая библиотека ---")
    print("1. Быстрое возведение в степень по модулю (a^x mod p)")
    print("2. Тест простоты Ферма")
    print("3. Обобщённый алгоритм Евклида (поиск НОД и коэффициентов)")
    print("4. Выход")
    return input("Выберите опцию: ")

if __name__ == "__main__":
    while True:
        choice = menu()

        if choice == '1':
            print("\n--- Возведение в степень по модулю ---")
            try:
                a = int(input("Введите основание a: "))
                x = int(input("Введите показатель степени x: "))
                p = int(input("Введите модуль p: "))
                result = modular_pow(a, x, p)
                print(f"Результат: {a}^{x} mod {p} = {result}")
            except ValueError:
                print("Ошибка: вводите только целые числа.")

        elif choice == '2':
            print("\n--- Тест простоты Ферма ---")
            try:
                n = int(input("Введите число для проверки на простоту: "))
                if is_prime_fermat(n):
                    print(f"Число {n} с высокой вероятностью является простым.")
                else:
                    print(f"Число {n} является составным.")
            except ValueError:
                print("Ошибка: вводите только целые числа.")

        elif choice == '3':
            print("\n--- Обобщённый алгоритм Евклида ---")
            print("Выберите способ получения чисел a и b:")
            print("  1. Ввести с клавиатуры")
            print("  2. Сгенерировать случайные числа")
            print("  3. Сгенерировать случайные ПРОСТЫЕ числа")
            sub_choice = input("Ваш выбор: ")

            try:
                if sub_choice == '1':
                    a = int(input("Введите число a: "))
                    b = int(input("Введите число b: "))
                elif sub_choice == '2':
                    a = random.randint(1, 10**9)
                    b = random.randint(1, 10**9)
                    print(f"Сгенерированы числа: a = {a}, b = {b}")
                elif sub_choice == '3':
                    print("Генерация простых чисел (может занять несколько секунд)...")
                    a = generate_prime_in_range(10**8, 10**9)
                    b = generate_prime_in_range(10**8, 10**9)
                    print(f"Сгенерированы простые числа: a = {a}, b = {b}")
                else:
                    print("Неверный выбор.")
                    continue

                gcd, x, y = extended_gcd(a, b)
                print(f"НОД({a}, {b}) = {gcd}")
                print(f"Найдены коэффициенты x = {x}, y = {y}")
                print(f"Проверка: {a} * ({x}) + {b} * ({y}) = {a * x + b * y}")

            except (ValueError, NameError):
                print("Ошибка: вводите только целые числа или выберите корректный пункт меню.")

        elif choice == '4':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите опцию от 1 до 4.")
