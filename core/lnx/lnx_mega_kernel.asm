BITS 64

section .text
    global _start
    global lnx_entry
    global lnx_dispatch

_start:
    call lnx_init_system
    jmp ulx_main

lnx_init_system:
    call lnx_init_cpu
    call lnx_init_mmu
    call lnx_init_pci
    call lnx_init_usb
    call lnx_init_video
    call lnx_init_audio
    call lnx_init_network
    call lnx_init_input
    ret

lnx_syscall_0: mov rax, 0 \ syscall \ ret
lnx_syscall_1: mov rax, 1 \ syscall \ ret
lnx_syscall_2: mov rax, 2 \ syscall \ ret
lnx_syscall_3: mov rax, 3 \ syscall \ ret
lnx_syscall_4: mov rax, 4 \ syscall \ ret
lnx_syscall_5: mov rax, 5 \ syscall \ ret
lnx_syscall_6: mov rax, 6 \ syscall \ ret
lnx_syscall_7: mov rax, 7 \ syscall \ ret
lnx_syscall_8: mov rax, 8 \ syscall \ ret
lnx_syscall_9: mov rax, 9 \ syscall \ ret
lnx_syscall_10: mov rax, 10 \ syscall \ ret
lnx_syscall_11: mov rax, 11 \ syscall \ ret
lnx_syscall_12: mov rax, 12 \ syscall \ ret
lnx_syscall_13: mov rax, 13 \ syscall \ ret
lnx_syscall_14: mov rax, 14 \ syscall \ ret
lnx_syscall_15: mov rax, 15 \ syscall \ ret
lnx_syscall_16: mov rax, 16 \ syscall \ ret
lnx_syscall_17: mov rax, 17 \ syscall \ ret
lnx_syscall_18: mov rax, 18 \ syscall \ ret
lnx_syscall_19: mov rax, 19 \ syscall \ ret
lnx_syscall_20: mov rax, 20 \ syscall \ ret
lnx_syscall_21: mov rax, 21 \ syscall \ ret
lnx_syscall_22: mov rax, 22 \ syscall \ ret
lnx_syscall_23: mov rax, 23 \ syscall \ ret
lnx_syscall_24: mov rax, 24 \ syscall \ ret
lnx_syscall_25: mov rax, 25 \ syscall \ ret
lnx_syscall_26: mov rax, 26 \ syscall \ ret
lnx_syscall_27: mov rax, 27 \ syscall \ ret
lnx_syscall_28: mov rax, 28 \ syscall \ ret
lnx_syscall_29: mov rax, 29 \ syscall \ ret
lnx_syscall_30: mov rax, 30 \ syscall \ ret
lnx_syscall_31: mov rax, 31 \ syscall \ ret
lnx_syscall_32: mov rax, 32 \ syscall \ ret
lnx_syscall_33: mov rax, 33 \ syscall \ ret
lnx_syscall_34: mov rax, 34 \ syscall \ ret
lnx_syscall_35: mov rax, 35 \ syscall \ ret
lnx_syscall_36: mov rax, 36 \ syscall \ ret
lnx_syscall_37: mov rax, 37 \ syscall \ ret
lnx_syscall_38: mov rax, 38 \ syscall \ ret
lnx_syscall_39: mov rax, 39 \ syscall \ ret
lnx_syscall_40: mov rax, 40 \ syscall \ ret
lnx_syscall_41: mov rax, 41 \ syscall \ ret
lnx_syscall_42: mov rax, 42 \ syscall \ ret
lnx_syscall_43: mov rax, 43 \ syscall \ ret
lnx_syscall_44: mov rax, 44 \ syscall \ ret
lnx_syscall_45: mov rax, 45 \ syscall \ ret
lnx_syscall_46: mov rax, 46 \ syscall \ ret
lnx_syscall_47: mov rax, 47 \ syscall \ ret
lnx_syscall_48: mov rax, 48 \ syscall \ ret
lnx_syscall_49: mov rax, 49 \ syscall \ ret
lnx_syscall_50: mov rax, 50 \ syscall \ ret
lnx_syscall_51: mov rax, 51 \ syscall \ ret
lnx_syscall_52: mov rax, 52 \ syscall \ ret
lnx_syscall_53: mov rax, 53 \ syscall \ ret
lnx_syscall_54: mov rax, 54 \ syscall \ ret
lnx_syscall_55: mov rax, 55 \ syscall \ ret
lnx_syscall_56: mov rax, 56 \ syscall \ ret
lnx_syscall_57: mov rax, 57 \ syscall \ ret
lnx_syscall_58: mov rax, 58 \ syscall \ ret
lnx_syscall_59: mov rax, 59 \ syscall \ ret
lnx_syscall_60: mov rax, 60 \ syscall \ ret
lnx_syscall_61: mov rax, 61 \ syscall \ ret
lnx_syscall_62: mov rax, 62 \ syscall \ ret
lnx_syscall_63: mov rax, 63 \ syscall \ ret
lnx_syscall_64: mov rax, 64 \ syscall \ ret
lnx_syscall_65: mov rax, 65 \ syscall \ ret
lnx_syscall_66: mov rax, 66 \ syscall \ ret
lnx_syscall_67: mov rax, 67 \ syscall \ ret
lnx_syscall_68: mov rax, 68 \ syscall \ ret
lnx_syscall_69: mov rax, 69 \ syscall \ ret
lnx_syscall_70: mov rax, 70 \ syscall \ ret
lnx_syscall_71: mov rax, 71 \ syscall \ ret
lnx_syscall_72: mov rax, 72 \ syscall \ ret
lnx_syscall_73: mov rax, 73 \ syscall \ ret
lnx_syscall_74: mov rax, 74 \ syscall \ ret
lnx_syscall_75: mov rax, 75 \ syscall \ ret
lnx_syscall_76: mov rax, 76 \ syscall \ ret
lnx_syscall_77: mov rax, 77 \ syscall \ ret
lnx_syscall_78: mov rax, 78 \ syscall \ ret
lnx_syscall_79: mov rax, 79 \ syscall \ ret
lnx_syscall_80: mov rax, 80 \ syscall \ ret
lnx_syscall_81: mov rax, 81 \ syscall \ ret
lnx_syscall_82: mov rax, 82 \ syscall \ ret
lnx_syscall_83: mov rax, 83 \ syscall \ ret
lnx_syscall_84: mov rax, 84 \ syscall \ ret
lnx_syscall_85: mov rax, 85 \ syscall \ ret
lnx_syscall_86: mov rax, 86 \ syscall \ ret
lnx_syscall_87: mov rax, 87 \ syscall \ ret
lnx_syscall_88: mov rax, 88 \ syscall \ ret
lnx_syscall_89: mov rax, 89 \ syscall \ ret
lnx_syscall_90: mov rax, 90 \ syscall \ ret
lnx_syscall_91: mov rax, 91 \ syscall \ ret
lnx_syscall_92: mov rax, 92 \ syscall \ ret
lnx_syscall_93: mov rax, 93 \ syscall \ ret
lnx_syscall_94: mov rax, 94 \ syscall \ ret
lnx_syscall_95: mov rax, 95 \ syscall \ ret
lnx_syscall_96: mov rax, 96 \ syscall \ ret
lnx_syscall_97: mov rax, 97 \ syscall \ ret
lnx_syscall_98: mov rax, 98 \ syscall \ ret
lnx_syscall_99: mov rax, 99 \ syscall \ ret
lnx_syscall_100: mov rax, 100 \ syscall \ ret

lnx_init_cpu: ret
lnx_init_mmu: ret
lnx_init_pci: ret
lnx_init_usb: ret
lnx_init_video: ret
lnx_init_audio: ret
lnx_init_network: ret
lnx_init_input: ret

section .data
    LNX_VERSION db "LNX_MEGA_V1", 0
    LNX_AUTHOR  db "Dragon_SCP", 0

section .bss
    LNX_STACK_BASE resb 65536
    LNX_HEAP_BASE  resb 1048576
