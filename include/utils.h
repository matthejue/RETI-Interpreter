#ifndef UTILS_H
#define UTILS_H

#include <stdint.h>

#define INITIAL_BUFFER_SIZE 1024

uint32_t mod(int32_t a, int32_t b);
int64_t max(int64_t a, int64_t b);
int64_t min(int64_t a, int64_t b);
uint32_t sign_extend_22_to_32(uint32_t num);
uint32_t swap_endian_32(uint32_t value);
char *proper_str_cat(char *prefix, char *suffix);
char *read_stdin_content();
char *read_file_content(const char *file_path);
char *get_prgrm_content(const char *prgrm_path);
char *allocate_and_copy_string(const char *original);

#endif // UTILS_H
