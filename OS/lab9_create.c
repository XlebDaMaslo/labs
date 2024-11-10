#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define FILENAME "Train.dat"
#define MAX_DESTINATION_LENGTH 50

// Структура для записи в файл
typedef struct {
    char destination[MAX_DESTINATION_LENGTH];
    int train_number;
    time_t departure_time; 
} Train;

int main() {
    FILE *file = fopen(FILENAME, "wb");
    if (file == NULL) {
        perror("Ошибка при открытии файла для записи");
        return 1;
    }

    Train trains[] = {
        {"Москва", 123, time(NULL) + 3600}, // Через час
        {"Санкт-Петербург", 456, time(NULL) + 7200}, // Через 2 часа
        {"Новосибирск", 789, time(NULL) + 10800}, // Через 3 часа
        {"Екатеринбург", 101, time(NULL) + 14400}, // Через 4 часа
        {"Казань", 112, time(NULL) + 18000}, // Через 5 часов
        {"Нижний Новгород", 223, time(NULL) + 21600}, // Через 6 часов
        {"Самара", 334, time(NULL) + 25200}, // Через 7 часов
        {"Сочи", 445, time(NULL) + 28800} // Через 8 часов

    };


    size_t num_trains = sizeof(trains) / sizeof(trains[0]);
    if (fwrite(trains, sizeof(Train), num_trains, file) != num_trains) {
        perror("Ошибка при записи в файл");
        fclose(file);
        return 1;
    }

    fclose(file);
    printf("Файл %s успешно создан.\n", FILENAME);

    printf("Автор: Trent Reznor\n");
    printf("Группа: Nine Inch Nails\n");


    return 0;
}