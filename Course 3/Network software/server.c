#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <time.h>

#define MAX_PACKET_SIZE 1000
#define LOSS_PROBABILITY 0.2 // 20% вероятность потери пакета

unsigned int crc32(const char *data, size_t len) {
    unsigned int crc = 0xFFFFFFFF;
    for (size_t i = 0; i < len; i++) {
        crc ^= (unsigned char)data[i];
        for (int j = 0; j < 8; j++) {
            crc = (crc >> 1) ^ (0xEDB88320 & -(crc & 1));
        }
    }
    return ~crc; // Инвертирование
}

int main() {
    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("Ошибка создания сокета");
        exit(EXIT_FAILURE);
    }

    struct sockaddr_in servaddr;
    memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    servaddr.sin_port = 0; // Автоматический выбор порта

    if (bind(sockfd, (struct sockaddr*)&servaddr, sizeof(servaddr)) < 0) {
        perror("Ошибка привязки сокета");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    socklen_t len = sizeof(servaddr);
    if (getsockname(sockfd, (struct sockaddr*)&servaddr, &len) < 0) {
        perror("Ошибка получения порта");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    printf("Порт сервера: %d\n", ntohs(servaddr.sin_port));

    srand(time(NULL));

    // Буфер (общий)
    FILE *fp = fopen("received_file.txt", "wb");
    if (!fp) {
        perror("Ошибка открытия файла");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    while (1) {
        char buffer[MAX_PACKET_SIZE + 12]; // 4 байта seq_num + 4 байта crc + данные
        struct sockaddr_in cliaddr;
        socklen_t clilen = sizeof(cliaddr);

        int n = recvfrom(sockfd, buffer, sizeof(buffer), 0, (struct sockaddr*)&cliaddr, &clilen);
        if (n < 0) {
            perror("Ошибка приема данных");
            continue;
        }

        // Извлечение заголовка
        int seq_num;
        unsigned int received_crc;
        memcpy(&seq_num, buffer, sizeof(int));
        memcpy(&received_crc, buffer + sizeof(int), sizeof(unsigned int));
        int data_size = n - 8;
        char *data = buffer + 8;

        // Проверка целостности
        unsigned int calculated_crc = crc32(data, data_size);
        if (calculated_crc != received_crc) {
            printf("Пакет %d поврежден, CRC не совпадает\n", seq_num);
            continue;
        }

        // Имитация потери пакета
        if ((double)rand() / RAND_MAX < LOSS_PROBABILITY) {
            printf("Пакет %d потерян\n", seq_num);
            continue;
        }

        // Отправка ACK
        char ack[sizeof(int)];
        memcpy(ack, &seq_num, sizeof(int));
        sendto(sockfd, ack, sizeof(int), 0, (struct sockaddr*)&cliaddr, clilen);
        printf("Отправлен ACK для пакета %d\n", seq_num);

        // Запись данных в файл
        fwrite(data, 1, data_size, fp);
        fwrite("\n", 1, 1, fp); // Перенос строки
    }

    fclose(fp);
    close(sockfd);
    return 0;
}