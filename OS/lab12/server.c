#include "header.h"

int main() {
    int fd_fifo, fd_in, fd_out;
    char buffer[BUFFER_SIZE];
    char filename[BUFFER_SIZE];
    char output_filename[BUFFER_SIZE] = "output.dat"; // Имя выходного файла

    // Создание FIFO
    if (mknod(FIFO_NAME, S_IFIFO | 0666, 0) == -1) {
        perror("mknod");
        exit(1);
    }

    // Открытие FIFO для чтения
    if ((fd_fifo = open(FIFO_NAME, O_RDONLY)) == -1) {
        perror("open FIFO");
        exit(1);
    }

    // Чтение имени файла из FIFO
    read(fd_fifo, buffer, BUFFER_SIZE);
    sscanf(buffer, "FILENAME~%s", filename); // Извлечение имени файла
    printf("Received filename: %s\n", filename);

    // Открытие входного файла
    if ((fd_in = open(filename, O_RDONLY)) == -1) {
        perror("open input file");
        exit(1);
    }

     // Открытие выходного файла
    if ((fd_out = open(output_filename, O_WRONLY | O_CREAT | O_TRUNC, 0644)) == -1) {
        perror("open output file");
        exit(1);
    }

    // Копирование данных из входного файла в выходной 
     while (read(fd_in, buffer, BUFFER_SIZE) > 0) {
        write(fd_out, buffer, strlen(buffer));
    }

    close(fd_in);
    close(fd_out);

    // Отправка имени выходного файла клиенту
    sprintf(buffer, "OUTPUT~%s", output_filename);
    write(fd_fifo, buffer, strlen(buffer));

    close(fd_fifo);
    unlink(FIFO_NAME);

    printf("Server finished.\n");
    return 0;
}