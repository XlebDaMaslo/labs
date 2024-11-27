#include "header.h"

int main() {
    int fd_fifo;
    char buffer[BUFFER_SIZE];
    char filename[BUFFER_SIZE];
    char output_filename[BUFFER_SIZE];
    int fd_out;

    // Открытие FIFO для записи
    if ((fd_fifo = open(FIFO_NAME, O_WRONLY)) == -1) {
        perror("open FIFO");
        exit(1);
    }

    // Ввод имени файла от пользователя
    printf("Enter filename: ");
    scanf("%s", filename);
    sprintf(buffer, "FILENAME~%s", filename);

    // Отправка имени файла серверу
    write(fd_fifo, buffer, strlen(buffer) +1);


    // Чтение имени выходного файла от сервера
    read(fd_fifo, buffer, BUFFER_SIZE);
    sscanf(buffer, "OUTPUT~%s", output_filename);
    printf("Output filename : %s\n", output_filename);
    
    
    if ((fd_out = open(output_filename, O_RDONLY)) == -1) {
        perror("open output file");
        exit(1);
    }
    // Вывод содержимого выходного файла на экран
    while (read(fd_out, buffer, BUFFER_SIZE) > 0) {
        printf("%s", buffer);
    }
    close(fd_out);

    close(fd_fifo);


    printf("Client finished.\n");
    return 0;
}