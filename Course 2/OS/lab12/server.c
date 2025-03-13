// Сервер
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include "header.h"

int main(void) {
    int fd;
    char buffer[MAX_BUFF];

    // Создание FIFO
    if (mknod(FIFO_NAME, S_IFIFO | 0666, 0) < 0) {
        perror("Невозможно создать FIFO");
        exit(1);
    }

    // Открытие FIFO для чтения
    if ((fd = open(FIFO_NAME, O_RDONLY)) < 0) {
        perror("Невозможно открыть FIFO");
        exit(1);
    }

    // Чтение сообщения от клиента
    read(fd, buffer, MAX_BUFF);
    printf("Получено сообщение: %s\n", buffer);

    close(fd);
    unlink(FIFO_NAME);
    return 0;
}
