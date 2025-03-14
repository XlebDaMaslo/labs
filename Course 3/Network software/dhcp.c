#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>

// Типы сообщений
#define DHCPDISCOVER 1 // Клиент ищет сервер
#define DHCPOFFER 2    // Сервер предлагает IP
#define DHCPREQUEST 3  // Клиент запрашивает IP
#define DHCPACK 5      // Сервер подтверждает выдачу IP

#define DHCPDECLINE  4  // Клиент отказывается от предложенного IP
#define DHCPNAK      6  // Сервер отклоняет запрос клиента
#define DHCPRELEASE  7  // Клиент освобождает IP
#define DHCPINFORM   8  // Клиент запрашивает информацию

// Структура пула IP-адресов
typedef struct ip_pool {
    uint32_t ip;        // IP-адрес в сетевом порядке
    int is_assigned;    // 1 - занят, 0 - свободен
    uint8_t chaddr[16]; // MAC-адрес клиента
} ip_pool_t;

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

// Пул IP-адресов (3 адреса для примера)
ip_pool_t ip_pool[] = {
    { .ip = 0, .is_assigned = 0, .chaddr = {0} },
    { .ip = 0, .is_assigned = 0, .chaddr = {0} },
    { .ip = 0, .is_assigned = 0, .chaddr = {0} }
};
const int pool_size = sizeof(ip_pool) / sizeof(ip_pool[0]);

// Подготовка пула IP
void init_ip_pool() {
    ip_pool[0].ip = inet_addr("192.168.1.100");
    ip_pool[1].ip = inet_addr("192.168.1.101");
    ip_pool[2].ip = inet_addr("192.168.1.102");
}

// Поиск свободного IP
uint32_t get_free_ip() {
    for (int i = 0; i < pool_size; i++) {
        if (!ip_pool[i].is_assigned) {
            return ip_pool[i].ip;
        }
    }
    return 0; // Нет свободных адресов
}

// Проверка доступности IP
int is_ip_available(uint32_t ip) {
    for (int i = 0; i < pool_size; i++) {
        if (ip_pool[i].ip == ip && !ip_pool[i].is_assigned) {
            return 1;
        }
    }
    return 0;
}

// Выделение IP клиенту
void assign_ip(uint32_t ip, uint8_t *chaddr) {
    for (int i = 0; i < pool_size; i++) {
        if (ip_pool[i].ip == ip) {
            ip_pool[i].is_assigned = 1;
            memcpy(ip_pool[i].chaddr, chaddr, 16);
            break;
        }
    }
}

// Освобождение IP
void release_ip(uint32_t ip) {
    for (int i = 0; i < pool_size; i++) {
        if (ip_pool[i].ip == ip) {
            ip_pool[i].is_assigned = 0;
            memset(ip_pool[i].chaddr, 0, 16);
            break;
        }
    }
}

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

// Добавление стандартных опций DHCP
void add_dhcp_options(dhcp_message_t *msg) {
    int i = 11;
    // Маска подсети
    msg->options[i] = 1;
    msg->options[i + 1] = 4;
    uint32_t subnet_mask = inet_addr("255.255.255.0");
    memcpy(&msg->options[i + 2], &subnet_mask, 4);
    i += 6;
    // Маршрутизатор
    msg->options[i] = 3;
    msg->options[i + 1] = 4;
    uint32_t router = inet_addr("192.168.1.1");
    memcpy(&msg->options[i + 2], &router, 4);
    i += 6;
    // DNS-сервер
    msg->options[i] = 6;
    msg->options[i + 1] = 4;
    uint32_t dns = inet_addr("8.8.8.8");
    memcpy(&msg->options[i + 2], &dns, 4);
    i += 6;
    // Время аренды (24 часа)
    msg->options[i] = 51;
    msg->options[i + 1] = 4;
    uint32_t lease_time = htonl(86400);
    memcpy(&msg->options[i + 2], &lease_time, 4);
    i += 6;
    msg->options[i] = 255; // Конец опций
}

