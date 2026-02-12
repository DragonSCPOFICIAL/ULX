; =============================================================================
; LNX Syscall Layer - Syscalls diretas do Linux sem libc
; Implementação 100% nativa usando instrução syscall
; =============================================================================

section .text

; =============================================================================
; SYSCALLS BÁSICAS DE ARQUIVO
; =============================================================================

; -----------------------------------------------------------------------------
; sys_read - Ler de arquivo
; Input:  rdi = fd, rsi = buf, rdx = count
; Output: rax = bytes lidos ou -errno
; -----------------------------------------------------------------------------
global lnx_read
lnx_read:
    mov rax, 0          ; __NR_read
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_write - Escrever em arquivo
; Input:  rdi = fd, rsi = buf, rdx = count
; Output: rax = bytes escritos ou -errno
; -----------------------------------------------------------------------------
global lnx_write
lnx_write:
    mov rax, 1          ; __NR_write
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_open - Abrir arquivo
; Input:  rdi = pathname, rsi = flags, rdx = mode
; Output: rax = fd ou -errno
; -----------------------------------------------------------------------------
global lnx_open
lnx_open:
    mov rax, 2          ; __NR_open
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_close - Fechar arquivo
; Input:  rdi = fd
; Output: rax = 0 ou -errno
; -----------------------------------------------------------------------------
global lnx_close
lnx_close:
    mov rax, 3          ; __NR_close
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_stat - Obter informações de arquivo
; Input:  rdi = pathname, rsi = statbuf
; Output: rax = 0 ou -errno
; -----------------------------------------------------------------------------
global lnx_stat
lnx_stat:
    mov rax, 4          ; __NR_stat
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_fstat - Obter informações de arquivo por fd
; Input:  rdi = fd, rsi = statbuf
; Output: rax = 0 ou -errno
; -----------------------------------------------------------------------------
global lnx_fstat
lnx_fstat:
    mov rax, 5          ; __NR_fstat
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_lstat - Obter informações de symlink
; Input:  rdi = pathname, rsi = statbuf
; Output: rax = 0 ou -errno
; -----------------------------------------------------------------------------
global lnx_lstat
lnx_lstat:
    mov rax, 6          ; __NR_lstat
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_poll - Esperar eventos em file descriptors
; Input:  rdi = fds, rsi = nfds, rdx = timeout
; Output: rax = número de fds prontos ou -errno
; -----------------------------------------------------------------------------
global lnx_poll
lnx_poll:
    mov rax, 7          ; __NR_poll
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_lseek - Reposicionar offset de arquivo
; Input:  rdi = fd, rsi = offset, rdx = whence
; Output: rax = novo offset ou -errno
; -----------------------------------------------------------------------------
global lnx_lseek
lnx_lseek:
    mov rax, 8          ; __NR_lseek
    syscall
    ret

; =============================================================================
; SYSCALLS DE MEMÓRIA
; =============================================================================

; -----------------------------------------------------------------------------
; sys_mmap - Mapear memória
; Input:  rdi = addr, rsi = length, rdx = prot
;         r10 = flags, r8 = fd, r9 = offset
; Output: rax = pointer ou -errno
; -----------------------------------------------------------------------------
global lnx_mmap
lnx_mmap:
    mov rax, 9          ; __NR_mmap
    mov r10, rcx        ; flags vai em r10 (convenção x86-64)
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_mprotect - Alterar proteção de memória
; Input:  rdi = addr, rsi = len, rdx = prot
; Output: rax = 0 ou -errno
; -----------------------------------------------------------------------------
global lnx_mprotect
lnx_mprotect:
    mov rax, 10         ; __NR_mprotect
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_munmap - Desmapear memória
; Input:  rdi = addr, rsi = length
; Output: rax = 0 ou -errno
; -----------------------------------------------------------------------------
global lnx_munmap
lnx_munmap:
    mov rax, 11         ; __NR_munmap
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_brk - Alterar tamanho do heap
; Input:  rdi = brk (0 para obter valor atual)
; Output: rax = novo brk ou -errno
; -----------------------------------------------------------------------------
global lnx_brk
lnx_brk:
    mov rax, 12         ; __NR_brk
    syscall
    ret

