// Keep lib as opaque as possible
void log_init(char const *location); // if user supplies different log file location
bool log_pid(char const *func_name);
void log_info(char const *str);
void log_error(char const *str); // will end logging as well
void log_end();
