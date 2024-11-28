import random
import numpy as np
import matplotlib.pyplot as plt

def generate_data(N):
    return "".join(str(random.randint(0, 1)) for _ in range(N))

def calculate_crc_numpy(data, polynomial):
    polynomial_len = len(polynomial)
    data_np = np.array([int(bit) for bit in data])
    polynomial_np = np.array([int(bit) for bit in polynomial])
    data_np = np.concatenate([data_np, np.zeros(polynomial_len - 1, dtype=int)])
    data_len = len(data_np)

    for i in range(data_len - polynomial_len + 1):
        if data_np[i] == 1:
            data_np[i:i + polynomial_len] = np.bitwise_xor(data_np[i:i + polynomial_len], polynomial_np)

    crc = data_np[-(polynomial_len - 1):]
    return "".join(map(str, crc))


def calculate_crc_receiver_numpy(data_with_crc, polynomial):
    polynomial_len = len(polynomial)
    data_np = np.array([int(bit) for bit in data_with_crc])
    polynomial_np = np.array([int(bit) for bit in polynomial])
    data_len = len(data_np)

    for i in range(data_len - polynomial_len + 1):
        if data_np[i] == 1:
            data_np[i:i + polynomial_len] = np.bitwise_xor(data_np[i:i + polynomial_len], polynomial_np)

    crc_check = data_np[-(polynomial_len - 1):]
    return "".join(map(str, crc_check))

def bit_distortion(data, index):
    data_list = list(data)
    data_list[index] = '1' if data_list[index] == '0' else '0'
    return "".join(data_list)



if __name__ == "__main__":
    N = 4000
    n_list = []
    polynomial = ['1101', '10000111']
    list4 = []
    list8 = []

    for i in range(500, N, 500):
        print("Работает")
        n_list.append(i)

        data = generate_data(i)
        crc4 = calculate_crc_numpy(data, polynomial[0])
        crc8 = calculate_crc_numpy(data, polynomial[1])

        data_with_crc4 = data + crc4
        data_with_crc8 = data + crc8

        errors_not_detected_4 = 0
        errors_not_detected_8 = 0

        for j in range(len(data_with_crc4)):
            corrupted_data_with_crc = bit_distortion(data_with_crc4, j)
            crc_receiver = calculate_crc_receiver_numpy(corrupted_data_with_crc, polynomial[0])
            if crc_receiver == crc4:
                errors_not_detected_4 += 1

        for j in range(len(data_with_crc8)):
            corrupted_data_with_crc = bit_distortion(data_with_crc8, j)
            crc_receiver = calculate_crc_receiver_numpy(corrupted_data_with_crc, polynomial[1])
            if crc_receiver == crc8:
                errors_not_detected_8 += 1
        
        list4.append(errors_not_detected_4)
        list8.append(errors_not_detected_8)

    plt.figure()

    plt.subplot(1, 2, 1)
    plt.plot(n_list, list4)
    plt.xlabel("N")
    plt.ylabel("Не обнаружено ошибок (CRC4)")
    plt.title("CRC4")

    plt.subplot(1, 2, 2)
    plt.plot(n_list, list8)
    plt.xlabel("N")
    plt.ylabel("Не обнаружено ошибок (CRC8)")
    plt.title("CRC8")


    plt.tight_layout()
    plt.show()