; =============================================================================
; SYSCALLS DE PROCESSO
; =============================================================================

; -----------------------------------------------------------------------------
; sys_exit - Terminar processo
; Input:  rdi = error_code
; Output: Não retorna
; -----------------------------------------------------------------------------
global lnx_exit
lnx_exit:
    mov rax, 60         ; __NR_exit
    syscall
    ; Não retorna

; -----------------------------------------------------------------------------
; sys_exit_group - Terminar todos os threads
; Input:  rdi = error_code
; Output: Não retorna
; -----------------------------------------------------------------------------
global lnx_exit_group
lnx_exit_group:
    mov rax, 231        ; __NR_exit_group
    syscall
    ; Não retorna

; -----------------------------------------------------------------------------
; sys_fork - Criar novo processo
; Input:  Nenhum
; Output: rax = 0 (filho), pid (pai), ou -errno
; -----------------------------------------------------------------------------
global lnx_fork
lnx_fork:
    mov rax, 57         ; __NR_fork
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_vfork - Criar novo processo (compartilha memória)
; Input:  Nenhum
; Output: rax = 0 (filho), pid (pai), ou -errno
; -----------------------------------------------------------------------------
global lnx_vfork
lnx_vfork:
    mov rax, 58         ; __NR_vfork
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_execve - Executar programa
; Input:  rdi = filename, rsi = argv, rdx = envp
; Output: rax = -errno (se falhar)
; -----------------------------------------------------------------------------
global lnx_execve
lnx_execve:
    mov rax, 59         ; __NR_execve
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_wait4 - Esperar por mudança de estado do processo
; Input:  rdi = pid, rsi = wstatus, rdx = options, r10 = rusage
; Output: rax = pid ou -errno
; -----------------------------------------------------------------------------
global lnx_wait4
lnx_wait4:
    mov rax, 61         ; __NR_wait4
    mov r10, rcx
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_kill - Enviar sinal para processo
; Input:  rdi = pid, rsi = sig
; Output: rax = 0 ou -errno
; -----------------------------------------------------------------------------
global lnx_kill
lnx_kill:
    mov rax, 62         ; __NR_kill
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_getpid - Obter PID
; Input:  Nenhum
; Output: rax = pid
; -----------------------------------------------------------------------------
global lnx_getpid
lnx_getpid:
    mov rax, 39         ; __NR_getpid
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_getppid - Obter PPID
; Input:  Nenhum
; Output: rax = ppid
; -----------------------------------------------------------------------------
global lnx_getppid
lnx_getppid:
    mov rax, 110        ; __NR_getppid
    syscall
    ret

; =============================================================================
; SYSCALLS DE SOCKET
; =============================================================================

