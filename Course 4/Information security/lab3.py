import random

from lab1 import is_prime_fermat, generate_prime_in_range, modular_pow

def diffie_hellman_key_exchange(p=None, g=None, X_A=None, X_B=None):
    if p is None:
        p = generate_prime_in_range(10**5, 10**6)  # простое число
    if g is None:
        g = random.randint(2, p - 2)
    if X_A is None:
        X_A = random.randint(2, p - 2)
    if X_B is None:
        X_B = random.randint(2, p - 2)

    print(f"p = {p}")
    print(f"g = {g}")
    print(f"Секретный ключ A: X_A = {X_A}")
    print(f"Секретный ключ B: X_B = {X_B}")

    # открытые ключи
    Y_A = modular_pow(g, X_A, p)
    Y_B = modular_pow(g, X_B, p)

    print(f"Открытый ключ A: Y_A = {Y_A}")
    print(f"Открытый ключ B: Y_B = {Y_B}")

    # общий секрет
    K_A = modular_pow(Y_B, X_A, p)
    K_B = modular_pow(Y_A, X_B, p)

    print(f"Общий ключ, вычисленный A: {K_A}")
    print(f"Общий ключ, вычисленный B: {K_B}")

    if K_A == K_B:
        print("Ключи совпадают — обмен успешен.")
    else:
        print("Ключи не совпадают — ошибка.")

def main():
    while True:
        print("\n=== Диффи–Хеллман ===")
        print("1. Ввести p, g, X_A, X_B вручную")
        print("2. Сгенерировать параметры автоматически")
        print("3. Выход")

        choice = input("Ваш выбор: ")

        if choice == '1':
            try:
                p = int(input("Введите простое число p: "))
                if not is_prime_fermat(p):
                    print("p не является простым числом.")
                    continue
                g = int(input(f"Введите g (2 <= g < {p}): "))
                X_A = int(input(f"Введите секретный ключ X_A (2 <= X_A < {p}): "))
                X_B = int(input(f"Введите секретный ключ X_B (2 <= X_B < {p}): "))
                diffie_hellman_key_exchange(p, g, X_A, X_B)
            except ValueError:
                print("Ошибка: вводите только целые числа.")
        elif choice == '2':
            diffie_hellman_key_exchange()
        elif choice == '3':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор.")

if __name__ == "__main__":
    main()
