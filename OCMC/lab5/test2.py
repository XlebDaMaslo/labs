import random

def generate_data(N):
  return ''.join(str(random.randint(0,1)) for _ in range(N))

def calculate_crc(data, polynomial):
    polynomial_len = len(polynomial)
    data += '0' * (polynomial_len - 1)  # Добавляем нули для вычисления остатка (CRC)

    data_len = len(data)

    for i in range(data_len - polynomial_len + 1):
        if data[i] == '1':
            for j in range(polynomial_len):
                data = data[:i + j] + str(int(data[i + j]) ^ int(polynomial[j])) + data[i + j + 1:]

    crc = data[-(polynomial_len - 1):]
    return crc

def calculate_crc_receiver(data_with_crc, polynomial):
    polynomial_len = len(polynomial)
    crc_len = polynomial_len - 1

    data = data_with_crc[:-crc_len]  # Данные без CRC
    received_crc = data_with_crc[-crc_len:]  # Полученный CRC (последние биты)

    calculated_crc = calculate_crc(data, polynomial)

    crc_match = received_crc == calculated_crc

    error = not crc_match

    return calculated_crc, error


def bit_distortion(data, index): # Искажение бита в строке данных
    return data[:index] + ('1' if data[index] == '0' else '0') + data[index + 1:]

N = 2000
polynomial = ['1101','10000111']

data = generate_data(N)
crc4 = calculate_crc(data, polynomial[0])
crc8 = calculate_crc(data, polynomial[1])

data_with_crc4 = data + crc4
data_with_crc8 = data + crc8

errors_detected_4 = 0
errors_not_detected_4 = 0

errors_detected_8 = 0
errors_not_detected_8 = 0

for i in range(len(data_with_crc4)):
    corrupted_data_with_crc = bit_distortion(data_with_crc4, i)
    crc_receiver, has_error = calculate_crc_receiver(corrupted_data_with_crc, polynomial[0])

    if has_error:
        errors_detected_4 += 1
    else:
        errors_not_detected_4 += 1

print(f"Обнаружено ошибок для полинома {polynomial[0]}: {errors_detected_4}")
print(f"Не обнаружено ошибок для полинома {polynomial[0]}: {errors_not_detected_4}")

for i in range(len(data_with_crc8)):
    corrupted_data_with_crc = bit_distortion(data_with_crc8, i)
    crc_receiver, has_error = calculate_crc_receiver(corrupted_data_with_crc, polynomial[1])

    if has_error:
        errors_detected_8 += 1
    else:
        errors_not_detected_8 += 1

print(f"Обнаружено ошибок для полинома {polynomial[1]}: {errors_detected_8}")
print(f"Не обнаружено ошибок для полинома {polynomial[1]}: {errors_not_detected_8}")