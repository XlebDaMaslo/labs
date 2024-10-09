#include <stdio.h>
#include <signal.h>
#include <unistd.h>

void signal_handler(int sig) {
    if (sig == SIGINT) {
        printf("\nReceived SIGINT (Ctrl+C), shutting down gracefully...\n");
    } else if (sig == SIGTERM) {
        printf("\nReceived SIGTERM, shutting down gracefully...\n");
    } else if (sig == SIGHUP) {
        printf("\nReceived SIGHUP, handling reconnection...\n");
    } else if (sig == SIGQUIT) {
        printf("\nReceived SIGQUIT, creating core dump and exiting...\n");
    }
    fflush(stdout);
    _exit(0); 
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);

    signal(SIGINT, signal_handler);
    signal(SIGTERM, signal_handler);
    signal(SIGHUP, signal_handler);
    signal(SIGQUIT, signal_handler);

    while (1) {
        printf("Running");
        fflush(stdout);
        sleep(1);

        for (int i = 0; i < 3; ++i) {
            printf(".");
            fflush(stdout);
            sleep(1);
        }
        printf("\n");
    }
    return 0;
}
