#include <stdbool.h>
#include <stdio.h>
#include <fcntl.h>
#include <sys/types.h>
#include <unistd.h>
#include "log.h"

typedef struct log_t {
    bool is_open;
    FILE *fp;
} log_t;

// "/tmp" is writable on *nix systems
// on MacOS /tmp symlinks to /private/tmp which is writable by current user
// this value can be overriden by user
static char const *default_location = "/tmp/jetsam.log";
static log_t log = { true, NULL };

void log_init(char const *location) {
    log.fp = fopen(location == NULL ? default_location : location, "a");
    log.is_open = true;
}

bool log_pid(char const *func_name) {
    if (!log.is_open) log_init(NULL);
    pid_t pid = getpid();
    fprintf(log.fp, "%s:%d:running\n", func_name, pid);
    if (ferror(log.fp)) {
        return false;
    }
    fflush(log.fp);
    return true;
}

void log_info(char const *str) {
    if (!log.is_open) log_init(NULL);
    fprintf(log.fp, "%s\n", str); // pulls from errno
    fflush(log.fp); // to force write to disk
}

void log_error(char const *str) {
    if (!log.is_open) log_init(NULL);
    fprintf(log.fp, "%s\n", str); 
    fflush(log.fp);
    log_end(log);
}

void log_end() {
    fclose(log.fp);
}

// --- low level kernel calls ---

// int fd = open(pid_path, 
//     O_CREAT | O_CLOEXEC | O_TRUNC | O_RDWR, // CLOEXEC useful when forking
//     S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP // chmod 660
// );

// if (fd == -1 || write(fd, pid_num_str, strlen(pid_num_str)) == -1) {
//     return false;
// }

// close(fd);
// return true;