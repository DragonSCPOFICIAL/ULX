#include <stdio.h>
#include <stdint.h>
#include <string.h>

/* 
 * ULX ELF Generator
 * Este módulo permite que o compilador ULX escreva binários ELF64 
 * diretamente, sem depender de assemblers ou linkers externos.
 */

typedef struct {
    uint8_t  e_ident[16];
    uint16_t e_type;
    uint16_t e_machine;
    uint32_t e_version;
    uint64_t e_entry;
    uint64_t e_phoff;
    uint64_t e_shoff;
    uint32_t e_flags;
    uint16_t e_ehsize;
    uint16_t e_phentsize;
    uint16_t e_phnum;
    uint16_t e_shentsize;
    uint16_t e_shnum;
    uint16_t e_shstrndx;
} Elf64_Ehdr;

void generate_minimal_elf(const char* filename) {
    FILE* f = fopen(filename, "wb");
    if (!f) return;

    Elf64_Ehdr header;
    memset(&header, 0, sizeof(header));

    // Identificação ELF (Magic Number)
    header.e_ident[0] = 0x7f;
    header.e_ident[1] = 'E';
    header.e_ident[2] = 'L';
    header.e_ident[3] = 'F';
    header.e_ident[4] = 2; // 64-bit
    header.e_ident[5] = 1; // Little Endian
    header.e_ident[6] = 1; // Version 1
    
    header.e_type = 2;    // Executable
    header.e_machine = 62; // x86-64
    header.e_version = 1;
    header.e_ehsize = sizeof(Elf64_Ehdr);

    fwrite(&header, 1, sizeof(header), f);
    fclose(f);
    
    printf("[ULX-ELF] Cabeçalho ELF64 gerado para: %s\n", filename);
}
