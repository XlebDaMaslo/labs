#include <stdio.h>
#include <stdlib.h>
#include <math.h>

void gen_gold_seq(int num1, int num2, int *sequence) {
    int x[5], y[5];
    int i, j;
    
    for (i = 4; i >= 0; i--) {
        x[i] = num1 % 2;
        num1 /= 2;
        y[i] = num2 % 2;
        num2 /= 2;
    }

    for (i = 0; i < 31; i++) {
        sequence[i] = x[4] ^ y[4];
        int temp_x = x[2] ^ x[4];
        int temp_y = y[2] ^ y[4];

        for (j = 4; j > 0; j--) {
            x[j] = x[j - 1];
            y[j] = y[j - 1];
        }
        x[0] = temp_x;
        y[0] = temp_y;
    }
}

void autocorr(int *seq, int len) {
    printf("Сдвиг    |");
    for (int i = 0; i < len; i++) {
        printf(" %d |", i + 1);
    }
    printf(" Автокорреляция\n");
    int new_seq[len];
    for (int i = 0; i <= len; i++) {
        for(int k = 0; k < len; k++) new_seq[k] = seq[k];
        for (int shift = 0; shift < i; shift++) {
            int temp = new_seq[len - 1];
            for (int k = len - 1; k > 0; k--) {
                new_seq[k] = new_seq[k - 1];
            }
            new_seq[0] = temp;
        }
        int count1 = 0, count0 = 0;
        for (int j = 0; j < len; j++) {
            if (seq[j] == new_seq[j]) count1++;
            else count0++;
        }
        float correlation = (1.0 / (31)) * (count1 - count0);
        printf("%-8d |", i);
        for (int j = 0; j < len; j++) {
            printf(" %d |", (seq[j] == new_seq[j]) ? 1 : 0);
        }
        printf(" %15f\n", correlation);
    }
}

int correlation(int *a, int *b, int len) {
    int result = 0;
    for (int i = 0; i < len; i++) {
        result += a[i] * b[i];
    }
    return result;
}

float normalized_correlation(int *a, int *b, int len) {
    int sum_a = 0, sum_b = 0;
    for (int i = 0; i < len; i++) {
        sum_a += a[i] * a[i];
        sum_b += b[i] * b[i];
    }
    return (float)correlation(a, b, len) / sqrt(sum_a * sum_b);
}

void corr_print(int *seq1, int *seq2, int len) {
    printf("\nСдвиг    |");
    for (int i = 0; i < len; i++) {
        printf(" %d |", i + 1);
    }
    printf(" Корреляция | Норм. корреляция\n");
    for (int i = 0; i <= len; i++) {
        int compare[len];
        for (int j = 0; j < len; j++) {
            compare[j] = (seq1[j] == seq2[j]) ? 1 : 0;
        }
        int corr = correlation(seq1, seq2, len);
        float n_corr = normalized_correlation(seq1, seq2, len);
        printf("%-8d |", i);
        for (int j = 0; j < len; j++) {
            printf(" %d |", compare[j]);
        }
        printf(" %8d | %f\n", corr, n_corr);
        
        int temp = seq2[len - 1];
        for (int j = len - 1; j > 0; j--) {
            seq2[j] = seq2[j - 1];
        }
        seq2[0] = temp;
    }
}

int main() {
    int number_st = 10;
    int sequence1[31], sequence2[31];
    gen_gold_seq(number_st, number_st + 7, sequence1);
    printf("Sequence 1: ");
    for (int i = 0; i < 31; i++) {
        printf("%d", sequence1[i]);
    }
    printf("\n");
    int count1 = 0, count0 = 0;
    for (int i = 0; i < 31; i++) {
        if (sequence1[i] == 1) count1++;
        else count0++;
    }
    printf("Count0: %d, Count1: %d\n", count0, count1);
    autocorr(sequence1, 31);
    gen_gold_seq(number_st + 1, (number_st + 7) - 5, sequence2);
    corr_print(sequence1, sequence2, 31);
    return 0;
}