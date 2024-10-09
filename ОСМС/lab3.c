#include <stdio.h>
#include <math.h>

float correlation(float arr1[], float arr2[], int n) {
    float sum = 0;
    for (int i = 0; i < n; i++) {
        sum += arr1[i] * arr2[i];
    }
    return sum;
}

float normalized_correlation(float arr1[], float arr2[], int n) {
    float sum_xy = 0, sum_x = 0, sum_y = 0, sum_x2 = 0, sum_y2 = 0;

    for (int i = 0; i < n; i++) {
        sum_xy += arr1[i] * arr2[i];
        sum_x += arr1[i];
        sum_y += arr2[i];
        sum_x2 += arr1[i] * arr1[i];
        sum_y2 += arr2[i] * arr2[i];
    }
  
   return sum_xy / (sqrt(sum_x2) * sqrt(sum_y2));
}


int main() {
    float a[] = {6, 2, 3, -2, -4, -4, 1, 1};
    float b[] = {3, 1, 5, 0, -3, -4, 2, 3};
    float c[] = {-1, -1, 3, -9, 2, -8, 4, -4};
    int n = sizeof(a) / sizeof(a[0]);

    printf("Корреляция:\n");
    printf("a и b: %f\n", correlation(a, b, n));
    printf("a и c: %f\n", correlation(a, c, n));
    printf("b и c: %f\n", correlation(b, c, n));

    printf("\nНормализованная корреляция:\n");
    printf("a и b: %f\n", normalized_correlation(a, b, n));
    printf("a и c: %f\n", normalized_correlation(a, c, n));
    printf("b и c: %f\n", normalized_correlation(b, c, n));

    return 0;
}