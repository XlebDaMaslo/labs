import math

def autocorr_check(seq):
    n = len(seq)
    first_correlation = None

    for shift in range(1, n):
        compare = []
        for j in range(n):
            shifted_index = (j + shift) % n
            if seq[j] == seq[shifted_index]:
                compare.append(1)
            else:
                compare.append(0)
        count1 = compare.count(1)
        count0 = compare.count(0)
        correlation = (1/n) * (count1 - count0)

        if first_correlation is None:
            first_correlation = correlation
        elif correlation != first_correlation:
            return False

    return True

def gen_gold_seq(initial_state1, initial_state2, polynomial1_bin, polynomial2_bin):
    n = len(polynomial1_bin)
    init_poly1 = polynomial1_bin
    init_poly2 = polynomial2_bin

    x = list(bin(initial_state1)[2:].zfill(n))
    y = list(bin(initial_state2)[2:].zfill(n))

    polynomial1 = [index for index in range(len(polynomial1_bin)) if polynomial1_bin[index] == '1']
    polynomial2 = [index for index in range(len(polynomial2_bin)) if polynomial2_bin[index] == '1']

    sequence = []

    for _ in range((2**n) - 1):
        out = int(x[-1]) ^ int(y[-1])

        new_x = 0
        for tap in polynomial1:
            new_x ^= int(x[tap])
        x = [str(new_x)] + x[:-1]

        new_y = 0
        for tap in polynomial2:
            new_y ^= int(y[tap])
        y = [str(new_y)] + y[:-1]

        sequence.append(out)
    if not autocorr_check(sequence):
        if polynomial1_bin == '11111':
            polynomial1_bin = init_poly1
            polynomial2_bin = bin(int(polynomial2_bin, 2) + 1)[2:].zfill(len(polynomial2_bin))
            sequence = gen_gold_seq(initial_state1, initial_state2, polynomial1_bin, polynomial2_bin)
        
        elif polynomial2_bin == '11111':
            polynomial2_bin = init_poly2
            polynomial1_bin = bin(int(polynomial1_bin, 2) + 1)[2:].zfill(len(polynomial1_bin))
            sequence = gen_gold_seq(initial_state1, initial_state2, polynomial1_bin, polynomial2_bin)

        else:
            polynomial1_bin = bin(int(polynomial1_bin, 2) + 1)[2:].zfill(len(polynomial1_bin))
            sequence = gen_gold_seq(initial_state1, initial_state2, polynomial1_bin, polynomial2_bin)
    #print(polynomial1_bin, polynomial2_bin)
    return sequence

def autocorr(seq):
    header = f"{'Сдвиг':<8}{' | '.join([f'{i+1}' for i in range(len(seq))])} | {'Автокорреляция':}"
    print(header)
    new_seq = seq
    for i in range(len(seq)+1):
        compare = []
        for j in range(len(seq)):
            if seq[j] == new_seq[j]:
                compare.append(1)
            else:
                compare.append(0)
        count1 = compare.count(1)
        count0 = compare.count(0)
        correlation = (1/(2**(math.log((len(seq)+1),2)) - 1)) * (count1 - count0)
        bits = ' | '.join(map(str, compare))
        print(f"{i:<8}{bits} | {correlation:<15}")
        new_seq = [new_seq[len(new_seq)-1]] + new_seq[:-1]

def correlation(a, b):
    result = 0
    for i in range(len(a)):
        result += a[i] * b[i]
    return result

def normalized_correlation(a, b):
    sum_a = 0
    sum_b = 0
    for i in range(len(a)):
        sum_a += a[i] * a[i]
        sum_b += b[i] * b[i]
    return correlation(a, b) / ((sum_a * sum_b) ** (1/2))

def corr_print(seq1, seq2):
    header = f"{'\nСдвиг':<8}{' | '.join([f'{i+1}' for i in range(len(seq1))])} | {'Корреляция'} | {'Норм. корреляция':}"
    print(header)
    for i in range(len(seq1)+1):
        compare = []
        for j in range(len(seq1)):
            if seq1[j] == seq2[j]:
                compare.append(1)
            else:
                compare.append(0)
        corr = correlation(seq1, seq2)
        n_corr = normalized_correlation(seq1, seq2)
        bits = ' | '.join(map(str, compare))
        print(f"{i:<8}{bits} | { corr:>8} | { n_corr}")
        seq2 = [seq2[len(seq2)-1]] + seq2[:-1]
    return 0
    

number_st = 10 # Номер по списку
number_st2 = number_st + 7

# x^5 + x^4 + 1 первый регистр по схеме
polynomial1_bin = "00011"

# x^5 + x^2 + 1 второй регистр по схеме
polynomial2_bin = "01001"

sequence1 = gen_gold_seq(number_st, number_st2, polynomial1_bin, polynomial2_bin)
print(sequence1)
print(sequence1.count(1), sequence1.count(0))
autocorr(sequence1)

sequence2 = gen_gold_seq(number_st+1, (number_st+7)-5, polynomial1_bin, polynomial2_bin)
corr_print(sequence1, sequence2)