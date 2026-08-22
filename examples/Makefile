SHELL := /bin/sh
CC ?= cc
CFLAGS ?= -std=c11 -Wall -Wextra -Werror -pedantic -O2
BUILD_DIR ?= build
PROGRAMS := syscall-boundary lost-update bounded-buffer dining-cycle

all: $(PROGRAMS:%=$(BUILD_DIR)/%)
$(BUILD_DIR):
	mkdir -p $@
$(BUILD_DIR)/syscall-boundary: syscall-boundary.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) $< -o $@
$(BUILD_DIR)/lost-update: lost-update.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -pthread $< -o $@
$(BUILD_DIR)/bounded-buffer: bounded-buffer.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -pthread $< -o $@
$(BUILD_DIR)/dining-cycle: dining-cycle.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -pthread $< -o $@
clean:
	rm -rf $(BUILD_DIR)
