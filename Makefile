CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -pedantic
LDFLAGS = -static

BIN_DIR = bin
SRC_COMPILER_DIR = src/compiler

ULXC_SRC = $(SRC_COMPILER_DIR)/main.c
ULXC_BIN = $(BIN_DIR)/ulxc

.PHONY: all clean

all: $(ULXC_BIN)

$(ULXC_BIN): $(ULXC_SRC)
	mkdir -p $(BIN_DIR)
	$(CC) $(CFLAGS) $(ULXC_SRC) -o $(ULXC_BIN) $(LDFLAGS)

clean:
	rm -f $(ULXC_BIN)

