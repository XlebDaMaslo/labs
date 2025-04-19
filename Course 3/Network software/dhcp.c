#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/types.h>
// #include <netdb.h>           // Для gethostbyname и struct hostent
#include <errno.h>
#include <time.h>

#define DHCP_SERVER_PORT 67         // Порт сервера DHCP (67)
#define DHCP_CLIENT_PORT 68         // Порт клиента DHCP (68)
#define MAX_LEASES 256              // Максимальное число записей аренды
#define MAX_ADDR   256              // Максимальное число IP-адресов
#define BUF_SIZE   1024             // Размер буфера для приема/передачи

// DHCP-пакет (упрощенная структура)
struct dhcp_packet {
    uint8_t  op;
    uint8_t  htype;
    uint8_t  hlen;
    uint8_t  hops;
    uint32_t xid;
    uint16_t secs;
    uint16_t flags;
    uint32_t ciaddr;
    uint32_t yiaddr;
    uint32_t siaddr;
    uint32_t giaddr;
    uint8_t  chaddr[16];
    uint8_t  sname[64];
    uint8_t  file[128];
    uint8_t  options[312];  // Опции DHCP (magic cookie + переменные опции)
};

// Запись аренды: MAC-адрес клиента и назначенный IP
struct lease {
    uint8_t  mac[16];
    uint32_t ip;
    int      used;
};

static struct lease leases[MAX_LEASES];       // Массив аренды
static uint32_t addr_list[MAX_ADDR];          // Список доступных IP-адресов
static int      addr_count = 0;               // Число адресов
static uint32_t server_ip  = 0;               // IP-адрес сервера (для поля siaddr)

// Загрузка списка адресов из файла
int load_addr_list(const char *filename) {
    FILE *f = fopen(filename, "r");
    if (!f) {
        perror("Ошибка открытия файла адресов");
        return -1;
    }
    char line[100];
    while (fgets(line, sizeof(line), f) && addr_count < MAX_ADDR) {
        if (line[0]=='#' || strlen(line)<7) continue;
        struct in_addr a;
        if (inet_aton(line, &a)) {
            addr_list[addr_count++] = a.s_addr;
        }
    }
    fclose(f);
    return 0;
}

// Поиск уже существующей аренды по MAC-адресу
int find_lease(uint8_t *mac) {
    for (int i = 0; i < addr_count; i++) {
        if (leases[i].used && memcmp(leases[i].mac, mac, 16) == 0) {
            return i;
        }
    }
    return -1;
}

// Назначение IP-адреса новому клиенту или возврат существующего
int allocate_ip(uint8_t *mac) {
    int idx = find_lease(mac);
    if (idx >= 0) {
        return idx;  // Уже было выделено
    }
    // Найти свободный адрес
    for (int i = 0; i < addr_count; i++) {
        if (!leases[i].used) {
            leases[i].used = 1;
            memcpy(leases[i].mac, mac, 16);
            leases[i].ip = addr_list[i];
            return i;
        }
    }
    return -1; // Нет свободных адресов
}

// Получить опцию DHCP из пакета
int get_dhcp_option(uint8_t *options, uint8_t code, uint8_t *len, uint8_t **data) {
    int i = 4; // пропустить magic cookie
    while (i < sizeof(((struct dhcp_packet*)0)->options)) {
        if (options[i] == 255) break; // End
        uint8_t c = options[i++];
        uint8_t l = options[i++];
        if (c == code) {
            *len = l;
            *data = &options[i];
            return 0;
        }
        i += l;
    }
    return -1;
}

// Добавить опцию DHCP в пакет
void add_dhcp_option(uint8_t *options, int *idx, uint8_t code, uint8_t len, uint8_t *data) {
    options[(*idx)++] = code;
    options[(*idx)++] = len;
    memcpy(&options[*idx], data, len);
    *idx += len;
}

// Обработчик DHCPDISCOVER: формирует и отправляет DHCPOFFER
void handle_discover(int sock, struct dhcp_packet *req) {
    int lease_idx = allocate_ip(req->chaddr);
    if (lease_idx < 0) {
        printf("Нет свободных IP-адресов для клиента\n");
        return;
    }
    struct dhcp_packet offer;
    memset(&offer, 0, sizeof(offer));
    offer.op = 2; // BOOTREPLY
    offer.htype = req->htype;
    offer.hlen   = req->hlen;
    offer.xid    = req->xid;
    offer.yiaddr = leases[lease_idx].ip;
    offer.siaddr = server_ip;
    memcpy(offer.chaddr, req->chaddr, 16);
    // Magic cookie
    uint8_t *opt = offer.options;
    opt[0]=99; opt[1]=130; opt[2]=83; opt[3]=99;
    int idx = 4;
    // Опция DHCP Message Type = DHCPOFFER (2)
    uint8_t msg_type = 2;
    add_dhcp_option(opt, &idx, 53, 1, &msg_type);
    // Опция Subnet Mask = 255.255.255.0
    uint32_t mask = htonl(0xFFFFFF00);
    add_dhcp_option(opt, &idx, 1, 4, (uint8_t*)&mask);
    // Опция Router = сервер
    add_dhcp_option(opt, &idx, 3, 4, (uint8_t*)&server_ip);
    // Опция Lease Time = 60 min
    uint32_t lease = htonl(60);
    add_dhcp_option(opt, &idx, 51, 4, (uint8_t*)&lease);
    // Опция Server Identifier
    add_dhcp_option(opt, &idx, 54, 4, (uint8_t*)&server_ip);
    // End
    opt[idx++] = 255;

    struct sockaddr_in dest = {0};
    dest.sin_family = AF_INET;
    dest.sin_port   = htons(DHCP_CLIENT_PORT);
    dest.sin_addr.s_addr = INADDR_BROADCAST;
    sendto(sock, &offer, sizeof(offer), 0,
        (struct sockaddr*)&dest, sizeof(dest));
    printf("DHCPOFFER отправлен клиенту %02x:%02x:%02x:%02x:%02x:%02x -> %s\n",
        req->chaddr[0],req->chaddr[1],req->chaddr[2],req->chaddr[3],req->chaddr[4],req->chaddr[5],
        inet_ntoa(*(struct in_addr*)&offer.yiaddr));
}

