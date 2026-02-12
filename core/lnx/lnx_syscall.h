/* =============================================================================
 * LNX Syscall Header - Interface C para syscalls diretas do Linux
 * ============================================================================= */

#ifndef LNX_SYSCALL_H
#define LNX_SYSCALL_H

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* =============================================================================
 * SYSCALLS BÁSICAS DE ARQUIVO
 * ============================================================================= */

extern long lnx_read(int fd, void *buf, size_t count);
extern long lnx_write(int fd, const void *buf, size_t count);
extern long lnx_open(const char *pathname, int flags, int mode);
extern long lnx_close(int fd);
extern long lnx_stat(const char *pathname, void *statbuf);
extern long lnx_fstat(int fd, void *statbuf);
extern long lnx_lstat(const char *pathname, void *statbuf);
extern long lnx_poll(void *fds, unsigned long nfds, int timeout);
extern long lnx_lseek(int fd, long offset, int whence);

/* =============================================================================
 * SYSCALLS DE MEMÓRIA
 * ============================================================================= */

extern long lnx_mmap(void *addr, size_t length, int prot, int flags, int fd, long offset);
extern long lnx_mprotect(void *addr, size_t len, int prot);
extern long lnx_munmap(void *addr, size_t length);
extern long lnx_brk(void *addr);

/* =============================================================================
 * SYSCALLS DE PROCESSO
 * ============================================================================= */

extern long lnx_exit(int error_code);
extern long lnx_exit_group(int error_code);
extern long lnx_fork(void);
extern long lnx_vfork(void);
extern long lnx_execve(const char *filename, char *const argv[], char *const envp[]);
extern long lnx_wait4(int pid, int *wstatus, int options, void *rusage);
extern long lnx_kill(int pid, int sig);
extern long lnx_getpid(void);
extern long lnx_getppid(void);

/* =============================================================================
 * SYSCALLS DE SOCKET
 * ============================================================================= */

extern long lnx_socket(int domain, int type, int protocol);
extern long lnx_bind(int sockfd, const void *addr, unsigned int addrlen);
extern long lnx_listen(int sockfd, int backlog);
extern long lnx_accept(int sockfd, void *addr, unsigned int *addrlen);
extern long lnx_connect(int sockfd, const void *addr, unsigned int addrlen);
extern long lnx_sendto(int sockfd, const void *buf, size_t len, int flags,
                       const void *dest_addr, unsigned int addrlen);
extern long lnx_recvfrom(int sockfd, void *buf, size_t len, int flags,
                         void *src_addr, unsigned int *addrlen);
extern long lnx_shutdown(int sockfd, int how);
extern long lnx_setsockopt(int sockfd, int level, int optname,
                           const void *optval, unsigned int optlen);

/* =============================================================================
 * SYSCALLS DE TEMPO
 * ============================================================================= */

extern long lnx_time(long *tloc);
extern long lnx_gettimeofday(void *tv, void *tz);
extern long lnx_clock_gettime(int which_clock, void *tp);
extern long lnx_nanosleep(const void *req, void *rem);

/* =============================================================================
 * SYSCALLS DE DIRETÓRIO
 * ============================================================================= */

extern long lnx_getcwd(char *buf, size_t size);
extern long lnx_chdir(const char *path);
extern long lnx_mkdir(const char *pathname, int mode);
extern long lnx_rmdir(const char *pathname);
extern long lnx_getdents64(int fd, void *dirp, size_t count);

/* =============================================================================
 * SYSCALLS DE SINAL
 * ============================================================================= */

extern long lnx_rt_sigaction(int sig, const void *act, void *oact, size_t sigsetsize);
extern long lnx_rt_sigprocmask(int how, const void *set, void *oset, size_t sigsetsize);
extern long lnx_sigreturn(void);

/* =============================================================================
 * SYSCALLS DE THREAD
 * ============================================================================= */

extern long lnx_clone(unsigned long flags, void *child_stack, void *ptid,
                      void *ctid, void *tls);
extern long lnx_set_tid_address(int *tidptr);
extern long lnx_futex(int *uaddr, int futex_op, int val,
                      const void *timeout, int *uaddr2, int val3);

/* =============================================================================
 * CONSTANTES
 * ============================================================================= */

