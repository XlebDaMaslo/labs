#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>

// Типы сообщений
#define DHCPDISCOVER 1 // клиент ищет сервер
#define DHCPOFFER 2    // сервер предлагает IP
#define DHCPREQUEST 3  // клиент запрашивает IP
#define DHCPACK 5      // сервер подтверждает выдачу IP

// Структура сообщения
typedef struct dhcp_message {
    uint8_t op;        // Тип сообщения: BOOTREQUEST (1 - запрос от клиента к серверу) или BOOTREPLY (2 - ответ от сервера к клиенту)
    uint8_t htype;     // Тип аппаратного адреса. Для MAC-адреса Ethernet 10 Мбит/с это поле принимает значение 1.
    uint8_t hlen;      // Длина аппаратного адреса. Для MAC-адреса Ethernet — 6.
    uint8_t hops;      // Количество промежуточных маршрутизаторов
    uint32_t xid;      // Уникальный идентификатор транзакции
    uint16_t secs;     // Время в секундах с момента начала процесса получения адреса.
    uint16_t flags;    // Поле для флагов — специальных параметров протокола DHCP.
    uint32_t ciaddr;   // IP-адрес клиента. Заполняется только в том случае, если клиент уже имеет собственный IP-адрес и способен отвечать на запросы ARP (это возможно, если клиент выполняет процедуру обновления адреса по истечении срока аренды).
    uint32_t yiaddr;   // Новый IP-адрес клиента, предложенный сервером.
    uint32_t siaddr;   // IP-адрес сервера. Возвращается в предложении DHCP.
    uint32_t giaddr;   // IP-адрес агента ретрансляции, если таковой участвовал в процессе доставки сообщения DHCP до сервера.
    uint8_t chaddr[16]; // Аппаратный адрес (обычно MAC-адрес) клиента.
    uint8_t sname[64];  // Необязательное имя сервера в виде нуль-терминированной строки.
    uint8_t file[128];  // Необязательное имя файла на сервере, используемое бездисковыми рабочими станциями при удалённой загрузке.
    uint8_t options[312]; // Поле опций DHCP
} dhcp_message_t;

// Инициализация сообщения
void init_dhcp_message(dhcp_message_t *msg) {
    memset(msg, 0, sizeof(dhcp_message_t));
    msg->htype = 1; // Тип аппаратного адреса. Для MAC-адреса Ethernet 10 Мбит/с это поле принимает значение 1.
    msg->hlen = 6;  // Длина аппаратного адреса. Для MAC-адреса Ethernet — 6.
    // Установка "волшебного числа"
    msg->options[0] = 99;
    msg->options[1] = 130;
    msg->options[2] = 83;
    msg->options[3] = 99;
}

// Получение типа сообщения из опций
uint8_t get_message_type(dhcp_message_t *msg) {
    int i = 4; // Начало после "волшебного числа"
    while (i < 312) {
        if (msg->options[i] == 53) { // Проверка кода опции типа сообщения
            return msg->options[i + 2]; // Значение типа сообщения
        }
        i += 2 + msg->options[i + 1]; // Сдвиг указателя на следующее свободное место в options
    }
    return 0;
}

// Установка типа сообщения в опциях
void set_message_type(dhcp_message_t *msg, uint8_t type) {
    int i = 4; // Начало после волшебного числа
    msg->options[i] = 53; // Код опции типа сообщения
    msg->options[i + 1] = 1; // Длина значения опции
    msg->options[i + 2] = type; // Значение типа сообщения
    msg->options[i + 3] = 255; // Конец опций
}

// Установка идентификатора сервера в опциях
void set_server_identifier(dhcp_message_t *msg, uint32_t server_ip) {
    int i = 7; // После опции типа сообщения
    msg->options[i] = 54; // Код опции идентификатора сервера
    msg->options[i + 1] = 4; // Длина значения опции
    memcpy(&msg->options[i + 2], &server_ip, 4); // Копирование данных опции (IP сервера)
    msg->options[i + 6] = 255; // Конец опций
}

