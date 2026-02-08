BITS 64

section .text
    global _start
    global lnx_syscall
    global lnx_init_hardware

_start:
    call lnx_init_hardware
    jmp ulx_main_entry

lnx_syscall:
    syscall
    ret

lnx_init_hardware:
    mov rax, 1
    mov rdi, 1
    lea rsi, [rel msg_active]
    mov rdx, len_active
    syscall
    ret

section .data
    msg_active db "LNX_ACTIVE", 10, 0
    len_active equ $ - msg_active
