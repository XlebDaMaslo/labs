// Клиент
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include "header.h"

int main(void) {
    int fd;
    char message[MAX_BUFF];

    // Запрос имени файла у пользователя
    printf("Введите имя файла: ");
    scanf("%s", message);

    // Формирование строки
    snprintf(message, sizeof(message), "FILENAME~%s", message);

    // Открытие FIFO для записи
    if ((fd = open(FIFO_NAME, O_WRONLY)) < 0) {
        perror("Невозможно открыть FIFO");
        exit(1);
    }

    // Отправка сообщения серверу
    write(fd, message, sizeof(message));

    // Закрытие канала
    close(fd);
    return 0;
}
