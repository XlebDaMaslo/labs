#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/wait.h>

#define BUF_SIZE 1024
#define END_OF_TRANSMISSION 26  // Код завершения передачи

// Функция для изменения слов — меняет местами первую и последнюю буквы
void swap_letters(char *word) {
    int len = strlen(word);
    if (len > 1) {
        char temp = word[0];
        word[0] = word[len - 1];
        word[len - 1] = temp;
    }
}

// Функция для обработки текста: меняет буквы в словах
void process_text(char *text, FILE *output_file) {
    char *token = strtok(text, " \t");
    while (token != NULL) {
        swap_letters(token);
        fprintf(output_file, "%s ", token);
        token = strtok(NULL, " \n\t");
    }
    fprintf(output_file, "\n");
}

int main(int argc, char *argv[]) {
    int pipe_fd[2];
    pid_t pid;
    char buffer[BUF_SIZE];
    int file_fd;

    if (argc != 3) {
        fprintf(stderr, "Usage: %s <input_file> <output_file>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    // Открытие входного файла для чтения
    file_fd = open(argv[1], O_RDONLY);
    if (file_fd == -1) {
        perror("Error opening input file");
        exit(EXIT_FAILURE);
    }

    // Создание канала
    if (pipe(pipe_fd) == -1) {
        perror("Error creating pipe");
        exit(EXIT_FAILURE);
    }

    // Создание дочернего процесса
    pid = fork();
    if (pid == -1) {
        perror("Error forking");
        exit(EXIT_FAILURE);
    }

    if (pid == 0) {  // Дочерний процесс
        close(pipe_fd[1]);  // Закрытие записи в канале

        // Открытие выходного файла для записи
        FILE *output_file = fopen(argv[2], "w");
        if (output_file == NULL) {
            perror("Error opening output file");
            exit(EXIT_FAILURE);
        }

        // Чтение из канала и обработка данных
        ssize_t num_read;
        while ((num_read = read(pipe_fd[0], buffer, BUF_SIZE)) > 0) {
            if (buffer[num_read - 1] == END_OF_TRANSMISSION) {
                buffer[num_read - 1] = '\0';  // Убираем символ завершения передачи
                process_text(buffer, output_file);
                break;
            }
            buffer[num_read] = '\0';
            process_text(buffer, output_file);
        }

        fclose(output_file);
        close(pipe_fd[0]);  // Закрытие чтения в канале
        exit(EXIT_SUCCESS);

    } else {  // Родительский процесс
        close(pipe_fd[0]);  // Закрытие чтения в канале

        // Чтение данных из файла и отправка их через канал
        ssize_t num_read;
        while ((num_read = read(file_fd, buffer, BUF_SIZE - 1)) > 0) {
            buffer[num_read] = '\0';
            write(pipe_fd[1], buffer, num_read);
        }

        // Отправка символа завершения передачи
        char end_signal = END_OF_TRANSMISSION;
        write(pipe_fd[1], &end_signal, 1);

        close(file_fd);
        close(pipe_fd[1]);  // Закрытие записи в канале

        // Ожидание завершения дочернего процесса
        wait(NULL);
    }

    return 0;
}