; -----------------------------------------------------------------------------
; sys_socket - Criar socket
; Input:  rdi = domain, rsi = type, rdx = protocol
; Output: rax = fd ou -errno
; -----------------------------------------------------------------------------
global lnx_socket
lnx_socket:
    mov rax, 41         ; __NR_socket
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_bind - Bind socket
; Input:  rdi = sockfd, rsi = addr, rdx = addrlen
; Output: rax = 0 ou -errno
; -----------------------------------------------------------------------------
global lnx_bind
lnx_bind:
    mov rax, 49         ; __NR_bind
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_listen - Listen socket
; Input:  rdi = sockfd, rsi = backlog
; Output: rax = 0 ou -errno
; -----------------------------------------------------------------------------
global lnx_listen
lnx_listen:
    mov rax, 50         ; __NR_listen
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_accept - Accept connection
; Input:  rdi = sockfd, rsi = addr, rdx = addrlen
; Output: rax = novo fd ou -errno
; -----------------------------------------------------------------------------
global lnx_accept
lnx_accept:
    mov rax, 43         ; __NR_accept
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_connect - Connect socket
; Input:  rdi = sockfd, rsi = addr, rdx = addrlen
; Output: rax = 0 ou -errno
; -----------------------------------------------------------------------------
global lnx_connect
lnx_connect:
    mov rax, 42         ; __NR_connect
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_sendto - Enviar dados
; Input:  rdi = sockfd, rsi = buf, rdx = len
;         r10 = flags, r8 = dest_addr, r9 = addrlen
; Output: rax = bytes enviados ou -errno
; -----------------------------------------------------------------------------
global lnx_sendto
lnx_sendto:
    mov rax, 44         ; __NR_sendto
    mov r10, rcx
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_recvfrom - Receber dados
; Input:  rdi = sockfd, rsi = buf, rdx = len
;         r10 = flags, r8 = src_addr, r9 = addrlen
; Output: rax = bytes recebidos ou -errno
; -----------------------------------------------------------------------------
global lnx_recvfrom
lnx_recvfrom:
    mov rax, 45         ; __NR_recvfrom
    mov r10, rcx
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_shutdown - Shutdown socket
; Input:  rdi = sockfd, rsi = how
; Output: rax = 0 ou -errno
; -----------------------------------------------------------------------------
global lnx_shutdown
lnx_shutdown:
    mov rax, 48         ; __NR_shutdown
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_setsockopt - Set socket options
; Input:  rdi = sockfd, rsi = level, rdx = optname
;         r10 = optval, r8 = optlen
; Output: rax = 0 ou -errno
; -----------------------------------------------------------------------------
global lnx_setsockopt
lnx_setsockopt:
    mov rax, 54         ; __NR_setsockopt
    mov r10, rcx
    syscall
    ret

; =============================================================================
; SYSCALLS DE TEMPO
; =============================================================================

; -----------------------------------------------------------------------------
; sys_time - Obter tempo em segundos
; Input:  rdi = tloc (pode ser NULL)
; Output: rax = tempo em segundos
; -----------------------------------------------------------------------------
global lnx_time
lnx_time:
    mov rax, 201        ; __NR_time
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_gettimeofday - Obter tempo com microsegundos
; Input:  rdi = tv, rsi = tz
; Output: rax = 0 ou -errno
; -----------------------------------------------------------------------------
global lnx_gettimeofday
lnx_gettimeofday:
    mov rax, 96         ; __NR_gettimeofday
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_clock_gettime - Obter tempo de clock específico
; Input:  rdi = which_clock, rsi = tp
; Output: rax = 0 ou -errno
; -----------------------------------------------------------------------------
global lnx_clock_gettime
lnx_clock_gettime:
    mov rax, 228        ; __NR_clock_gettime
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_nanosleep - Dormir por tempo específico
; Input:  rdi = req, rsi = rem
; Output: rax = 0 ou -errno
; -----------------------------------------------------------------------------
global lnx_nanosleep
lnx_nanosleep:
    mov rax, 35         ; __NR_nanosleep
    syscall
    ret

; =============================================================================
; SYSCALLS DE DIRETÓRIO
; =============================================================================