/* Flags para open */
#define LNX_O_RDONLY        00000000
#define LNX_O_WRONLY        00000001
#define LNX_O_RDWR          00000002
#define LNX_O_CREAT         00000100
#define LNX_O_EXCL          00000200
#define LNX_O_NOCTTY        00000400
#define LNX_O_TRUNC         00001000
#define LNX_O_APPEND        00002000
#define LNX_O_NONBLOCK      00004000
#define LNX_O_DSYNC         00010000
#define LNX_O_ASYNC         00020000
#define LNX_O_DIRECT        00040000
#define LNX_O_LARGEFILE     00100000
#define LNX_O_DIRECTORY     00200000
#define LNX_O_NOFOLLOW      00400000
#define LNX_O_NOATIME       01000000
#define LNX_O_CLOEXEC       02000000
#define LNX_O_SYNC          04010000
#define LNX_O_PATH          010000000

/* Modos de arquivo */
#define LNX_S_IRWXU  00700
#define LNX_S_IRUSR  00400
#define LNX_S_IWUSR  00200
#define LNX_S_IXUSR  00100
#define LNX_S_IRWXG  00070
#define LNX_S_IRGRP  00040
#define LNX_S_IWGRP  00020
#define LNX_S_IXGRP  00010
#define LNX_S_IRWXO  00007
#define LNX_S_IROTH  00004
#define LNX_S_IWOTH  00002
#define LNX_S_IXOTH  00001

/* Proteção de memória para mmap */
#define LNX_PROT_READ       0x1
#define LNX_PROT_WRITE      0x2
#define LNX_PROT_EXEC       0x4
#define LNX_PROT_NONE       0x0
#define LNX_PROT_GROWSDOWN  0x01000000
#define LNX_PROT_GROWSUP    0x02000000

/* Flags para mmap */
#define LNX_MAP_SHARED      0x01
#define LNX_MAP_PRIVATE     0x02
#define LNX_MAP_FIXED       0x10
#define LNX_MAP_ANONYMOUS   0x20
#define LNX_MAP_GROWSDOWN   0x00100
#define LNX_MAP_DENYWRITE   0x00800
#define LNX_MAP_EXECUTABLE  0x01000
#define LNX_MAP_LOCKED      0x02000
#define LNX_MAP_NORESERVE   0x04000
#define LNX_MAP_POPULATE    0x08000
#define LNX_MAP_NONBLOCK    0x10000
#define LNX_MAP_STACK       0x20000
#define LNX_MAP_HUGETLB     0x40000
#define LNX_MAP_SYNC        0x80000
#define LNX_MAP_FIXED_NOREPLACE 0x100000

/* Domínios de socket */
#define LNX_AF_UNIX         1
#define LNX_AF_INET         2
#define LNX_AF_INET6        10
#define LNX_AF_NETLINK      16

/* Tipos de socket */
#define LNX_SOCK_STREAM     1
#define LNX_SOCK_DGRAM      2
#define LNX_SOCK_RAW        3
#define LNX_SOCK_RDM        4
#define LNX_SOCK_SEQPACKET  5
#define LNX_SOCK_DCCP       6
#define LNX_SOCK_PACKET     10
#define LNX_SOCK_NONBLOCK   00004000
#define LNX_SOCK_CLOEXEC    02000000

