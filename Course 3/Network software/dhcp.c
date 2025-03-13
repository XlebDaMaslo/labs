#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define DHCP_SERVER_PORT 67 // Порт DHCP сервера
#define DHCP_CLIENT_PORT 68 // Порт DHCP клиента
#define DHCP_MAGIC_COOKIE 0x63825363 // "Волшебное число" DHCP
#define MAX_DHCP_MSG_SIZE 576 // Максимальный размер DHCP сообщения

#define DHCPDISCOVER  1 // клиент ищет сервер
#define DHCPOFFER     2 // сервер предлагает IP
#define DHCPREQUEST   3 // клиент запрашивает IP
#define DHCPACK       5 // сервер подтверждает выдачу IP

#define DHCP_MESSAGE_TYPE 53 // Тип DHCP сообщения
#define DHCP_SERVER_IDENTIFIER 54 // Идентификатор DHCP сервера
#define DHCP_SUBNET_MASK 1 // Маска подсети
#define DHCP_ROUTER 3 // IP адрес маршрутизатора по умолчанию
#define DHCP_DNS_SERVERS 6 // Адреса DNS серверов
#define DHCP_LEASE_TIME 51 // Время аренды IP адреса

typedef struct dhcp_message {
    uint8_t op;                 // Тип сообщения: BOOTREQUEST (1 - запрос от клиента к серверу) или BOOTREPLY (2 - ответ от сервера к клиенту)
    uint8_t htype;              // Тип аппаратного адреса. для MAC-адреса Ethernet 10 Мбит/с это поле принимает значение 1.
    uint8_t hlen;               // Длина аппаратного адреса. Для MAC-адреса Ethernet — 6.
    uint8_t hops;               // Количество промежуточных маршрутизаторов
    uint32_t xid;              // Уникальный идентификатор транзакции
    uint16_t secs;             // Время в секундах с момента начала процесса получения адреса.
    uint16_t flags;            // Поле для флагов — специальных параметров протокола DHCP.
    struct in_addr ciaddr;      // IP-адрес клиента. Заполняется только в том случае, если клиент уже имеет собственный IP-адрес и способен отвечать на запросы ARP (это возможно, если клиент выполняет процедуру обновления адреса по истечении срока аренды).
    struct in_addr yiaddr;      // Новый IP-адрес клиента, предложенный сервером.
    struct in_addr siaddr;      // IP-адрес сервера. Возвращается в предложении DHCP.
    struct in_addr giaddr;      // IP-адрес агента ретрансляции, если таковой участвовал в процессе доставки сообщения DHCP до сервера.
    uint8_t chaddr[16];         // Аппаратный адрес (обычно MAC-адрес) клиента.
    uint8_t sname[64];          // Необязательное имя сервера в виде нуль-терминированной строки.
    uint8_t file[128];          // Необязательное имя файла на сервере, используемое бездисковыми рабочими станциями при удалённой загрузке.
    uint32_t magic_cookie;     // Волшебное число
    uint8_t options[300];       // Поле опций DHCP
} dhcp_message_t;

void add_dhcp_option(uint8_t *options, uint8_t option_code, uint8_t option_len, const void *option_data, int *option_index) {
    options[(*option_index)++] = option_code; // Код опции
    options[(*option_index)++] = option_len;  // Длина значения опции
    memcpy(&options[*option_index], option_data, option_len); // Копирование данных опции
    *option_index += option_len; // Сдвиг указателя на следующее свободное место в options
}