; -----------------------------------------------------------------------------
; sys_getcwd - Obter diretório atual
; Input:  rdi = buf, rsi = size
; Output: rax = pointer para buf ou -errno
; -----------------------------------------------------------------------------
global lnx_getcwd
lnx_getcwd:
    mov rax, 79         ; __NR_getcwd
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_chdir - Mudar diretório
; Input:  rdi = path
; Output: rax = 0 ou -errno
; -----------------------------------------------------------------------------
global lnx_chdir
lnx_chdir:
    mov rax, 80         ; __NR_chdir
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_mkdir - Criar diretório
; Input:  rdi = pathname, rsi = mode
; Output: rax = 0 ou -errno
; -----------------------------------------------------------------------------
global lnx_mkdir
lnx_mkdir:
    mov rax, 83         ; __NR_mkdir
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_rmdir - Remover diretório
; Input:  rdi = pathname
; Output: rax = 0 ou -errno
; -----------------------------------------------------------------------------
global lnx_rmdir
lnx_rmdir:
    mov rax, 84         ; __NR_rmdir
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_getdents64 - Ler entradas de diretório
; Input:  rdi = fd, rsi = dirp, rdx = count
; Output: rax = bytes lidos ou -errno
; -----------------------------------------------------------------------------
global lnx_getdents64
lnx_getdents64:
    mov rax, 217        ; __NR_getdents64
    syscall
    ret

; =============================================================================
; SYSCALLS DE SINAL
; =============================================================================

; -----------------------------------------------------------------------------
; sys_rt_sigaction - Configurar handler de sinal
; Input:  rdi = sig, rsi = act, rdx = oact, r10 = sigsetsize
; Output: rax = 0 ou -errno
; -----------------------------------------------------------------------------
global lnx_rt_sigaction
lnx_rt_sigaction:
    mov rax, 13         ; __NR_rt_sigaction
    mov r10, rcx
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_rt_sigprocmask - Manipular máscara de sinais
; Input:  rdi = how, rsi = set, rdx = oset, r10 = sigsetsize
; Output: rax = 0 ou -errno
; -----------------------------------------------------------------------------
global lnx_rt_sigprocmask
lnx_rt_sigprocmask:
    mov rax, 14         ; __NR_rt_sigprocmask
    mov r10, rcx
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_sigreturn - Retornar de handler de sinal
; Input:  Nenhum (contexto na stack)
; Output: Não retorna normalmente
; -----------------------------------------------------------------------------
global lnx_sigreturn
lnx_sigreturn:
    mov rax, 15         ; __NR_rt_sigreturn
    syscall
    ret

; =============================================================================
; SYSCALLS DE THREAD
; =============================================================================

; -----------------------------------------------------------------------------
; sys_clone - Criar thread/processo
; Input:  rdi = flags, rsi = child_stack, rdx = ptid, r10 = ctid, r8 = tls
; Output: rax = tid ou -errno
; -----------------------------------------------------------------------------
global lnx_clone
lnx_clone:
    mov rax, 56         ; __NR_clone
    mov r10, rcx
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_set_tid_address - Setar endereço de tid
; Input:  rdi = tidptr
; Output: rax = tid
; -----------------------------------------------------------------------------
global lnx_set_tid_address
lnx_set_tid_address:
    mov rax, 218        ; __NR_set_tid_address
    syscall
    ret

; -----------------------------------------------------------------------------
; sys_futex - Operações futex (sincronização)
; Input:  rdi = uaddr, rsi = futex_op, rdx = val
;         r10 = timeout, r8 = uaddr2, r9 = val3
; Output: rax = valor ou -errno
; -----------------------------------------------------------------------------
global lnx_futex
lnx_futex:
    mov rax, 202        ; __NR_futex
    mov r10, rcx
    syscall
    ret

; =============================================================================
; CONSTANTES DE SYSCALLS (para referência)
; =============================================================================

