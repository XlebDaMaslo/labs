// gcc Сlient.c -o client -lzmq

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <zmq.h>
#include <unistd.h>


#define MAX_USERNAME_LEN 50
#define MAX_INPUT_LEN 450 

#define MAX_MESSAGE_LEN (MAX_USERNAME_LEN + MAX_INPUT_LEN + 3)

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "Использование: %s <имя_пользователя>\n", argv[0]);
        return 1;
    }
    const char *username = argv[1];

    if (strlen(username) > MAX_USERNAME_LEN) {
        fprintf(stderr, "Ошибка: Имя пользователя не должно превышать %d символов.\n", MAX_USERNAME_LEN);
        return 1;
    }

    void *context = zmq_ctx_new();
    void *requester = zmq_socket(context, ZMQ_DEALER);

    zmq_setsockopt(requester, ZMQ_IDENTITY, username, strlen(username));

    if (zmq_connect(requester, "tcp://localhost:5555") != 0) {
        perror("Ошибка zmq_connect");
        return 1;
    }
    printf("Добро пожаловать, '%s'. Введите сообщение и нажимайте Enter.\nВы: ", username);
    fflush(stdout);

    zmq_pollitem_t items[] = {
        { NULL, STDIN_FILENO, ZMQ_POLLIN, 0 },
        { requester, 0, ZMQ_POLLIN, 0 }
    };

    char input_buffer[MAX_INPUT_LEN];
    char message_to_send[MAX_MESSAGE_LEN];

    while (1) {
        zmq_poll(items, 2, -1);

        if (items[0].revents & ZMQ_POLLIN) {
            if (fgets(input_buffer, sizeof(input_buffer), stdin) == NULL) break;
            
            input_buffer[strcspn(input_buffer, "\n")] = 0;
            
            snprintf(message_to_send, sizeof(message_to_send), "%s: %s", username, input_buffer);

            zmq_send(requester, message_to_send, strlen(message_to_send), 0);

            printf("Вы: ");
            fflush(stdout);
        }

        if (items[1].revents & ZMQ_POLLIN) {
            int size = zmq_recv(requester, message_to_send, sizeof(message_to_send) - 1, 0);
            if (size < 0) break;
            
            message_to_send[size] = '\0';
            
            printf("\r%s\nВы: ", message_to_send);
            fflush(stdout);
        }
    }

    zmq_close(requester);
    zmq_ctx_destroy(context);
    return 0;
}