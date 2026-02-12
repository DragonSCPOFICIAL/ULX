# Makefile para ULX

.PHONY: all build install uninstall clean test examples

# Diretórios
SRC_DIR = src/compiler
CORE_DIR = core/lnx
BIN_DIR = bin
PREFIX = /usr/local

# Compiladores
PYTHON = python3
NASM = nasm
GCC = gcc

# Flags
NASM_FLAGS = -f elf64
GCC_FLAGS = -O2 -static

all: build

# Compilar tudo
build: build-compiler build-runtime

# Compilar compilador Python
build-compiler:
	@echo "Building ULX compiler..."
	@mkdir -p $(BIN_DIR)
	@chmod +x $(SRC_DIR)/ulxc.py
	@ln -sf $(SRC_DIR)/ulxc.py $(BIN_DIR)/ulxc 2>/dev/null || true

# Compilar runtime em assembly
build-runtime:
	@echo "Building LNX runtime..."
	@mkdir -p $(BIN_DIR)
	$(NASM) $(NASM_FLAGS) $(CORE_DIR)/lnx_syscall.asm -o $(BIN_DIR)/lnx_syscall.o 2>/dev/null || echo "NASM not available, skipping assembly build"

# Instalar
install: build
	@echo "Installing ULX..."
	@install -d $(PREFIX)/bin
	@install -d $(PREFIX)/lib/ulx
	@install -m 755 $(SRC_DIR)/ulxc.py $(PREFIX)/bin/ulxc
	@cp -r src $(PREFIX)/lib/ulx/
	@cp -r core $(PREFIX)/lib/ulx/
	@echo "ULX installed to $(PREFIX)/bin/ulxc"

# Desinstalar
uninstall:
	@echo "Uninstalling ULX..."
	@rm -f $(PREFIX)/bin/ulxc
	@rm -rf $(PREFIX)/lib/ulx
	@echo "ULX uninstalled"

# Limpar
clean:
	@echo "Cleaning..."
	@rm -rf $(BIN_DIR)
	@rm -f *.o *.out *.elf
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete

# Testar
test: build
	@echo "Running tests..."
	@$(PYTHON) $(SRC_DIR)/ulx_parser.py
	@$(PYTHON) $(SRC_DIR)/ulx_ir.py
	@echo "All tests passed!"

# Compilar exemplos
examples: build
	@echo "Building examples..."
	@for f in examples/*.ulx; do \
		echo "Compiling $$f..."; \
		$(PYTHON) $(SRC_DIR)/ulxc.py "$$f" -o "$${f%.ulx}" 2>/dev/null || echo "Failed: $$f"; \
	done

# Desenvolvimento
dev-setup:
	@echo "Setting up development environment..."
	@pip3 install -r requirements.txt 2>/dev/null || echo "No requirements.txt"

# Formatar código
format:
	@echo "Formatting code..."
	@black $(SRC_DIR)/*.py 2>/dev/null || echo "black not installed"

# Verificar tipos
typecheck:
	@echo "Type checking..."
	@mypy $(SRC_DIR)/*.py 2>/dev/null || echo "mypy not installed"

# Documentação
docs:
	@echo "Generating documentation..."
	@cd docs && make html 2>/dev/null || echo "Documentation build not configured"

# Ajuda
help:
	@echo "ULX Makefile targets:"
	@echo "  make build       - Build compiler and runtime"
	@echo "  make install     - Install ULX system-wide"
	@echo "  make uninstall   - Remove ULX from system"
	@echo "  make clean       - Clean build artifacts"
	@echo "  make test        - Run tests"
	@echo "  make examples    - Build example programs"
	@echo "  make help        - Show this help"
