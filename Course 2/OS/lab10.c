#include "./lab10.h"

extern char **environ;

int main(int argc, char **argv) {
    int c;
    int env_opt = 0; // Флаг для выбора способа вывода переменных окружения
    int file_opt = 0; // Флаг для указания файла
    char *filename = NULL;
    int fd;

    // Обработка опций командной строки
    while ((c = getopt(argc, argv, "12f:")) != -1) {
        switch (c) {
            case '1':
                if(env_opt) {
                    fprintf(stderr, "Опции -1 и -2 взаимоисключающие.\n");
                    exit(1);
                }
                env_opt = 1;
                break;
            case '2':
                if(env_opt) {
                    fprintf(stderr, "Опции -1 и -2 взаимоисключающие.\n");
                    exit(1);
                }
                 env_opt = 2;
                break;
            case 'f':
                file_opt = 1;
                filename = optarg;
                break;
            case '?':
                fprintf(stderr, "Неизвестная опция или отсутствует аргумент.\n");
                exit(1);
            default:
                abort();
        }
    }

    // Вывод переменных окружения
    if (env_opt == 1) {
        for (int i = 0; i < 10 && environ[i] != NULL; i++) {
            printf("%s\n", environ[i]);
        }
    } else if (env_opt == 2) {
        for (char **env = environ; *env != NULL && env - environ < 10 ; env++) {
            printf("%s\n", *env);
        }
    }

    // Обработка файла
    if (file_opt) {
        if ((fd = open(filename, O_RDONLY)) == -1) {
            perror("Ошибка открытия файла");
            exit(1);
        }

        char buffer[1024];
        ssize_t bytes_read;

        while ((bytes_read = read(fd, buffer, sizeof(buffer))) > 0) {
            if (write(STDOUT_FILENO, buffer, bytes_read) == -1) {
                perror("Ошибка записи");
                exit(1);
            }
        }

        if (bytes_read == -1) {
            perror("Ошибка чтения файла");
            exit(1);
        }
        if (close(fd) == -1) {
            perror("Ошибка закрытия файла");
            exit(1);
        }

    }

    // Вывод информации об авторе
    printf("Автор: Trent Reznor\n");
    printf("Группа: Nine Inch Nails\n");

    return 0;
}