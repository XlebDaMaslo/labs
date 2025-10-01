import math
import random

def solve_discrete_log(a, y, p):
    # Определение m, округляя корень из (p-1) вверх
    m = math.ceil(math.sqrt(p - 1))

    # Шаги младенца (Baby steps)
    baby_steps = {}
    val = 1
    for j in range(m):
        if val not in baby_steps:
            baby_steps[val] = j
        val = (val * a) % p

    # Шаги великана (Giant steps)
    # a^(p-2) ≡ a^(-1) (mod p)
    a_m = pow(a, m, p)
    
    a_inv_m = pow(a_m, -1, p)
    
    giant_step_val = y
    for i in range(m):
        # Совпадения в значениях шагов младенца
        if giant_step_val in baby_steps:
            j = baby_steps[giant_step_val]
            return i * m + j
        giant_step_val = (giant_step_val * a_inv_m) % p

    return "Решение не найдено"

def modular_pow(base, exp, modulus): # возведение числа в степень по модулю (y = a^x mod p)
    result = 1
    base %= modulus
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % modulus
        exp //= 2
        base = (base * base) % modulus
    return result

def is_prime(n, k=10): # тест простоты Ферма
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

def generate_params():
    print("\nГенерация параметров...")
    while True:
        p = random.randint(10000, 50000)
        if is_prime(p):
            break
            
    a = random.randint(2, p - 2)
    x = random.randint(2, p - 2)
    
    # y = a^x mod p
    y = pow(a, x, p)
    
    print(f"Сгенерировано простое p = {p}")
    print(f"Сгенерировано основание a = {a}")
    print(f"Вычислен y = {y}")
    print(f"(Секретный показатель x равен {x} для проверки)")
    
    return a, y, p

def main():
    while True:
        print("\n" + "="*30)
        print("     Решение дискретного логарифма")
        print("         y = a^x mod p")
        print("="*30)
        print("Режим работы:")
        print("1. Ввести параметры (a, y, p) с клавиатуры")
        print("2. Сгенерировать параметры автоматически")
        print("3. Выход")
        
        choice = input("Введите режим: ")
        
        a, y, p = None, None, None
        
        if choice == '1':
            try:
                p = int(input("Введите простое число p: "))
                a = int(input(f"Введите основание a (2 <= a < {p}): "))
                y = int(input(f"Введите результат y (1 <= y < {p}): "))
                
                if not (2 <= a < p and 1 <= y < p):
                    print("\n[Ошибка] Неверные параметры. a и y должны быть в указанных диапазонах.")
                    continue
                
            except ValueError:
                print("\n[Ошибка] Пожалуйста, вводите целые числа.")
                continue
                
        elif choice == '2':
            a, y, p = generate_params()

        elif choice == '3':
            print("Выход из программы.")
            break
            
        else:
            print("\n[Ошибка] Неверный выбор. Пожалуйста, введите 1, 2 или 3.")
            continue
        
        if all(v is not None for v in [a, y, p]):
            print(f"\nРешение уравнения {y} = {a}^x mod {p}")
            result = solve_discrete_log(a, y, p)
            
            if isinstance(result, int):
                print(f"Найденный x = {result}")
                # Проверка
                if pow(a, result, p) == y:
                    print("Проверка: pow(a, x, p) == y. Решение верно.")
                else:
                    print("Проверка: pow(a, x, p) != y. Решение неверно.")
            else:
                print(result)

if __name__ == "__main__":
    main()