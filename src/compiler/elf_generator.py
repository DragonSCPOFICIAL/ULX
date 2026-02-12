#!/usr/bin/env python3
"""
ELF Generator - Gera binários ELF64 completos
Implementação direta do formato ELF sem dependências externas
"""

import struct
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ELFConstants:
    """Constantes do formato ELF"""
    ELFMAG = b'\x7fELF'
    ELFCLASS64 = 2
    ELFDATA2LSB = 1  # Little-endian
    EV_CURRENT = 1
    ELFOSABI_LINUX = 0
    ELFOSABI_GNU = 3
    
    ET_EXEC = 2
    ET_DYN = 3
    
    EM_X86_64 = 62
    
    PT_LOAD = 1
    PT_DYNAMIC = 2
    PT_INTERP = 3
    PT_NOTE = 4
    
    PF_X = 1
    PF_W = 2
    PF_R = 4
    
    SHT_NULL = 0
    SHT_PROGBITS = 1
    SHT_SYMTAB = 2
    SHT_STRTAB = 3
    SHT_RELA = 4
    SHT_HASH = 5
    SHT_DYNAMIC = 6
    SHT_NOTE = 7
    SHT_NOBITS = 8
    SHT_REL = 9
    
    SHF_WRITE = 1
    SHF_ALLOC = 2
    SHF_EXECINSTR = 4
    
    STB_GLOBAL = 1
    STT_FUNC = 2
    STT_OBJECT = 1
    STT_SECTION = 3


@dataclass
class Elf64_Ehdr:
    """ELF64 Header"""
    e_ident: bytes = field(default_factory=lambda: b'\x00' * 16)
    e_type: int = 0
    e_machine: int = 0
    e_version: int = 0
    e_entry: int = 0
    e_phoff: int = 0
    e_shoff: int = 0
    e_flags: int = 0
    e_ehsize: int = 0
    e_phentsize: int = 0
    e_phnum: int = 0
    e_shentsize: int = 0
    e_shnum: int = 0
    e_shstrndx: int = 0
    
    def pack(self) -> bytes:
        return struct.pack('<16sHHIIQQIIHHHHHH',
            self.e_ident,
            self.e_type,
            self.e_machine,
            self.e_version,
            self.e_entry,
            self.e_phoff,
            self.e_shoff,
            self.e_flags,
            self.e_ehsize,
            self.e_phentsize,
            self.e_phnum,
            self.e_shentsize,
            self.e_shnum,
            self.e_shstrndx
        )


@dataclass
class Elf64_Phdr:
    """ELF64 Program Header"""
    p_type: int = 0
    p_flags: int = 0
    p_offset: int = 0
    p_vaddr: int = 0
    p_paddr: int = 0
    p_filesz: int = 0
    p_memsz: int = 0
    p_align: int = 0
    
    def pack(self) -> bytes:
        return struct.pack('<IIQQQQQQ',
            self.p_type,
            self.p_flags,
            self.p_offset,
            self.p_vaddr,
            self.p_paddr,
            self.p_filesz,
            self.p_memsz,
            self.p_align
        )


@dataclass
class Elf64_Shdr:
    """ELF64 Section Header"""
    sh_name: int = 0
    sh_type: int = 0
    sh_flags: int = 0
    sh_addr: int = 0
    sh_offset: int = 0
    sh_size: int = 0
    sh_link: int = 0
    sh_info: int = 0
    sh_addralign: int = 0
    sh_entsize: int = 0
    
    def pack(self) -> bytes:
        return struct.pack('<IIQQQQIIQQ',
            self.sh_name,
            self.sh_type,
            self.sh_flags,
            self_addr,
            self.sh_offset,
            self.sh_size,
            self.sh_link,
            self.sh_info,
            self.sh_addralign,
            self.sh_entsize
        )


@dataclass
class Elf64_Sym:
    """ELF64 Symbol Table Entry"""
    st_name: int = 0
    st_info: int = 0
    st_other: int = 0
    st_shndx: int = 0
    st_value: int = 0
    st_size: int = 0
    
    def pack(self) -> bytes:
        return struct.pack('<IBBHQQ',
            self.st_name,
            self.st_info,
            self.st_other,
            self.st_shndx,
            self.st_value,
            self.st_size
        )


@dataclass
class Section:
    """Seção do ELF"""
    name: str
    sh_type: int
    sh_flags: int
    data: bytes = b''
    addr: int = 0
    addralign: int = 1
    entsize: int = 0
    link: int = 0
    info: int = 0
    
    def size(self) -> int:
        return len(self.data)


@dataclass
class Symbol:
    """Símbolo"""
    name: str
    value: int
    size: int
    section_idx: int
    is_global: bool = True
    is_function: bool = False


