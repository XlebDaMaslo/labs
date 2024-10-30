#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>


// Генерация последовательности Голда
void gen_gold_seq(int num1, int num2, int *sequence) {
    int x[5], y[5];

    // Преобразование чисел в двоичный вид и заполнение массивов
    for (int i = 4; i >= 0; i--) {
        x[i] = num1 % 2;
        y[i] = num2 % 2;
        num1 /= 2;
        num2 /= 2;
    }
    
    int n = 31; //длина последовательности 2^5 - 1

    if (num1 % 2 == 0) { // Четный
        for (int i = 0; i < n; i++) {
            sequence[i] = x[4] ^ y[4];
            int temp_x = x[0] ^ x[2];
            int temp_y = y[0] ^ y[2];
            for(int j=0; j < 4; j++)
            {
                x[j] = x[j+1];
                y[j] = y[j+1];
            }
            x[4] = temp_x;
            y[4] = temp_y;

        }
    } else { // Нечетный
        for (int i = 0; i < n; i++) {
            sequence[i] = x[4] ^ y[4];
            int temp_x = x[0] ^ x[3];
            int temp_y = y[0] ^ y[1];

            for(int j=0; j < 4; j++)
            {
                x[j] = x[j+1];
                y[j] = y[j+1];
            }
            x[4] = temp_x;
            y[4] = temp_y;
        }
    }
}


void autocorr(int *seq, int n) {
    printf("Сдвиг");
    for (int i = 0; i < n; i++) {
        printf(" | %d", i + 1);
    }
    printf(" | Автокорреляция\n");

    int new_seq[n];
    for(int i=0; i < n; i++)
    {
        new_seq[i] = seq[i];
    }

    for (int i = 0; i <= n; i++) {
        int compare[n];
        int count1 = 0;
        int count0 = 0;
        for (int j = 0; j < n; j++) {
            if (seq[j] == new_seq[j]) {
                compare[j] = 1;
                count1++;
            } else {
                compare[j] = 0;
                count0++;
            }
        }
        double correlation = (1.0 / (pow(2, 5) - 1)) * (count1 - count0);

        printf("%-7d", i);
        for (int j=0; j<n; j++){
            printf(" | %d", compare[j]);
        }
        printf(" | %15f\n", correlation);

        // Циклический сдвиг
        int temp = new_seq[n - 1];
        for (int j = n - 1; j > 0; j--) {
            new_seq[j] = new_seq[j - 1];
        }
        new_seq[0] = temp;
    }
}



double correlation(int *a, int *b, int n) {
    double result = 0;
    for (int i = 0; i < n; i++) {
        result += a[i] * b[i];
    }
    return result;
}


double normalized_correlation(int *a, int *b, int n) {
    double sum_a = 0;
    double sum_b = 0;
    for (int i = 0; i < n; i++) {
        sum_a += a[i] * a[i];
        sum_b += b[i] * b[i];
    }
    return correlation(a, b, n) / sqrt(sum_a * sum_b);
}

void corr_print(int *seq1, int *seq2, int n) {

    printf("\nСдвиг");
    for (int i = 0; i < n; i++) {
        printf(" | %d", i + 1);
    }
    printf(" | Корреляция | Норм. корреляция\n");

    
    for (int i = 0; i <= n; i++) {
        int compare[n];

        for (int j=0; j < n; j++){
            if (seq1[j] == seq2[j]){
                compare[j] = 1;
            }
            else{
                compare[j] = 0;
            }
        }

        double corr = correlation(seq1, seq2, n);
        double n_corr = normalized_correlation(seq1, seq2, n);

        printf("%-7d", i);
        for (int j=0; j<n; j++){
            printf(" | %d", compare[j]);
        }
        printf(" | %10.6f | %10.6f\n", corr, n_corr);

        // Циклический сдвиг
        int temp = seq2[n - 1];
        for (int j = n - 1; j > 0; j--) {
            seq2[j] = seq2[j - 1];
        }
        seq2[0] = temp;
    }
}




int main() {
    int number_st = 10;
    int n = 31;
    int sequence1[n];
    int sequence2[n];
    gen_gold_seq(number_st, number_st + 7, sequence1);

    printf("Последовательность 1: ");
    for (int i = 0; i < n; i++) {
        printf("%d", sequence1[i]);
    }
    printf("\n");

    int count1 = 0;
    int count0 = 0;
    for (int i = 0; i < n; i++) {
        if (sequence1[i] == 1) {
            count1++;
        } else {
            count0++;
        }
    }
    printf("Количество нулей: %d, количество единиц: %d\n", count0, count1);

    autocorr(sequence1, n);

    gen_gold_seq(number_st + 1, number_st + 7 - 5, sequence2);
    corr_print(sequence1, sequence2, n);

    return 0;
}