; Números de syscalls x86-64 Linux
%define __NR_read              0
%define __NR_write             1
%define __NR_open              2
%define __NR_close             3
%define __NR_stat              4
%define __NR_fstat             5
%define __NR_lstat             6
%define __NR_poll              7
%define __NR_lseek             8
%define __NR_mmap              9
%define __NR_mprotect         10
%define __NR_munmap           11
%define __NR_brk              12
%define __NR_rt_sigaction     13
%define __NR_rt_sigprocmask   14
%define __NR_rt_sigreturn     15
%define __NR_ioctl            16
%define __NR_pread64          17
%define __NR_pwrite64         18
%define __NR_readv            19
%define __NR_writev           20
%define __NR_access           21
%define __NR_pipe             22
%define __NR_select           23
%define __NR_sched_yield      24
%define __NR_mremap           25
%define __NR_msync            26
%define __NR_mincore          27
%define __NR_madvise          28
%define __NR_shmget           29
%define __NR_shmat            30
%define __NR_shmctl           31
%define __NR_dup              32
%define __NR_dup2             33
%define __NR_pause            34
%define __NR_nanosleep        35
%define __NR_getitimer        36
%define __NR_alarm            37
%define __NR_setitimer        38
%define __NR_getpid           39
%define __NR_sendfile         40
%define __NR_socket           41
%define __NR_connect          42
%define __NR_accept           43
%define __NR_sendto           44
%define __NR_recvfrom         45
%define __NR_sendmsg          46
%define __NR_recvmsg          47
%define __NR_shutdown         48
%define __NR_bind             49
%define __NR_listen           50
%define __NR_getsockname      51
%define __NR_getpeername      52
%define __NR_socketpair       53
%define __NR_setsockopt       54
%define __NR_getsockopt       55
%define __NR_clone            56
%define __NR_fork             57
%define __NR_vfork            58
%define __NR_execve           59
%define __NR_exit             60
%define __NR_wait4            61
%define __NR_kill             62
%define __NR_uname            63
%define __NR_semget           64
%define __NR_semop            65
%define __NR_semctl           66
%define __NR_shmdt            67
%define __NR_msgget           68
%define __NR_msgsnd           69
%define __NR_msgrcv           70
%define __NR_msgctl           71
%define __NR_fcntl            72
%define __NR_flock            73
%define __NR_fsync            74
%define __NR_fdatasync        75
%define __NR_truncate         76
%define __NR_ftruncate        77
%define __NR_getdents         78
%define __NR_getcwd           79
%define __NR_chdir            80
%define __NR_fchdir           81
%define __NR_rename           82
%define __NR_mkdir            83
%define __NR_rmdir            84
%define __NR_creat            85
%define __NR_link             86
%define __NR_unlink           87
%define __NR_symlink          88
%define __NR_readlink         89
%define __NR_chmod            90
%define __NR_fchmod           91
%define __NR_chown            92
%define __NR_fchown           93
%define __NR_lchown           94
%define __NR_umask            95
%define __NR_gettimeofday     96
%define __NR_getrlimit        97
%define __NR_getrusage        98
%define __NR_sysinfo          99
%define __NR_times           100
%define __NR_ptrace          101
%define __NR_getuid          102
%define __NR_syslog          103
%define __NR_getgid          104
%define __NR_setuid          105
%define __NR_setgid          106
%define __NR_geteuid         107
%define __NR_getegid         108
%define __NR_setpgid         109
%define __NR_getppid         110
%define __NR_getpgrp         111
%define __NR_setsid          112
%define __NR_setreuid        113
%define __NR_setregid        114
%define __NR_getgroups       115
%define __NR_setgroups       116
%define __NR_setresuid       117
%define __NR_getresuid       118
%define __NR_setresgid       119
%define __NR_getresgid       120
%define __NR_getpgid         121
%define __NR_setfsuid        122
%define __NR_setfsgid        123
%define __NR_getsid          124
%define __NR_capget          125
%define __NR_capset          126
%define __NR_rt_sigpending   127
%define __NR_rt_sigtimedwait 128
%define __NR_rt_sigqueueinfo 129
%define __NR_rt_sigsuspend   130
%define __NR_sigaltstack     131
%define __NR_utime           132
%define __NR_mknod           133
%define __NR_uselib          134
%define __NR_personality     135
%define __NR_ustat           136
%define __NR_statfs          137
%define __NR_fstatfs         138
%define __NR_sysfs           139
%define __NR_getpriority     140
%define __NR_setpriority     141
%define __NR_sched_setparam  142
%define __NR_sched_getparam  143
%define __NR_sched_setscheduler  144
%define __NR_sched_getscheduler  145
%define __NR_sched_get_priority_max  146
%define __NR_sched_get_priority_min  147
%define __NR_sched_rr_get_interval   148
%define __NR_mlock           149
%define __NR_munlock         150
%define __NR_mlockall        151
%define __NR_munlockall      152
%define __NR_vhangup         153
%define __NR_modify_ldt      154
%define __NR_pivot_root      155
%define __NR__sysctl         156
%define __NR_prctl           157
%define __NR_arch_prctl      158
%define __NR_adjtimex        159
%define __NR_setrlimit       160
%define __NR_chroot          161
%define __NR_sync            162
%define __NR_acct            163
%define __NR_settimeofday    164
%define __NR_mount           165
%define __NR_umount2         166
%define __NR_swapon          167
%define __NR_swapoff         168
%define __NR_reboot          169
%define __NR_sethostname     170
%define __NR_setdomainname   171
%define __NR_iopl            172
%define __NR_ioperm          173
%define __NR_create_module   174
%define __NR_init_module     175
%define __NR_delete_module   176
%define __NR_get_kernel_syms 177
%define __NR_query_module    178
%define __NR_quotactl        179
%define __NR_nfsservctl      180
%define __NR_getpmsg         181
%define __NR_putpmsg         182
%define __NR_afs_syscall     183
%define __NR_tuxcall         184
%define __NR_security        185
%define __NR_gettid          186
%define __NR_readahead       187
%define __NR_setxattr        188
%define __NR_lsetxattr       189
%define __NR_fsetxattr       190
%define __NR_getxattr        191
%define __NR_lgetxattr       192
%define __NR_fgetxattr       193
%define __NR_listxattr       194
%define __NR_llistxattr      195
%define __NR_flistxattr      196
%define __NR_removexattr     197
%define __NR_lremovexattr    198
%define __NR_fremovexattr    199
%define __NR_tkill           200
%define __NR_time            201
%define __NR_futex           202
%define __NR_sched_setaffinity  203
%define __NR_sched_getaffinity  204
%define __NR_set_thread_area    205
%define __NR_io_setup        206
%define __NR_io_destroy      207
%define __NR_io_getevents    208
%define __NR_io_submit       209
%define __NR_io_cancel       210
%define __NR_get_thread_area    211
%define __NR_lookup_dcookie  212
%define __NR_epoll_create    213
%define __NR_epoll_ctl_old   214
%define __NR_epoll_wait_old  215
%define __NR_remap_file_pages   216
%define __NR_getdents64      217
%define __NR_set_tid_address    218
%define __NR_restart_syscall    219
%define __NR_semtimedop      220
%define __NR_fadvise64       221
%define __NR_timer_create    222
%define __NR_timer_settime   223
%define __NR_timer_gettime   224
%define __NR_timer_getoverrun   225
%define __NR_timer_delete    226
%define __NR_clock_settime   227
%define __NR_clock_gettime   228
%define __NR_clock_getres    229
%define __NR_clock_nanosleep    230
%define __NR_exit_group      231
%define __NR_epoll_wait      232
%define __NR_epoll_ctl       233
%define __NR_tgkill          234
%define __NR_utimes          235
%define __NR_vserver         236
%define __NR_mbind           237
%define __NR_set_mempolicy   238
%define __NR_get_mempolicy   239
%define __NR_mq_open         240
%define __NR_mq_unlink       241
%define __NR_mq_timedsend    242
%define __NR_mq_timedreceive    243
%define __NR_mq_notify       244
%define __NR_mq_getsetattr   245
%define __NR_kexec_load      246
%define __NR_waitid          247
%define __NR_add_key         248
%define __NR_request_key     249
%define __NR_keyctl          250
%define __NR_ioprio_set      251
%define __NR_ioprio_get      252
%define __NR_inotify_init    253
%define __NR_inotify_add_watch  254
%define __NR_inotify_rm_watch   255
%define __NR_migrate_pages   256
%define __NR_openat          257
%define __NR_mkdirat         258
%define __NR_mknodat         259
%define __NR_fchownat        260
%define __NR_futimesat       261
%define __NR_newfstatat      262
%define __NR_unlinkat        263
%define __NR_renameat        264
%define __NR_linkat          265
%define __NR_symlinkat       266
%define __NR_readlinkat      267
%define __NR_fchmodat        268
%define __NR_faccessat       269
%define __NR_pselect6        270
%define __NR_ppoll           271
%define __NR_unshare         272
%define __NR_set_robust_list    273
%define __NR_get_robust_list    274
%define __NR_splice          275
%define __NR_tee             276
%define __NR_sync_file_range    277
%define __NR_vmsplice        278
%define __NR_move_pages      279
%define __NR_utimensat       280
%define __NR_epoll_pwait     281
%define __NR_signalfd        282
%define __NR_timerfd_create  283
%define __NR_eventfd         284
%define __NR_fallocate       285
%define __NR_timerfd_settime    286
%define __NR_timerfd_gettime    287
%define __NR_accept4         288
%define __NR_signalfd4       289
%define __NR_eventfd2        290
%define __NR_epoll_create1   291
%define __NR_dup3            292
%define __NR_pipe2           293
%define __NR_inotify_init1   294
%define __NR_preadv          295
%define __NR_pwritev         296
%define __NR_rt_tgsigqueueinfo  297
%define __NR_perf_event_open    298
%define __NR_recvmmsg        299
%define __NR_fanotify_init   300
%define __NR_fanotify_mark   301
%define __NR_prlimit64       302
%define __NR_name_to_handle_at  303
%define __NR_open_by_handle_at  304
%define __NR_clock_adjtime   305
%define __NR_syncfs          306
%define __NR_sendmmsg        307
%define __NR_setns           308
%define __NR_getcpu          309
%define __NR_process_vm_readv   310
%define __NR_process_vm_writev  311
%define __NR_kcmp            312
%define __NR_finit_module    313
%define __NR_sched_setattr   314
%define __NR_sched_getattr   315
%define __NR_renameat2       316
%define __NR_seccomp         317
%define __NR_getrandom       318
%define __NR_memfd_create    319
%define __NR_kexec_file_load    320
%define __NR_bpf             321
%define __NR_execveat        322
%define __NR_userfaultfd     323
%define __NR_membarrier      324
%define __NR_mlock2          325
%define __NR_copy_file_range    326
%define __NR_preadv2         327
%define __NR_pwritev2        328
%define __NR_pkey_mprotect   329
%define __NR_pkey_alloc      330
%define __NR_pkey_free       331
%define __NR_statx           332
%define __NR_io_pgetevents   333
%define __NR_rseq            334
%define __NR_pidfd_send_signal  424
%define __NR_io_uring_setup  425
%define __NR_io_uring_enter  426
%define __NR_io_uring_register  427
%define __NR_open_tree       428
%define __NR_move_mount      429
%define __NR_fsopen          430
%define __NR_fsconfig        431
%define __NR_fsmount         432
%define __NR_fspick          433
%define __NR_pidfd_open      434
%define __NR_clone3          435
%define __NR_openat2         437
%define __NR_pidfd_getfd     438
%define __NR_faccessat2      439
%define __NR_process_madvise    440
%define __NR_epoll_pwait2    441
%define __NR_mount_setattr   442
%define __NR_quotactl_fd     443
%define __NR_landlock_create_ruleset  444
%define __NR_landlock_add_rule  445
%define __NR_landlock_restrict_self  446
%define __NR_memfd_secret    447
%define __NR_process_mrelease   448