class ELFBuilder:
    """Builder para criar binários ELF64"""
    
    def __init__(self, entry_point: int = 0x400000):
        self.entry_point = entry_point
        self.sections: List[Section] = []
        self.symbols: List[Symbol] = []
        self.section_names: List[str] = []
        self.string_table: bytes = b'\x00'
        
        # Adicionar seção nula
        self.add_section("", ELFConstants.SHT_NULL, 0, b'')
    
    def add_string(self, s: str) -> int:
        """Adiciona string à tabela de strings e retorna offset"""
        offset = len(self.string_table)
        self.string_table += s.encode('utf-8') + b'\x00'
        return offset
    
    def add_section(self, name: str, sh_type: int, sh_flags: int, 
                    data: bytes = b'', addralign: int = 1) -> int:
        """Adiciona uma seção e retorna seu índice"""
        idx = len(self.sections)
        self.section_names.append(name)
        section = Section(name, sh_type, sh_flags, data, addralign=addralign)
        self.sections.append(section)
        return idx
    
    def add_symbol(self, name: str, value: int, size: int, 
                   section_idx: int, is_global: bool = True, 
                   is_function: bool = False):
        """Adiciona um símbolo"""
        self.symbols.append(Symbol(name, value, size, section_idx, 
                                   is_global, is_function))
    
    def align(self, offset: int, alignment: int) -> int:
        """Alinha offset ao boundary especificado"""
        if alignment <= 1:
            return offset
        return (offset + alignment - 1) & ~(alignment - 1)
    
    def build(self) -> bytes:
        """Constrói o binário ELF completo"""
        # Layout do arquivo:
        # 0x00: ELF Header (64 bytes)
        # 0x40: Program Headers
        # ...: Sections
        # ...: Section Headers
        
        # Calcular offsets
        elf_header_size = 64
        phdr_size = 56
        shdr_size = 64
        
        num_phdrs = 0
        num_sections = len(self.sections)
        
        # Calcular tamanho necessário para program headers
        # Precisamos de pelo menos um PT_LOAD para código e dados
        has_code = any(s.sh_flags & ELFConstants.SHF_EXECINSTR for s in self.sections)
        has_data = any(s.sh_flags & ELFConstants.SHF_WRITE for s in self.sections)
        
        num_phdrs = 1  # Pelo menos um segmento de load
        
        phdr_offset = elf_header_size
        sections_offset = self.align(phdr_offset + num_phdrs * phdr_size, 4096)
        
        # Atribuir endereços virtuais e offsets
        current_offset = sections_offset
        current_vaddr = self.entry_point
        
        for section in self.sections:
            if section.sh_type == ELFConstants.SHT_NULL:
                continue
            
            # Alinhar
            current_offset = self.align(current_offset, section.addralign)
            
            section.addr = current_vaddr
            section.sh_offset = current_offset
            
            current_offset += section.size()
            current_vaddr += section.size()
        
        # Calcular offset dos section headers
        shdr_offset = self.align(current_offset, 8)
        
        # Criar section header string table
        shstrtab_data = b'\x00'.join(name.encode('utf-8') for name in self.section_names) + b'\x00'
        shstrtab_idx = self.add_section(".shstrtab", ELFConstants.SHT_STRTAB, 0, shstrtab_data)
        
        # Criar symbol table
        symtab_data = b''
        strtab_data = b'\x00'
        
        for sym in self.symbols:
            name_offset = len(strtab_data)
            strtab_data += sym.name.encode('utf-8') + b'\x00'
            
            info = (ELFConstants.STB_GLOBAL << 4) | (
                ELFConstants.STT_FUNC if sym.is_function else ELFConstants.STT_OBJECT
            )
            
            elf_sym = Elf64_Sym(
                st_name=name_offset,
                st_info=info,
                st_other=0,
                st_shndx=sym.section_idx,
                st_value=sym.value,
                st_size=sym.size
            )
            symtab_data += elf_sym.pack()
        
        # Adicionar tabelas
        if self.symbols:
            strtab_idx = self.add_section(".strtab", ELFConstants.SHT_STRTAB, 0, strtab_data)
            symtab_idx = self.add_section(".symtab", ELFConstants.SHT_SYMTAB, 0, symtab_data)
            # Atualizar link e info do symtab
            self.sections[symtab_idx].link = strtab_idx
            self.sections[symtab_idx].info = 1  # Primeiro símbolo global
        
        # Recalcular offsets com as novas seções
        current_offset = sections_offset
        current_vaddr = self.entry_point
        
        for section in self.sections:
            if section.sh_type == ELFConstants.SHT_NULL:
                continue
            
            current_offset = self.align(current_offset, section.addralign)
            section.addr = current_vaddr
            section.sh_offset = current_offset
            current_offset += section.size()
        
        shdr_offset = self.align(current_offset, 8)
        
        # Criar ELF header
        ehdr = Elf64_Ehdr()
        ehdr.e_ident = (ELFConstants.ELFMAG + 
                       bytes([ELFConstants.ELFCLASS64,
                             ELFConstants.ELFDATA2LSB,
                             ELFConstants.EV_CURRENT,
                             ELFConstants.ELFOSABI_LINUX]) +
                       b'\x00' * 8)
        ehdr.e_type = ELFConstants.ET_EXEC
        ehdr.e_machine = ELFConstants.EM_X86_64
        ehdr.e_version = 1
        ehdr.e_entry = self.entry_point + sections_offset  # Ajustar entry point
        ehdr.e_phoff = phdr_offset
        ehdr.e_shoff = shdr_offset
        ehdr.e_flags = 0
        ehdr.e_ehsize = elf_header_size
        ehdr.e_phentsize = phdr_size
        ehdr.e_phnum = num_phdrs
        ehdr.e_shentsize = shdr_size
        ehdr.e_shnum = len(self.sections)
        ehdr.e_shstrndx = shstrtab_idx
        
        # Montar arquivo
        output = bytearray()
        
        # ELF Header
        output.extend(ehdr.pack())
        
        # Padding até program headers
        while len(output) < phdr_offset:
            output.append(0)
        
        # Program Headers
        # Segmento de load para código e dados
        load_size = sum(s.size() for s in self.sections if s.sh_type != ELFConstants.SHT_NULL)
        
        phdr = Elf64_Phdr()
        phdr.p_type = ELFConstants.PT_LOAD
        phdr.p_flags = ELFConstants.PF_R | ELFConstants.PF_W | ELFConstants.PF_X
        phdr.p_offset = sections_offset
        phdr.p_vaddr = self.entry_point
        phdr.p_paddr = self.entry_point
        phdr.p_filesz = load_size
        phdr.p_memsz = load_size
        phdr.p_align = 4096
        output.extend(phdr.pack())
        
        # Padding até sections
        while len(output) < sections_offset:
            output.append(0)
        
        # Sections
        for section in self.sections:
            # Alinhar
            while len(output) < section.sh_offset:
                output.append(0)
            output.extend(section.data)
        
        # Padding até section headers
        while len(output) < shdr_offset:
            output.append(0)
        
        # Section Headers
        for i, section in enumerate(self.sections):
            shdr = Elf64_Shdr()
            shdr.sh_name = self.add_string(section.name) if section.name else 0
            shdr.sh_type = section.sh_type
            shdr.sh_flags = section.sh_flags
            shdr.sh_addr = section.addr
            shdr.sh_offset = section.sh_offset
            shdr.sh_size = section.size()
            shdr.sh_link = section.link
            shdr.sh_info = section.info
            shdr.sh_addralign = section.addralign
            shdr.sh_entsize = section.entsize
            output.extend(shdr.pack())
        
        return bytes(output)


