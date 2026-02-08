BITS 64

section .text
    global _start
    global lnx_syscall
    global lnx_init_all
    global lnx_video_init
    global lnx_audio_init
    global lnx_net_init
    global lnx_input_init
    global lnx_mem_init

_start:
    call lnx_init_all
    jmp ulx_main_entry

lnx_init_all:
    call lnx_mem_init
    call lnx_video_init
    call lnx_audio_init
    call lnx_net_init
    call lnx_input_init
    ret

lnx_syscall:
    syscall
    ret

lnx_video_init:
    mov rax, 2
    lea rdi, [rel dev_fb]
    mov rsi, 2
    syscall
    mov [fb_fd], rax
    ret

lnx_audio_init:
    mov rax, 2
    lea rdi, [rel dev_snd]
    mov rsi, 2
    syscall
    mov [snd_fd], rax
    ret

lnx_net_init:
    mov rax, 41
    mov rdi, 2
    mov rsi, 1
    mov rdx, 0
    syscall
    mov [sock_fd], rax
    ret

lnx_input_init:
    mov rax, 2
    lea rdi, [rel dev_input]
    mov rsi, 0
    syscall
    mov [input_fd], rax
    ret

lnx_mem_init:
    mov rax, 12
    xor rdi, rdi
    syscall
    mov [heap_start], rax
    ret

lnx_write:
    mov rax, 1
    syscall
    ret

lnx_read:
    mov rax, 0
    syscall
    ret

lnx_open:
    mov rax, 2
    syscall
    ret

lnx_close:
    mov rax, 3
    syscall
    ret

lnx_mmap:
    mov rax, 9
    syscall
    ret

lnx_fork:
    mov rax, 57
    syscall
    ret

lnx_execve:
    mov rax, 59
    syscall
    ret

lnx_exit:
    mov rax, 60
    syscall

lnx_getpid:
    mov rax, 39
    syscall
    ret

lnx_socket:
    mov rax, 41
    syscall
    ret

lnx_connect:
    mov rax, 42
    syscall
    ret

lnx_accept:
    mov rax, 43
    syscall
    ret

lnx_bind:
    mov rax, 49
    syscall
    ret

lnx_listen:
    mov rax, 50
    syscall
    ret

lnx_nanosleep:
    mov rax, 35
    syscall
    ret

section .data
    dev_fb db "/dev/fb0", 0
    dev_snd db "/dev/snd/pcmC0D0p", 0
    dev_input db "/dev/input/event0", 0
    
section .bss
    fb_fd resq 1
    snd_fd resq 1
    sock_fd resq 1
    input_fd resq 1
    heap_start resq 1
