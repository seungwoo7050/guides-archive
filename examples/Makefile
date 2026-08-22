SHELL := /bin/sh
CC ?= cc
CFLAGS ?= -std=c11 -Wall -Wextra -Werror -pedantic -O2
BUILD_DIR ?= build
PROGRAMS := syscall-boundary

all: $(PROGRAMS:%=$(BUILD_DIR)/%)
$(BUILD_DIR):
	mkdir -p $@
$(BUILD_DIR)/syscall-boundary: syscall-boundary.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) $< -o $@
clean:
	rm -rf $(BUILD_DIR)