class SimpleELFGenerator:
    """Gerador ELF simplificado para binários básicos"""
    
    def __init__(self):
        self.code = bytearray()
        self.data = bytearray()
        self.entry_point = 0x400000
    
    def add_code(self, code: bytes):
        """Adiciona código"""
        self.code.extend(code)
    
    def add_data(self, data: bytes):
        """Adiciona dados"""
        self.data.extend(data)
    
    def generate_minimal_executable(self) -> bytes:
        """Gera executável ELF64 mínimo funcional"""
        # Código mínimo: exit(0)
        # mov $60, %rax  (syscall exit)
        # mov $0, %rdi   (status 0)
        # syscall
        minimal_code = bytes([
            0x48, 0xc7, 0xc0, 0x3c, 0x00, 0x00, 0x00,  # mov $60, %rax
            0x48, 0xc7, 0xc7, 0x00, 0x00, 0x00, 0x00,  # mov $0, %rdi
            0x0f, 0x05,                                  # syscall
        ])
        
        builder = ELFBuilder(self.entry_point)
        
        # Seção .text
        text_idx = builder.add_section(".text", 
                                       ELFConstants.SHT_PROGBITS,
                                       ELFConstants.SHF_ALLOC | ELFConstants.SHF_EXECINSTR,
                                       minimal_code,
                                       addralign=16)
        
        # Adicionar símbolo _start
        builder.add_symbol("_start", self.entry_point + 0x1000, 
                          len(minimal_code), text_idx, 
                          is_global=True, is_function=True)
        
        return builder.build()
    
    def generate_from_assembly(self, assembly_code: str) -> bytes:
        """Gera ELF a partir de código assembly (simplificado)"""
        # Assembler simplificado - apenas algumas instruções
        # Na prática, usaria um assembler completo
        
        # Por enquanto, retorna executável mínimo
        return self.generate_minimal_executable()


if __name__ == "__main__":
    # Teste
    gen = SimpleELFGenerator()
    elf = gen.generate_minimal_executable()
    
    # Salvar para arquivo
    with open("/mnt/okcomputer/output/test_elf", "wb") as f:
        f.write(elf)
    
    print(f"Generated ELF: {len(elf)} bytes")
    print(f"Magic: {elf[:4]}")
    
    # Verificar com readelf se disponível
    import subprocess
    try:
        result = subprocess.run(["readelf", "-h", "/mnt/okcomputer/output/test_elf"], 
                               capture_output=True, text=True)
        print(result.stdout)
    except:
        print("readelf not available")