int main() {
    int sockfd; // Сокет для обмена данными с клиентами
    struct sockaddr_in server_addr, client_addr; // Структуры для адресов сервера и клиента
    socklen_t client_addr_len = sizeof(client_addr); // Размер структуры адреса клиента
    dhcp_message_t dhcp_recv_msg, dhcp_send_msg; // Структуры для приема и отправки DHCP сообщений

    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) == -1) {
        perror("Ошибка создания сокета");
        exit(EXIT_FAILURE);
    }

    memset(&server_addr, 0, sizeof(server_addr)); // Заполнение структуры нулями
    server_addr.sin_family = AF_INET; // Семейство адресов IPv4
    server_addr.sin_port = htons(DHCP_SERVER_PORT); // Порт сервера (67)
    server_addr.sin_addr.s_addr = INADDR_ANY; // Прослушивание на всех доступных интерфейсах

    if (bind(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) == -1) {
        perror("Ошибка привязки сокета к порту");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    printf("DHCP Сервер запущен. Ожидание запросов на порту %d\n", DHCP_SERVER_PORT);

    while (1) {
        // Прием DHCPDISCOVER
        memset(&dhcp_recv_msg, 0, sizeof(dhcp_recv_msg));
        if (recvfrom(sockfd, &dhcp_recv_msg, sizeof(dhcp_recv_msg), 0, (struct sockaddr *)&client_addr, &client_addr_len) == -1) {
            perror("Ошибка приема данных");
            continue;
        }

        if (dhcp_recv_msg.op == DHCPDISCOVER) { // Если DHCPDISCOVER
            printf("Получен DHCPDISCOVER от клиента MAC: %02x:%02x:%02x:%02x:%02x:%02x\n",
                   dhcp_recv_msg.chaddr[0], dhcp_recv_msg.chaddr[1], dhcp_recv_msg.chaddr[2],
                   dhcp_recv_msg.chaddr[3], dhcp_recv_msg.chaddr[4], dhcp_recv_msg.chaddr[5]);

            // Подготовка DHCPOFFER
            memset(&dhcp_send_msg, 0, sizeof(dhcp_send_msg));
            dhcp_send_msg.op = DHCPOFFER;
            dhcp_send_msg.htype = 1;
            dhcp_send_msg.hlen = 6;
            dhcp_send_msg.xid = dhcp_recv_msg.xid;
            memcpy(dhcp_send_msg.chaddr, dhcp_recv_msg.chaddr, 6);
            dhcp_send_msg.magic_cookie = htonl(DHCP_MAGIC_COOKIE);

            // Пример предложения IP-адреса (##########)
            inet_pton(AF_INET, "192.168.1.101", &dhcp_send_msg.yiaddr);
            inet_pton(AF_INET, "192.168.1.100", &dhcp_send_msg.siaddr);

            int option_index = 0;
            uint8_t dhcp_msg_type = DHCPOFFER;
            add_dhcp_option(dhcp_send_msg.options, DHCP_MESSAGE_TYPE, 1, &dhcp_msg_type, &option_index);

            struct in_addr subnet_mask_addr; // Структура для маски подсети
            inet_pton(AF_INET, "255.255.255.0", &subnet_mask_addr);
            add_dhcp_option(dhcp_send_msg.options, DHCP_SUBNET_MASK, 4, &subnet_mask_addr, &option_index);

            struct in_addr router_addr; // Структура для адреса маршрутизатора
            inet_pton(AF_INET, "192.168.1.1", &router_addr);
            add_dhcp_option(dhcp_send_msg.options, DHCP_ROUTER, 4, &router_addr, &option_index);

            struct in_addr dns_addr; // Структура для адреса DNS сервера
            inet_pton(AF_INET, "8.8.8.8", &dns_addr);
            add_dhcp_option(dhcp_send_msg.options, DHCP_DNS_SERVERS, 4, &dns_addr, &option_index);

            uint32_t lease_time = htonl(86400); // 1 день
            add_dhcp_option(dhcp_send_msg.options, DHCP_LEASE_TIME, 4, &lease_time, &option_index);


            printf("Отправка DHCPOFFER клиенту IP: %s\n", inet_ntoa(dhcp_send_msg.yiaddr));

            sendto(sockfd, &dhcp_send_msg, sizeof(dhcp_send_msg), 0, (struct sockaddr *)&client_addr, client_addr_len);


        } else if (dhcp_recv_msg.op == DHCPREQUEST) { // Если DHCPREQUEST
            printf("Получен DHCPREQUEST от клиента MAC: %02x:%02x:%02x:%02x:%02x:%02x\n",
                   dhcp_recv_msg.chaddr[0], dhcp_recv_msg.chaddr[1], dhcp_recv_msg.chaddr[2],
                   dhcp_recv_msg.chaddr[3], dhcp_recv_msg.chaddr[4], dhcp_recv_msg.chaddr[5]);

            // Подготовка DHCPACK
            memset(&dhcp_send_msg, 0, sizeof(dhcp_send_msg));
            dhcp_send_msg.op = DHCPACK;
            dhcp_send_msg.htype = 1;
            dhcp_send_msg.hlen = 6;
            dhcp_send_msg.xid = dhcp_recv_msg.xid; // Копирование ID транзакции из запроса
            memcpy(dhcp_send_msg.chaddr, dhcp_recv_msg.chaddr, 6); // Копирование MAC-адреса клиента
            dhcp_send_msg.magic_cookie = htonl(DHCP_MAGIC_COOKIE);

            dhcp_send_msg.yiaddr = dhcp_recv_msg.yiaddr; // IP-адрес тот же, что и в DHCPOFFER
            inet_pton(AF_INET, "192.168.1.100", &dhcp_send_msg.siaddr);

            int option_index = 0;
            uint8_t dhcp_msg_type = DHCPACK;
            add_dhcp_option(dhcp_send_msg.options, DHCP_MESSAGE_TYPE, 1, &dhcp_msg_type, &option_index);

            struct in_addr subnet_mask_addr; // Структура для маски подсети
            inet_pton(AF_INET, "255.255.255.0", &subnet_mask_addr);
            add_dhcp_option(dhcp_send_msg.options, DHCP_SUBNET_MASK, 4, &subnet_mask_addr, &option_index);

            struct in_addr router_addr; // Структура для адреса маршрутизатора
            inet_pton(AF_INET, "192.168.1.1", &router_addr);
            add_dhcp_option(dhcp_send_msg.options, DHCP_ROUTER, 4, &router_addr, &option_index);

            struct in_addr dns_addr; // Структура для адреса DNS сервера
            inet_pton(AF_INET, "8.8.8.8", &dns_addr);
            add_dhcp_option(dhcp_send_msg.options, DHCP_DNS_SERVERS, 4, &dns_addr, &option_index);

            uint32_t lease_time = htonl(86400); // 1 день
            add_dhcp_option(dhcp_send_msg.options, DHCP_LEASE_TIME, 4, &lease_time, &option_index);
            
            printf("Отправка DHCPACK клиенту IP: %s\n", inet_ntoa(dhcp_send_msg.yiaddr));
            sendto(sockfd, &dhcp_send_msg, sizeof(dhcp_send_msg), 0, (struct sockaddr *)&client_addr, client_addr_len);
        }
    }

    close(sockfd); // Закрытие сокета
    return 0;
}