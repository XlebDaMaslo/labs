#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define FILENAME "Train.dat"
#define MAX_DESTINATION_LENGTH 50


typedef struct {
    char destination[MAX_DESTINATION_LENGTH];
    int train_number;
    time_t departure_time;
} Train;

int main() {
    FILE *file = fopen(FILENAME, "rb");
    if (file == NULL) {
        perror("Ошибка при открытии файла для чтения\n");
        return 1;
    }

    char destination_to_find[MAX_DESTINATION_LENGTH];
    printf("Введите пункт назначения: ");
    scanf("%s", destination_to_find);

    Train train;
    int found = 0;
    while (fread(&train, sizeof(Train), 1, file) == 1) {
        if (strcmp(train.destination, destination_to_find) == 0) {
            printf("Поезд №%d отправляется в %s в %s", train.train_number, train.destination, ctime(&(train.departure_time)));
            found = 1;
        }
    }

    if (!found) {
        printf("Поездов в %s не найдено.\n", destination_to_find);
    }


    fclose(file);

    printf("Автор: Trent Reznor\n");
    printf("Группа: Nine Inch Nails\n");



    return 0;
}