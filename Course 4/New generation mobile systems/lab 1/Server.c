// gcc Server.c -o server -lzmq

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <zmq.h>

#define MAX_CLIENTS 10

typedef struct {
    void* id_data;
    size_t id_len;
} client_data;

int main(void) {
    void *context = zmq_ctx_new();
    void *responder = zmq_socket(context, ZMQ_ROUTER);

    int rc = zmq_bind (responder, "tcp://*:5555");
    if (rc != 0) {
        perror("Ошибка zmq_bind");
        return 1;
    }
    printf("Сервер запущен на tcp://*:5555\n");

    client_data clients[MAX_CLIENTS];
    int client_count = 0;

    while (1) {
        zmq_msg_t client_id_msg;
        zmq_msg_init(&client_id_msg);
        zmq_msg_recv(&client_id_msg, responder, 0);
        
        zmq_msg_t body_msg;
        zmq_msg_init(&body_msg);
        zmq_msg_recv(&body_msg, responder, 0);

        size_t id_len = zmq_msg_size(&client_id_msg);
        void* id_data = zmq_msg_data(&client_id_msg);
        
        int sender_index = -1;
        int found = 0;
        for (int i = 0; i < client_count; i++) {
            if (clients[i].id_len == id_len && memcmp(clients[i].id_data, id_data, id_len) == 0) {
                found = 1;
                sender_index = i;
                break;
            }
        }

        if (!found && client_count < MAX_CLIENTS) {
            clients[client_count].id_data = malloc(id_len);
            memcpy(clients[client_count].id_data, id_data, id_len);
            clients[client_count].id_len = id_len;
            sender_index = client_count;
            client_count++;
            printf("Подключен новый клиент #%d\n", client_count);
        }

        for (int i = 0; i < client_count; i++) {
            if (i == sender_index) continue;

            zmq_msg_t recipient_id_msg;
            zmq_msg_init_size(&recipient_id_msg, clients[i].id_len);
            memcpy(zmq_msg_data(&recipient_id_msg), clients[i].id_data, clients[i].id_len);

            zmq_msg_t body_copy_msg;
            zmq_msg_init_data(&body_copy_msg, zmq_msg_data(&body_msg), zmq_msg_size(&body_msg), NULL, NULL);

            zmq_msg_send(&recipient_id_msg, responder, ZMQ_SNDMORE);
            zmq_msg_send(&body_copy_msg, responder, 0);
        }

        zmq_msg_close(&client_id_msg);
        zmq_msg_close(&body_msg);
    }

    zmq_close(responder);
    zmq_ctx_destroy(context);
    return 0;
}