/* Syscalls numbers (x86-64) */
#define LNX_NR_read              0
#define LNX_NR_write             1
#define LNX_NR_open              2
#define LNX_NR_close             3
#define LNX_NR_stat              4
#define LNX_NR_fstat             5
#define LNX_NR_lstat             6
#define LNX_NR_poll              7
#define LNX_NR_lseek             8
#define LNX_NR_mmap              9
#define LNX_NR_mprotect         10
#define LNX_NR_munmap           11
#define LNX_NR_brk              12
#define LNX_NR_rt_sigaction     13
#define LNX_NR_rt_sigprocmask   14
#define LNX_NR_rt_sigreturn     15
#define LNX_NR_ioctl            16
#define LNX_NR_pread64          17
#define LNX_NR_pwrite64         18
#define LNX_NR_readv            19
#define LNX_NR_writev           20
#define LNX_NR_access           21
#define LNX_NR_pipe             22
#define LNX_NR_select           23
#define LNX_NR_sched_yield      24
#define LNX_NR_mremap           25
#define LNX_NR_msync            26
#define LNX_NR_mincore          27
#define LNX_NR_madvise          28
#define LNX_NR_shmget           29
#define LNX_NR_shmat            30
#define LNX_NR_shmctl           31
#define LNX_NR_dup              32
#define LNX_NR_dup2             33
#define LNX_NR_pause            34
#define LNX_NR_nanosleep        35
#define LNX_NR_getitimer        36
#define LNX_NR_alarm            37
#define LNX_NR_setitimer        38
#define LNX_NR_getpid           39
#define LNX_NR_sendfile         40
#define LNX_NR_socket           41
#define LNX_NR_connect          42
#define LNX_NR_accept           43
#define LNX_NR_sendto           44
#define LNX_NR_recvfrom         45
#define LNX_NR_sendmsg          46
#define LNX_NR_recvmsg          47
#define LNX_NR_shutdown         48
#define LNX_NR_bind             49
#define LNX_NR_listen           50
#define LNX_NR_getsockname      51
#define LNX_NR_getpeername      52
#define LNX_NR_socketpair       53
#define LNX_NR_setsockopt       54
#define LNX_NR_getsockopt       55
#define LNX_NR_clone            56
#define LNX_NR_fork             57
#define LNX_NR_vfork            58
#define LNX_NR_execve           59
#define LNX_NR_exit             60
#define LNX_NR_wait4            61
#define LNX_NR_kill             62
#define LNX_NR_uname            63
#define LNX_NR_semget           64
#define LNX_NR_semop            65
#define LNX_NR_semctl           66
#define LNX_NR_shmdt            67
#define LNX_NR_msgget           68
#define LNX_NR_msgsnd           69
#define LNX_NR_msgrcv           70
#define LNX_NR_msgctl           71
#define LNX_NR_fcntl            72
#define LNX_NR_flock            73
#define LNX_NR_fsync            74
#define LNX_NR_fdatasync        75
#define LNX_NR_truncate         76
#define LNX_NR_ftruncate        77
#define LNX_NR_getdents         78
#define LNX_NR_getcwd           79
#define LNX_NR_chdir            80
#define LNX_NR_fchdir           81
#define LNX_NR_rename           82
#define LNX_NR_mkdir            83
#define LNX_NR_rmdir            84
#define LNX_NR_creat            85
#define LNX_NR_link             86
#define LNX_NR_unlink           87
#define LNX_NR_symlink          88
#define LNX_NR_readlink         89
#define LNX_NR_chmod            90
#define LNX_NR_fchmod           91
#define LNX_NR_chown            92
#define LNX_NR_fchown           93
#define LNX_NR_lchown           94
#define LNX_NR_umask            95
#define LNX_NR_gettimeofday     96
#define LNX_NR_getrlimit        97
#define LNX_NR_getrusage        98
#define LNX_NR_sysinfo          99
#define LNX_NR_times            100
#define LNX_NR_ptrace           101
#define LNX_NR_getuid           102
#define LNX_NR_syslog           103
#define LNX_NR_getgid           104
#define LNX_NR_setuid           105
#define LNX_NR_setgid           106
#define LNX_NR_geteuid          107
#define LNX_NR_getegid          108
#define LNX_NR_setpgid          109
#define LNX_NR_getppid          110
#define LNX_NR_getpgrp          111
#define LNX_NR_setsid           112
#define LNX_NR_setreuid         113
#define LNX_NR_setregid         114
#define LNX_NR_getgroups        115
#define LNX_NR_setgroups        116
#define LNX_NR_setresuid        117
#define LNX_NR_getresuid        118
#define LNX_NR_setresgid        119
#define LNX_NR_getresgid        120
#define LNX_NR_getpgid          121
#define LNX_NR_setfsuid         122
#define LNX_NR_setfsgid         123
#define LNX_NR_getsid           124
#define LNX_NR_capget           125
#define LNX_NR_capset           126
#define LNX_NR_rt_sigpending    127
#define LNX_NR_rt_sigtimedwait  128
#define LNX_NR_rt_sigqueueinfo  129
#define LNX_NR_rt_sigsuspend    130
#define LNX_NR_sigaltstack      131
#define LNX_NR_utime            132
#define LNX_NR_mknod            133
#define LNX_NR_uselib           134
#define LNX_NR_personality      135
#define LNX_NR_ustat            136
#define LNX_NR_statfs           137
#define LNX_NR_fstatfs          138
#define LNX_NR_sysfs            139
#define LNX_NR_getpriority      140
#define LNX_NR_setpriority      141
#define LNX_NR_sched_setparam   142
#define LNX_NR_sched_getparam   143
#define LNX_NR_sched_setscheduler   144
#define LNX_NR_sched_getscheduler   145
#define LNX_NR_sched_get_priority_max   146
#define LNX_NR_sched_get_priority_min   147
#define LNX_NR_sched_rr_get_interval    148
#define LNX_NR_mlock            149
#define LNX_NR_munlock          150
#define LNX_NR_mlockall         151
#define LNX_NR_munlockall       152
#define LNX_NR_vhangup          153
#define LNX_NR_modify_ldt       154
#define LNX_NR_pivot_root       155
#define LNX_NR__sysctl          156
#define LNX_NR_prctl            157
#define LNX_NR_arch_prctl       158
#define LNX_NR_adjtimex         159
#define LNX_NR_setrlimit        160
#define LNX_NR_chroot           161
#define LNX_NR_sync             162
#define LNX_NR_acct             163
#define LNX_NR_settimeofday     164
#define LNX_NR_mount            165
#define LNX_NR_umount2          166
#define LNX_NR_swapon           167
#define LNX_NR_swapoff          168
#define LNX_NR_reboot           169
#define LNX_NR_sethostname      170
#define LNX_NR_setdomainname    171
#define LNX_NR_iopl             172
#define LNX_NR_ioperm           173
#define LNX_NR_create_module    174
#define LNX_NR_init_module      175
#define LNX_NR_delete_module    176
#define LNX_NR_get_kernel_syms  177
#define LNX_NR_query_module     178
#define LNX_NR_quotactl         179
#define LNX_NR_nfsservctl       180
#define LNX_NR_getpmsg          181
#define LNX_NR_putpmsg          182
#define LNX_NR_afs_syscall      183
#define LNX_NR_tuxcall          184
#define LNX_NR_security         185
#define LNX_NR_gettid           186
#define LNX_NR_readahead        187
#define LNX_NR_setxattr         188
#define LNX_NR_lsetxattr        189
#define LNX_NR_fsetxattr        190
#define LNX_NR_getxattr         191
#define LNX_NR_lgetxattr        192
#define LNX_NR_fgetxattr        193
#define LNX_NR_listxattr        194
#define LNX_NR_llistxattr       195
#define LNX_NR_flistxattr       196
#define LNX_NR_removexattr      197
#define LNX_NR_lremovexattr     198
#define LNX_NR_fremovexattr     199
#define LNX_NR_tkill            200
#define LNX_NR_time             201
#define LNX_NR_futex            202
#define LNX_NR_sched_setaffinity    203
#define LNX_NR_sched_getaffinity    204
#define LNX_NR_set_thread_area      205
#define LNX_NR_io_setup         206
#define LNX_NR_io_destroy       207
#define LNX_NR_io_getevents     208
#define LNX_NR_io_submit        209
#define LNX_NR_io_cancel        210
#define LNX_NR_get_thread_area      211
#define LNX_NR_lookup_dcookie   212
#define LNX_NR_epoll_create     213
#define LNX_NR_epoll_ctl_old    214
#define LNX_NR_epoll_wait_old   215
#define LNX_NR_remap_file_pages 216
#define LNX_NR_getdents64       217
#define LNX_NR_set_tid_address  218
#define LNX_NR_restart_syscall  219
#define LNX_NR_semtimedop       220
#define LNX_NR_fadvise64        221
#define LNX_NR_timer_create     222
#define LNX_NR_timer_settime    223
#define LNX_NR_timer_gettime    224
#define LNX_NR_timer_getoverrun 225
#define LNX_NR_timer_delete     226
#define LNX_NR_clock_settime    227
#define LNX_NR_clock_gettime    228
#define LNX_NR_clock_getres     229
#define LNX_NR_clock_nanosleep  230
#define LNX_NR_exit_group       231
#define LNX_NR_epoll_wait       232
#define LNX_NR_epoll_ctl        233
#define LNX_NR_tgkill           234
#define LNX_NR_utimes           235
#define LNX_NR_vserver          236
#define LNX_NR_mbind            237
#define LNX_NR_set_mempolicy    238
#define LNX_NR_get_mempolicy    239
#define LNX_NR_mq_open          240
#define LNX_NR_mq_unlink        241
#define LNX_NR_mq_timedsend     242
#define LNX_NR_mq_timedreceive  243
#define LNX_NR_mq_notify        244
#define LNX_NR_mq_getsetattr    245
#define LNX_NR_kexec_load       246
#define LNX_NR_waitid           247
#define LNX_NR_add_key          248
#define LNX_NR_request_key      249
#define LNX_NR_keyctl           250
#define LNX_NR_ioprio_set       251
#define LNX_NR_ioprio_get       252
#define LNX_NR_inotify_init     253
#define LNX_NR_inotify_add_watch    254
#define LNX_NR_inotify_rm_watch 255
#define LNX_NR_migrate_pages    256
#define LNX_NR_openat           257
#define LNX_NR_mkdirat          258
#define LNX_NR_mknodat          259
#define LNX_NR_fchownat         260
#define LNX_NR_futimesat        261
#define LNX_NR_newfstatat       262
#define LNX_NR_unlinkat         263
#define LNX_NR_renameat         264
#define LNX_NR_linkat           265
#define LNX_NR_symlinkat        266
#define LNX_NR_readlinkat       267
#define LNX_NR_fchmodat         268
#define LNX_NR_faccessat        269
#define LNX_NR_pselect6         270
#define LNX_NR_ppoll            271
#define LNX_NR_unshare          272
#define LNX_NR_set_robust_list  273
#define LNX_NR_get_robust_list  274
#define LNX_NR_splice           275
#define LNX_NR_tee              276
#define LNX_NR_sync_file_range  277
#define LNX_NR_vmsplice         278
#define LNX_NR_move_pages       279
#define LNX_NR_utimensat        280
#define LNX_NR_epoll_pwait      281
#define LNX_NR_signalfd         282
#define LNX_NR_timerfd_create   283
#define LNX_NR_eventfd          284
#define LNX_NR_fallocate        285
#define LNX_NR_timerfd_settime  286
#define LNX_NR_timerfd_gettime  287
#define LNX_NR_accept4          288
#define LNX_NR_signalfd4        289
#define LNX_NR_eventfd2         290
#define LNX_NR_epoll_create1    291
#define LNX_NR_dup3             292
#define LNX_NR_pipe2            293
#define LNX_NR_inotify_init1    294
#define LNX_NR_preadv           295
#define LNX_NR_pwritev          296
#define LNX_NR_rt_tgsigqueueinfo    297
#define LNX_NR_perf_event_open  298
#define LNX_NR_recvmmsg         299
#define LNX_NR_fanotify_init    300
#define LNX_NR_fanotify_mark    301
#define LNX_NR_prlimit64        302
#define LNX_NR_name_to_handle_at    303
#define LNX_NR_open_by_handle_at    304
#define LNX_NR_clock_adjtime    305
#define LNX_NR_syncfs           306
#define LNX_NR_sendmmsg         307
#define LNX_NR_setns            308
#define LNX_NR_getcpu           309
#define LNX_NR_process_vm_readv 310
#define LNX_NR_process_vm_writev    311
#define LNX_NR_kcmp             312
#define LNX_NR_finit_module     313
#define LNX_NR_sched_setattr    314
#define LNX_NR_sched_getattr    315
#define LNX_NR_renameat2        316
#define LNX_NR_seccomp          317
#define LNX_NR_getrandom        318
#define LNX_NR_memfd_create     319
#define LNX_NR_kexec_file_load  320
#define LNX_NR_bpf              321
#define LNX_NR_execveat         322
#define LNX_NR_userfaultfd      323
#define LNX_NR_membarrier       324
#define LNX_NR_mlock2           325
#define LNX_NR_copy_file_range  326
#define LNX_NR_preadv2          327
#define LNX_NR_pwritev2         328
#define LNX_NR_pkey_mprotect    329
#define LNX_NR_pkey_alloc       330
#define LNX_NR_pkey_free        331
#define LNX_NR_statx            332
#define LNX_NR_io_pgetevents    333
#define LNX_NR_rseq             334

#ifdef __cplusplus
}
#endif

#endif /* LNX_SYSCALL_H */
