import random
import time
import matplotlib.pyplot as plt

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
                data_with_crc = data_with_crc[:i+j] + str(int(data_with_crc[i+j]) ^ int(polynomial[j])) + data_with_crc[i+j+1:]


    crc = data_with_crc[-polynomial_len + 1:]
    error = any(bit == '1' for bit in crc)  # Ошибка, если CRC не все нули
    return crc, error

N = 100

polynomial = ['1101','101101','11011010']
times = [[],[],[]]
for i in range(N, 2000, 50):
    data = generate_data(i)
    for j in polynomial:
        ti = []
        for k in range(100):
            start_time = time.time()
            crc = calculate_crc(data, j)
            end_time = time.time()
            ti.append(end_time - start_time)
        times[polynomial.index(j)].append(sum(ti)/100)
        #data_with_crc = data + crc
        #crc_receiver, has_error = calculate_crc_receiver(data_with_crc, j)


N = range(100, 2000, 50)

plt.figure()
plt.plot(N, times[0], label=f'Polynomial: {polynomial[0]}')
plt.xlabel('N')
plt.ylabel('Time (sec)')
plt.legend()
plt.grid(True)

plt.figure()
plt.plot(N, times[1], label=f'Polynomial: {polynomial[1]}')
plt.xlabel('N')
plt.ylabel('Time (sec)')
plt.legend()
plt.grid(True)

plt.figure()
plt.plot(N, times[2], label=f'Polynomial: {polynomial[2]}')
plt.xlabel('N')
plt.ylabel('Time (sec)')
plt.legend()
plt.grid(True)

plt.show()