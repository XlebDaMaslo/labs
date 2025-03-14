#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/time.h>

#define MAX_PACKET_SIZE 1000
#define TIMEOUT_SEC 5

// Простая функция CRC32 (должна совпадать с серверной)
unsigned int crc32(const char *data, size_t len) {
    unsigned int crc = 0xFFFFFFFF;
    for (size_t i = 0; i < len; i++) {
        crc ^= (unsigned char)data[i];
        for (int j = 0; j < 8; j++) {
            crc = (crc >> 1) ^ (0xEDB88320 & -(crc & 1));
        }
    }
    return ~crc;
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        fprintf(stderr, "Использование: %s <server_ip> <server_port> <file_path>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    char *server_ip = argv[1];
    int server_port = atoi(argv[2]);
    char *file_path = argv[3];

    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("Ошибка создания сокета");
        exit(EXIT_FAILURE);
    }

    struct sockaddr_in servaddr;
    memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(server_port);
    if (inet_pton(AF_INET, server_ip, &servaddr.sin_addr) <= 0) {
        perror("Ошибка преобразования IP-адреса");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    // Чтение файла
    FILE *fp = fopen(file_path, "rb");
    if (!fp) {
        perror("Ошибка открытия файла");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    fseek(fp, 0, SEEK_END);
    long file_size = ftell(fp);
    fseek(fp, 0, SEEK_SET);

    int num_packets = (file_size + MAX_PACKET_SIZE - 1) / MAX_PACKET_SIZE;
    char buffer[MAX_PACKET_SIZE + 12]; // 4 байта seq_num + 4 байта crc + данные

    for (int seq_num = 0; seq_num < num_packets; seq_num++) {
        int data_size = fread(buffer + 8, 1, MAX_PACKET_SIZE, fp);
        memcpy(buffer, &seq_num, sizeof(int));
        unsigned int crc = crc32(buffer + 8, data_size);
        memcpy(buffer + 4, &crc, sizeof(unsigned int));

        while (1) {
            sendto(sockfd, buffer, 8 + data_size, 0, (struct sockaddr*)&servaddr, sizeof(servaddr));

            struct timeval tv;
            tv.tv_sec = TIMEOUT_SEC;
            tv.tv_usec = 0;
            setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));

            char ack[sizeof(int)];
            int n = recvfrom(sockfd, ack, sizeof(int), 0, NULL, NULL);
            if (n > 0) {
                int ack_seq;
                memcpy(&ack_seq, ack, sizeof(int));
                if (ack_seq == seq_num) {
                    printf("Получен ACK для пакета %d\n", seq_num);
                    break;
                }
            } else {
                printf("Таймаут для пакета %d, повторная отправка...\n", seq_num);
            }
        }
    }

    printf("Передача файла завершена\n");
    fclose(fp);
    close(sockfd);
    return 0;
}