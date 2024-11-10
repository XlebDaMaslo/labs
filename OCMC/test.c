#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

double correlation(int a[], int b[], int N) {
    double result = 0;
    for (int i = 0; i < N; i++) {
        result += a[i] * b[i];
    }
    return result;
}

double normalized_correlation(int a[], int b[], int N) {
    double sum_a = 0, sum_b = 0;
    for (int i = 0; i < N; i++) {
        sum_a += a[i] * a[i];
        sum_b += b[i] * b[i];
    }
    return correlation(a, b, N) / sqrt(sum_a * sum_b);
}

double sampleNormal() {
    double u, v, r, c;
    do {
        u = ((double) rand() / (RAND_MAX)) * 2.0 - 1.0;
        v = ((double) rand() / (RAND_MAX)) * 2.0 - 1.0;
        r = u * u + v * v;
    } while (r == 0 || r > 1);
    
    c = sqrt(-2.0 * log(r) / r);
    return u * c;
}

int main() {
    srand(time(0));

    int n = 10;
    double a[n], b[n], a_shifted[n], b_shifted[n], a_corr[n], b_corr[n];
    
    for (int i = 0; i < n; i++) {
        a[i] = sampleNormal();
    }
    for (int i = 0; i < n; i++) {
        b[i] = sampleNormal();
    }
    
    for (int j = 0; j < n; j++){
        for (int i = 0; i < n; i++){
            if (i == n-1){
                a_shifted[i] = a[0];
                b_shifted[i] = b[0];
            }
            else{
                a_shifted[i] = a[i+1];
                b_shifted[i] = b[i+1];
            }
        }

        a_corr[j] = normalized_correlation(a, a_shifted, n);
        b_corr[j] = normalized_correlation(b, b_shifted, n);

    }

    return 0;
}