int main() {
    int sockfd; // Сокет для обмена данными с клиентами
    struct sockaddr_in server_addr, client_addr; // Структуры для адресов сервера и клиента
    socklen_t client_len = sizeof(client_addr); // Размер структуры адреса клиента
    dhcp_message_t msg; // Структура для приема и отправки DHCP сообщений
    uint32_t server_ip = inet_addr("192.168.1.1"); // IP-адрес сервера. Возвращается в предложении DHCP.

    // Инициализация пула IP
    init_ip_pool();

    // Создание сокета
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

    // Привязка сокета
    if (bind(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Ошибка привязки сокета к порту");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    printf("DHCP сервер запущен. Ожидание запросов на порту %d\n", 67);

    // Основной цикл обработки сообщений
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

        switch (msg_type) {
            case DHCPDISCOVER: {
                uint32_t offered_ip = get_free_ip();
                if (offered_ip == 0) {
                    printf("Нет свободных IP-адресов\n");
                    break;
                }
                init_dhcp_message(&msg);
                msg.op = 2; // Тип сообщения: BOOTREPLY (2 - ответ от сервера к клиенту)
                msg.xid = msg.xid; // Копирование ID транзакции из запроса
                msg.yiaddr = offered_ip; // Новый IP-адрес клиента, предложенный сервером.
                msg.siaddr = server_ip; // IP-адрес сервера. Возвращается в предложении DHCP.
                memcpy(msg.chaddr, msg.chaddr, 16); // Копирование MAC-адреса клиента
                set_message_type(&msg, DHCPOFFER); // Установка типа сообщения
                set_server_identifier(&msg, server_ip); // Установка идентификатора сервера
                add_dhcp_options(&msg);
                client_addr.sin_port = htons(68);
                sendto(sockfd, &msg, sizeof(dhcp_message_t), 0,
                       (struct sockaddr *)&client_addr, client_len);
                printf("Отправлен DHCPOFFER для IP: %s\n", inet_ntoa(*(struct in_addr *)&offered_ip));
                break;
            }
            case DHCPREQUEST: {
                uint32_t requested_ip = msg.yiaddr; // Упрощение: берем из yiaddr
                if (is_ip_available(requested_ip)) {
                    init_dhcp_message(&msg);
                    msg.op = 2; // Тип сообщения: BOOTREPLY (2 - ответ от сервера к клиенту)
                    msg.xid = msg.xid; // Копирование ID транзакции из запроса
                    msg.yiaddr = requested_ip; // IP-адрес клиента, предложенный сервером.
                    msg.siaddr = server_ip; // IP-адрес сервера. Возвращается в предложении DHCP.
                    memcpy(msg.chaddr, msg.chaddr, 16); // Копирование MAC-адреса клиента
                    set_message_type(&msg, DHCPACK); // Установка типа сообщения
                    set_server_identifier(&msg, server_ip); // Установка идентификатора сервера
                    add_dhcp_options(&msg);
                    assign_ip(requested_ip, msg.chaddr);
                    client_addr.sin_port = htons(68); // Порт клиента (68)
                    sendto(sockfd, &msg, sizeof(dhcp_message_t), 0,
                           (struct sockaddr *)&client_addr, client_len);
                    printf("Отправлен DHCPACK для IP: %s\n", inet_ntoa(*(struct in_addr *)&requested_ip));
                } else {
                    init_dhcp_message(&msg);
                    msg.op = 2;
                    msg.xid = msg.xid;
                    memcpy(msg.chaddr, msg.chaddr, 16);
                    set_message_type(&msg, DHCPNAK);
                    set_server_identifier(&msg, server_ip);
                    client_addr.sin_port = htons(68);
                    sendto(sockfd, &msg, sizeof(dhcp_message_t), 0,
                           (struct sockaddr *)&client_addr, client_len);
                    printf("Отправлен DHCPNAK для IP: %s\n", inet_ntoa(*(struct in_addr *)&requested_ip));
                }
                break;
            }
            case DHCPDECLINE: {
                uint32_t declined_ip = msg.yiaddr; // Упрощение: из yiaddr
                uint8_t dummy_chaddr[16] = {0};
                assign_ip(declined_ip, dummy_chaddr);
                printf("IP %s отмечен как отклоненный\n", inet_ntoa(*(struct in_addr *)&declined_ip));
                break;
            }
            case DHCPRELEASE: {
                uint32_t released_ip = msg.ciaddr;
                release_ip(released_ip);
                printf("IP %s освобожден\n", inet_ntoa(*(struct in_addr *)&released_ip));
                break;
            }
            case DHCPINFORM: {
                init_dhcp_message(&msg);
                msg.op = 2;
                msg.xid = msg.xid;
                msg.yiaddr = 0; // Без выделения IP
                msg.siaddr = server_ip;
                memcpy(msg.chaddr, msg.chaddr, 16);
                set_message_type(&msg, DHCPACK);
                set_server_identifier(&msg, server_ip);
                add_dhcp_options(&msg);
                client_addr.sin_port = htons(68);
                sendto(sockfd, &msg, sizeof(dhcp_message_t), 0,
                       (struct sockaddr *)&client_addr, client_len);
                printf("Отправлен DHCPACK для DHCPINFORM\n");
                break;
            }
            default:
                printf("Неподдерживаемый тип сообщения: %d\n", msg_type);
                break;
        }
    }

    close(sockfd);
    return 0;
}