// Обработчик DHCPREQUEST: формирует и отправляет DHCPACK
void handle_request(int sock, struct dhcp_packet *req) {
    uint32_t requested;
    uint8_t *pdata;
    uint8_t plen;
    // Сначала пробуем опцию 'requested IP' (код 50)
    if (get_dhcp_option(req->options, 50, &plen, &pdata) == 0) {
        requested = *(uint32_t*)pdata;
    } else if (req->ciaddr != 0) {
        // Если клиент уже имеет IP (renewal), берем ciaddr
        requested = req->ciaddr;
    } else {
        printf("DHCPREQUEST без запрошенного IP (нет опции 50 и ciaddr == 0)\n");
        return;
    }
    // Проверяем, что запрос именно нашему серверу (опция 54)
    if (get_dhcp_option(req->options, 54, &plen, &pdata) == 0) {
        uint32_t sid = *(uint32_t*)pdata;
        if (sid != server_ip) {
            printf("DHCPREQUEST предназначен другому серверу %s\n", inet_ntoa(*(struct in_addr*)&sid));
            return;
        }
    }
    // Находим аренду по MAC и проверяем IP
    int idx = find_lease(req->chaddr);
    if (idx < 0 || leases[idx].ip != requested) {
        printf("Запрошенный IP %s не совпадает с арендой для этого клиента\n", inet_ntoa(*(struct in_addr*)&requested));
        return;
    }
    // Формируем ACK
    struct dhcp_packet ack;
    memset(&ack, 0, sizeof(ack));
    ack.op = 2;
    ack.htype = req->htype;
    ack.hlen   = req->hlen;
    ack.xid    = req->xid;
    ack.yiaddr = requested;
    ack.siaddr = server_ip;
    memcpy(ack.chaddr, req->chaddr, 16);
    // Опции
    uint8_t *opt = ack.options;
    opt[0]=99; opt[1]=130; opt[2]=83; opt[3]=99;
    int oidx = 4;
    uint8_t msg_type = 5; // DHCPACK
    add_dhcp_option(opt, &oidx, 53, 1, &msg_type);
    uint32_t mask = htonl(0xFFFFFF00);
    add_dhcp_option(opt, &oidx, 1, 4, (uint8_t*)&mask);
    add_dhcp_option(opt, &oidx, 3, 4, (uint8_t*)&server_ip);
    uint32_t lease_time = htonl(60);
    add_dhcp_option(opt, &oidx, 51, 4, (uint8_t*)&lease_time);
    add_dhcp_option(opt, &oidx, 54, 4, (uint8_t*)&server_ip);
    opt[oidx++] = 255;
    
    struct sockaddr_in dest = {0};
    dest.sin_family = AF_INET;
    dest.sin_port   = htons(DHCP_CLIENT_PORT);
    dest.sin_addr.s_addr = INADDR_BROADCAST;
    sendto(sock, &ack, sizeof(ack), 0,
        (struct sockaddr*)&dest, sizeof(dest));
    printf("DHCPACK отправлен клиенту %02x:%02x:%02x:%02x:%02x:%02x -> %s\n",
        req->chaddr[0],req->chaddr[1],req->chaddr[2],req->chaddr[3],req->chaddr[4],req->chaddr[5],
        inet_ntoa(*(struct in_addr*)&ack.yiaddr));
}

int main() {
    // Получаем IP сервера через gethostbyname
    char host[256];
    // if (gethostname(host, sizeof(host)) < 0) perror("gethostname");
    server_ip = inet_addr("192.168.1.1");
    // struct hostent *he = gethostbyname(host);
//  if (!he) {
//      perror("gethostbyname");
//      return 1;
//  }
    // memcpy(&server_ip, he->h_addr_list[0], 4);
    printf("DHCP-сервер запущен на IP %s\n", inet_ntoa(*(struct in_addr*)&server_ip));

    if (load_addr_list("address_list.txt") < 0) return 1;
    printf("Загружено %d IP-адресов для аренды\n", addr_count);

    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        perror("socket");
        return 1;
    }
    int optval = 1;
    setsockopt(sock, SOL_SOCKET, SO_BROADCAST, &optval, sizeof(optval));

    struct sockaddr_in servaddr = {0};
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = INADDR_ANY;
    servaddr.sin_port = htons(DHCP_SERVER_PORT);
    if (bind(sock, (struct sockaddr*)&servaddr, sizeof(servaddr)) < 0) {
        perror("bind");
        return 1;
    }

    while (1) {
        struct dhcp_packet buf;
        struct sockaddr_in cliaddr;
        socklen_t len = sizeof(cliaddr);
        ssize_t n = recvfrom(sock, &buf, sizeof(buf), 0,
                            (struct sockaddr*)&cliaddr, &len);
        if (n < 0) {
            perror("recvfrom");
            continue;
        }
        uint8_t *data;
        uint8_t dlen;
        if (get_dhcp_option(buf.options, 53, &dlen, &data) < 0) continue;
        uint8_t msg_type = data[0];
        if (msg_type == 1) { // DHCPDISCOVER
            handle_discover(sock, &buf);
        } else if (msg_type == 3) { // DHCPREQUEST
            handle_request(sock, &buf);
        }
    }

    close(sock);
    return 0;
}
