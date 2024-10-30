def gen_gold_seq(num1, num2):
    x = list(bin(num1)[2:])
    for i in range(5):
        if len(x) <=4:
            x = [0] + x
        else:
            break
    
    y = list(bin(num2)[2:])
    for i in range(5):
        if len(y) <=4:
            y = [0] + y
        else:
            break
    
    sequence = []

    #even
    if num1 > 0:#% 2 == 0:
        for i in range((2**(len(x)) - 1)):
            #print(x)
            #print(y)
            out = int(x[4]) ^ int(y[4])
            #print(out,'\n')
            x = [(int(x[2]) ^ int(x[4]))] + x[:-1]
            y = [(int(y[2]) ^ int(y[4]))] + y[:-1]
        
            sequence.append(out)
    #odd
    else:
        for i in range((2**(len(x)) - 1)):
            #print(x)
            #print(y)
            out = int(x[4]) ^ int(y[4])
            #print(out,'\n')
            x = [(int(x[3]) ^ int(x[4]))] + x[:-1]
            y = [(int(y[1]) ^ int(y[4]))] + y[:-1]
        
            sequence.append(out)
    
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
        correlation = (1/(2**5-1)) * (count1 - count0)
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
        

number_st = 10
sequence1 = gen_gold_seq(number_st, number_st+7)
print(sequence1)
count1 = sequence1.count(1)
count0 = sequence1.count(0)
print(count0, count1)
autocorr(sequence1)
sequence2 = gen_gold_seq(number_st+1, (number_st+7)-5)
corr_print(sequence1, sequence2)
