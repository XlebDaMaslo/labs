import random

def generate_data(N):
  return ''.join(str(random.randint(0,1)) for _ in range(N))

def calculate_crc(data, polynomial):
    polynomial_len = len(polynomial)
    data += '0' * (polynomial_len - 1) 

    data_len = len(data)

    for i in range(data_len - polynomial_len + 1):
        if data[i] == '1':
            for j in range(polynomial_len):
                data = data[:i + j] + str(int(data[i + j]) ^ int(polynomial[j])) + data[i + j + 1:]

    crc = data[-polynomial_len + 1:]
    return crc


def calculate_crc_receiver(data_with_crc, polynomial):
    polynomial_len = len(polynomial)
    data_len = len(data_with_crc)

    for i in range(data_len - polynomial_len + 1):
        if data_with_crc[i] == '1':
            for j in range(polynomial_len):
                data_with_crc = data_with_crc[:i + j] + str(int(data_with_crc[i + j]) ^ int(polynomial[j])) + data_with_crc[i + j + 1:]

    crc_check = data_with_crc[-(polynomial_len - 1):]

    return crc_check

def bit_distortion(data, index): # Искажение бита в строке данных
    return data[:index] + ('1' if data[index] == '0' else '0') + data[index + 1:]

# 1, 2
N = 20 + 10 # порядковый номер в журнале
polynomial = '11011110' #G=x7+x6+x4+x3+x2+x
data = generate_data(N)

crc = calculate_crc(data, polynomial)
print("CRC на передатчике:", crc)

# 3
data_with_crc = data + crc
crc_receiver = calculate_crc_receiver(data_with_crc, polynomial)

print("CRC на приемнике:", crc_receiver)

if crc_receiver != crc:
    print("Ошибка обнаружена!")
else:
    print("Передача без ошибок.")

# 4
N = 250
data = generate_data(N)
crc = calculate_crc(data, polynomial)

data_with_crc = data + crc

# 5
errors_detected = 0
errors_not_detected = 0

for i in range(len(data_with_crc)):
    corrupted_data_with_crc = bit_distortion(data_with_crc, i)
    crc_receiver = calculate_crc_receiver(corrupted_data_with_crc, polynomial)

    if crc_receiver != crc:
        errors_detected += 1
    else:
        errors_not_detected += 1

print(f"Обнаружено ошибок: {errors_detected}")
print(f"Не обнаружено ошибок: {errors_not_detected}")