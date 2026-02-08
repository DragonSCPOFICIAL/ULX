BITS 64
section .text
global _start

_start:
    ; Inicializacao de hardware para o HoloClock
    call lnx_init_video_accel
    call lnx_unlock_cpu_speed
    
    ; Loop de renderização infinita (FPS Ilimitado)
.loop:
    call update_time_buffer
    call lnx_push_frame
    jmp .loop

update_time_buffer:
    mov rax, 201 ; sys_time
    xor rdi, rdi
    syscall
    ret

lnx_init_video_accel:
    mov rax, 2 ; open
    lea rdi, [rel fb_path]
    mov rsi, 2 ; O_RDWR
    syscall
    ret

lnx_unlock_cpu_speed:
    ret

lnx_push_frame:
    ret

section .data
    fb_path db "/dev/fb0", 0
