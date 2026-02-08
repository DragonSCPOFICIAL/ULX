CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -pedantic
LDFLAGS = -lX11
# Nota: Removemos o -static temporariamente para linkar com a X11 do sistema, 
# mas o objetivo final é embutir tudo.

BIN_DIR = bin
SRC_COMPILER_DIR = src/compiler
SRC_LIB_DIR = src/lib

ULXC_SRC = $(SRC_COMPILER_DIR)/main.c
ULX_PLAYER_SRC = src/ulx-player.c
ULXC_BIN = $(BIN_DIR)/ulxc
ULX_RUN_BIN = $(BIN_DIR)/ulx-run

.PHONY: all clean

all: $(ULXC_BIN) $(ULX_RUN_BIN)

$(ULXC_BIN): $(ULXC_SRC)
	mkdir -p $(BIN_DIR)
	$(CC) $(CFLAGS) $(ULXC_SRC) -o $(ULXC_BIN)

$(ULX_RUN_BIN): $(ULX_PLAYER_SRC)
	mkdir -p $(BIN_DIR)
	$(CC) $(CFLAGS) $(ULX_PLAYER_SRC) -o $(ULX_RUN_BIN) $(LDFLAGS)

clean:
	rm -f $(ULXC_BIN)

