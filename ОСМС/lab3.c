#include <stdio.h>
#include <math.h>

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

int main() {
    int a[] = {6, 2, 3, -2, -4, -4, 1, 1};
    int b[] = {3, 1, 5, 0, -3, -4, 2, 3};
    int c[] = {-1, -1, 3, -9, 2, -8, 4, -4};
    int N = sizeof(a) / sizeof(a[0]);

    double corr_ab = correlation(a, b, N);
    double corr_ac = correlation(a, c, N);
    double corr_bc = correlation(b, c, N);
    
    printf("Корреляция между a, b и c:\n");
    printf("   |   a   |   b   |   c  \n");
    printf("a  |   -   | %.2f | %.2f \n", corr_ab, corr_ac);
    printf("b  | %.2f |   -   | %.2f \n", corr_ab, corr_bc);
    printf("c  | %.2f | %.2f |  -  \n\n", corr_ac, corr_bc);

    double norm_corr_ab = normalized_correlation(a, b, N);
    double norm_corr_ac = normalized_correlation(a, c, N);
    double norm_corr_bc = normalized_correlation(b, c, N);

    printf("Нормализованная корреляция между a, b и c:\n");
    printf("   |  a   |  b   |  c  \n");
    printf("a  |  -   | %.2f | %.2f \n", norm_corr_ab, norm_corr_ac);
    printf("b  | %.2f |  -   | %.2f \n", norm_corr_ab, norm_corr_bc);
    printf("c  | %.2f | %.2f |  -  \n", norm_corr_ac, norm_corr_bc);

    return 0;
}