int main() {
    int sockfd; // Сокет для обмена данными с клиентами
    struct sockaddr_in server_addr, client_addr; // Структуры для адресов сервера и клиента
    socklen_t client_len = sizeof(client_addr); // Размер структуры адреса клиента
    dhcp_message_t msg; // Структура для приема и отправки DHCP сообщений
    uint32_t server_ip = inet_addr("192.168.1.1"); // IP-адрес сервера. Возвращается в предложении DHCP.
    uint32_t offered_ip = inet_addr("192.168.1.100"); // Новый IP-адрес клиента, предложенный сервером.

    // Создание UDP сокета
    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("Ошибка создания сокета");
        exit(EXIT_FAILURE);
    }

    // Включение широковещательных сообщений
    int broadcast = 1;
    if (setsockopt(sockfd, SOL_SOCKET, SO_BROADCAST, &broadcast, sizeof(broadcast)) < 0) {
        perror("Ошибка настройки сокета");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    // Привязка к порту 67
    memset(&server_addr, 0, sizeof(server_addr)); // Заполнение структуры нулями
    server_addr.sin_family = AF_INET; // IPv4
    server_addr.sin_addr.s_addr = INADDR_ANY; // Прослушивание на всех доступных интерфейсах
    server_addr.sin_port = htons(67); // Порт сервера (67)

    if (bind(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Ошибка привязки сокета к порту");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    printf("DHCP сервер запущен. Ожидание запросов на порту %d\n", 67);

    while (1) {
        // Прием DHCPDISCOVER
        init_dhcp_message(&msg);
        int n = recvfrom(sockfd, &msg, sizeof(dhcp_message_t), 0,
                         (struct sockaddr *)&client_addr, &client_len);
        if (n < 0) {
            perror("Ошибка приема данных");
            continue;
        }

        uint8_t msg_type = get_message_type(&msg);
        printf("Получен тип сообщения: %d\n", msg_type);

        if (msg_type == DHCPDISCOVER) { // Если DHCPDISCOVER
            printf("Получен DHCPDISCOVER от клиента MAC: ");
            for (int i = 0; i < msg.hlen; i++) {
                printf("%02x", msg.chaddr[i]);
                if (i < msg.hlen - 1) printf(":");
            }
            printf("\n");

            // Подготовка DHCPOFFER
            init_dhcp_message(&msg);
            msg.op = 2; // Тип сообщения: BOOTREPLY (2 - ответ от сервера к клиенту)
            msg.htype = 1; // Тип аппаратного адреса. Для MAC-адреса Ethernet 10 Мбит/с это поле принимает значение 1.
            msg.hlen = 6;  // Длина аппаратного адреса. Для MAC-адреса Ethernet — 6.
            msg.xid = msg.xid; // Копирование ID транзакции из запроса
            msg.yiaddr = offered_ip; // Новый IP-адрес клиента, предложенный сервером.
            msg.siaddr = server_ip; // IP-адрес сервера. Возвращается в предложении DHCP.
            memcpy(msg.chaddr, msg.chaddr, 16); // Копирование MAC-адреса клиента
            set_message_type(&msg, DHCPOFFER); // Установка типа сообщения
            set_server_identifier(&msg, server_ip); // Установка идентификатора сервера

            // Отправка DHCPOFFER клиенту
            client_addr.sin_port = htons(68); // Порт клиента (68)
            if (sendto(sockfd, &msg, sizeof(dhcp_message_t), 0,
                       (struct sockaddr *)&client_addr, client_len) < 0) {
                perror("Ошибка отправки DHCPOFFER");
            } else {
                printf("Отправка DHCPOFFER клиенту IP: %s\n", inet_ntoa(*(struct in_addr *)&offered_ip));
            }
        } else if (msg_type == DHCPREQUEST) { // Если DHCPREQUEST
            printf("Получен DHCPREQUEST от клиента MAC: ");
            for (int i = 0; i < msg.hlen; i++) {
                printf("%02x", msg.chaddr[i]);
                if (i < msg.hlen - 1) printf(":");
            }
            printf("\n");

            // Подготовка DHCPACK
            init_dhcp_message(&msg);
            msg.op = 2; // Тип сообщения: BOOTREPLY (2 - ответ от сервера к клиенту)
            msg.htype = 1; // Тип аппаратного адреса. Для MAC-адреса Ethernet 10 Мбит/с это поле принимает значение 1.
            msg.hlen = 6;  // Длина аппаратного адреса. Для MAC-адреса Ethernet — 6.
            msg.xid = msg.xid; // Копирование ID транзакции из запроса
            msg.yiaddr = offered_ip; // IP-адрес тот же, что и в DHCPOFFER
            msg.siaddr = server_ip; // IP-адрес сервера. Возвращается в предложении DHCP.
            memcpy(msg.chaddr, msg.chaddr, 16); // Копирование MAC-адреса клиента
            set_message_type(&msg, DHCPACK); // Установка типа сообщения
            set_server_identifier(&msg, server_ip); // Установка идентификатора сервера

            // Отправка DHCPACK клиенту
            client_addr.sin_port = htons(68); // Порт клиента (68)
            if (sendto(sockfd, &msg, sizeof(dhcp_message_t), 0,
                       (struct sockaddr *)&client_addr, client_len) < 0) {
                perror("Ошибка отправки DHCPACK");
            } else {
                printf("Отправка DHCPACK клиенту IP: %s\n", inet_ntoa(*(struct in_addr *)&offered_ip));
            }
        }
    }

    close(sockfd); // Закрытие сокета
    return 0;
}