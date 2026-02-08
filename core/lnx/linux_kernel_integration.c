/*
 * LNX - Linux Kernel Integration Layer
 * 
 * Integração direta com syscalls do Linux kernel
 * Usa as mesmas estruturas e convenções do kernel
 * Máxima compatibilidade e performance
 */

#include <linux/types.h>
#include <linux/fs.h>
#include <linux/fcntl.h>
#include <linux/stat.h>
#include <linux/socket.h>
#include <linux/in.h>
#include <linux/errno.h>
#include <asm/unistd.h>
#include <asm/syscall.h>

#pragma GCC optimize("O3")
#pragma GCC target("native")

/* ===== SYSCALLS DIRETOS (x86-64) ===== */

/* Syscall 0: read */
static inline long syscall_read(int fd, void *buf, size_t count) {
    return syscall(__NR_read, fd, buf, count);
}

/* Syscall 1: write */
static inline long syscall_write(int fd, const void *buf, size_t count) {
    return syscall(__NR_write, fd, buf, count);
}

/* Syscall 2: open */
static inline long syscall_open(const char *pathname, int flags, mode_t mode) {
    return syscall(__NR_open, pathname, flags, mode);
}

/* Syscall 3: close */
static inline long syscall_close(int fd) {
    return syscall(__NR_close, fd);
}

/* Syscall 4: stat */
static inline long syscall_stat(const char *pathname, struct stat *statbuf) {
    return syscall(__NR_stat, pathname, statbuf);
}

/* Syscall 5: fstat */
static inline long syscall_fstat(int fd, struct stat *statbuf) {
    return syscall(__NR_fstat, fd, statbuf);
}

/* Syscall 6: lstat */
static inline long syscall_lstat(const char *pathname, struct stat *statbuf) {
    return syscall(__NR_lstat, pathname, statbuf);
}

/* Syscall 9: link */
static inline long syscall_link(const char *oldpath, const char *newpath) {
    return syscall(__NR_link, oldpath, newpath);
}

/* Syscall 10: unlink */
static inline long syscall_unlink(const char *pathname) {
    return syscall(__NR_unlink, pathname);
}

/* Syscall 11: execve */
static inline long syscall_execve(const char *filename, char *const argv[], char *const envp[]) {
    return syscall(__NR_execve, filename, argv, envp);
}

/* Syscall 12: chdir */
static inline long syscall_chdir(const char *path) {
    return syscall(__NR_chdir, path);
}

/* Syscall 13: time */
static inline long syscall_time(time_t *tloc) {
    return syscall(__NR_time, tloc);
}

/* Syscall 21: access */
static inline long syscall_access(const char *pathname, int mode) {
    return syscall(__NR_access, pathname, mode);
}

/* Syscall 33: dup2 */
static inline long syscall_dup2(int oldfd, int newfd) {
    return syscall(__NR_dup2, oldfd, newfd);
}

/* Syscall 36: ioctl */
static inline long syscall_ioctl(int fd, unsigned long request, ...) {
    // Implementação variável
    return -1;
}

/* Syscall 39: mkdir */
static inline long syscall_mkdir(const char *pathname, mode_t mode) {
    return syscall(__NR_mkdir, pathname, mode);
}

/* Syscall 40: rmdir */
static inline long syscall_rmdir(const char *pathname) {
    return syscall(__NR_rmdir, pathname);
}

/* Syscall 41: creat */
static inline long syscall_creat(const char *pathname, mode_t mode) {
    return syscall(__NR_creat, pathname, mode);
}

/* Syscall 42: link */
static inline long syscall_link_new(const char *oldpath, const char *newpath) {
    return syscall(__NR_link, oldpath, newpath);
}

/* Syscall 43: unlink */
static inline long syscall_unlink_new(const char *pathname) {
    return syscall(__NR_unlink, pathname);
}

/* Syscall 49: chown */
static inline long syscall_chown(const char *pathname, uid_t owner, gid_t group) {
    return syscall(__NR_chown, pathname, owner, group);
}

/* Syscall 51: acct */
static inline long syscall_acct(const char *filename) {
    return syscall(__NR_acct, filename);
}

/* Syscall 52: umount2 */
static inline long syscall_umount2(const char *target, int flags) {
    return syscall(__NR_umount2, target, flags);
}

/* Syscall 55: fcntl */
static inline long syscall_fcntl(int fd, int cmd, ...) {
    // Implementação variável
    return -1;
}

/* Syscall 57: setpgid */
static inline long syscall_setpgid(pid_t pid, pid_t pgid) {
    return syscall(__NR_setpgid, pid, pgid);
}

/* Syscall 60: umask */
static inline long syscall_umask(mode_t mask) {
    return syscall(__NR_umask, mask);
}

/* Syscall 63: getpriority */
static inline long syscall_getpriority(int which, id_t who) {
    return syscall(__NR_getpriority, which, who);
}

/* Syscall 64: setpriority */
static inline long syscall_setpriority(int which, id_t who, int prio) {
    return syscall(__NR_setpriority, which, who, prio);
}

/* Syscall 72: wait4 */
static inline long syscall_wait4(pid_t pid, int *wstatus, int options, struct rusage *rusage) {
    return syscall(__NR_wait4, pid, wstatus, options, rusage);
}

/* Syscall 83: symlink */
static inline long syscall_symlink(const char *target, const char *linkpath) {
    return syscall(__NR_symlink, target, linkpath);
}

/* Syscall 85: readlink */
static inline long syscall_readlink(const char *pathname, char *buf, size_t bufsiz) {
    return syscall(__NR_readlink, pathname, buf, bufsiz);
}

/* Syscall 89: readdir */
static inline long syscall_readdir(unsigned int fd, struct linux_dirent *dirp, unsigned int count) {
    return syscall(__NR_getdents, fd, dirp, count);
}

/* Syscall 92: writev */
static inline long syscall_writev(int fd, const struct iovec *iov, int iovcnt) {
    return syscall(__NR_writev, fd, iov, iovcnt);
}

/* Syscall 93: readv */
static inline long syscall_readv(int fd, const struct iovec *iov, int iovcnt) {
    return syscall(__NR_readv, fd, iov, iovcnt);
}

/* Syscall 102: socketcall */
static inline long syscall_socketcall(int call, unsigned long *args) {
    return syscall(__NR_socketcall, call, args);
}

/* Syscall 104: setitimer */
static inline long syscall_setitimer(int which, const struct itimerval *new_value, struct itimerval *old_value) {
    return syscall(__NR_setitimer, which, new_value, old_value);
}

/* Syscall 107: stat_new */
static inline long syscall_stat_new(const char *pathname, struct stat *statbuf) {
    return syscall(__NR_stat, pathname, statbuf);
}

/* Syscall 114: wait3 */
static inline long syscall_wait3(int *wstatus, int options, struct rusage *rusage) {
    return syscall(__NR_wait3, wstatus, options, rusage);
}

/* Syscall 125: mprotect */
static inline long syscall_mprotect(void *addr, size_t len, int prot) {
    return syscall(__NR_mprotect, addr, len, prot);
}

/* Syscall 140: _llseek */
static inline long syscall_llseek(int fd, unsigned long offset_high, unsigned long offset_low, loff_t *result, int whence) {
    return syscall(__NR__llseek, fd, offset_high, offset_low, result, whence);
}

/* Syscall 162: nanosleep */
static inline long syscall_nanosleep(const struct timespec *req, struct timespec *rem) {
    return syscall(__NR_nanosleep, req, rem);
}

/* Syscall 168: poll */
static inline long syscall_poll(struct pollfd *fds, nfds_t nfds, int timeout) {
    return syscall(__NR_poll, fds, nfds, timeout);
}

/* Syscall 186: gettid */
static inline long syscall_gettid(void) {
    return syscall(__NR_gettid);
}

/* Syscall 228: clock_nanosleep */
static inline long syscall_clock_nanosleep(clockid_t clockid, int flags, const struct timespec *request, struct timespec *remain) {
    return syscall(__NR_clock_nanosleep, clockid, flags, request, remain);
}

/* Syscall 257: openat */
static inline long syscall_openat(int dirfd, const char *pathname, int flags, mode_t mode) {
    return syscall(__NR_openat, dirfd, pathname, flags, mode);
}

/* Syscall 258: openat_read */
static inline long syscall_openat_read(int dirfd, const char *pathname) {
    return syscall(__NR_openat, dirfd, pathname, O_RDONLY, 0);
}

/* Syscall 259: openat_write */
static inline long syscall_openat_write(int dirfd, const char *pathname) {
    return syscall(__NR_openat, dirfd, pathname, O_WRONLY | O_CREAT, 0644);
}

/* Syscall 262: newfstatat */
static inline long syscall_newfstatat(int dirfd, const char *pathname, struct stat *statbuf, int flags) {
    return syscall(__NR_newfstatat, dirfd, pathname, statbuf, flags);
}

/* Syscall 273: set_robust_list */
static inline long syscall_set_robust_list(struct robust_list_head *head, size_t len) {
    return syscall(__NR_set_robust_list, head, len);
}

/* Syscall 274: get_robust_list */
static inline long syscall_get_robust_list(int pid, struct robust_list_head **head_ptr, size_t *len_ptr) {
    return syscall(__NR_get_robust_list, pid, head_ptr, len_ptr);
}

/* ===== SYSCALLS MODERNOS (x86-64) ===== */

/* Syscall 0: read */
static inline long syscall_read_new(int fd, void *buf, size_t count) {
    return syscall(__NR_read, fd, buf, count);
}

/* Syscall 1: write */
static inline long syscall_write_new(int fd, const void *buf, size_t count) {
    return syscall(__NR_write, fd, buf, count);
}

/* Syscall 2: open */
static inline long syscall_open_new(const char *pathname, int flags, mode_t mode) {
    return syscall(__NR_openat, AT_FDCWD, pathname, flags, mode);
}

/* Syscall 3: close */
static inline long syscall_close_new(int fd) {
    return syscall(__NR_close, fd);
}

/* Syscall 257: openat */
static inline long syscall_openat_new(int dirfd, const char *pathname, int flags, mode_t mode) {
    return syscall(__NR_openat, dirfd, pathname, flags, mode);
}

/* ===== OTIMIZAÇÕES DO KERNEL ===== */

/* Prefetch para otimizar cache */
#define KERNEL_PREFETCH(addr) __builtin_prefetch((addr), 0, 3)

/* Barrier para garantir ordem de execução */
#define KERNEL_BARRIER() asm volatile("" ::: "memory")

/* Likely/Unlikely para otimizar branch prediction */
#define likely(x) __builtin_expect(!!(x), 1)
#define unlikely(x) __builtin_expect(!!(x), 0)

/* ===== ESTRUTURAS DO KERNEL ===== */

/* Estrutura de arquivo (simplificada) */
struct ulx_file {
    int fd;
    long offset;
    int flags;
    int mode;
};

/* Estrutura de diretório (simplificada) */
struct ulx_dir {
    int fd;
    char *buffer;
    size_t buffer_size;
    size_t offset;
};

/* ===== FUNÇÕES WRAPPER ===== */

/* Abre arquivo usando syscall direto */
int ulx_kernel_open(const char *path, int flags, int mode) {
    long ret = syscall_open(path, flags, mode);
    if (ret < 0) {
        return -1;
    }
    return (int)ret;
}

/* Lê arquivo usando syscall direto */
ssize_t ulx_kernel_read(int fd, void *buf, size_t count) {
    return syscall_read(fd, buf, count);
}

/* Escreve arquivo usando syscall direto */
ssize_t ulx_kernel_write(int fd, const void *buf, size_t count) {
    return syscall_write(fd, buf, count);
}

/* Fecha arquivo usando syscall direto */
int ulx_kernel_close(int fd) {
    return (int)syscall_close(fd);
}

/* ===== OTIMIZAÇÕES ESPECÍFICAS DO KERNEL ===== */

/* Usa mmap para leitura rápida de arquivos grandes */
void* ulx_kernel_mmap_file(int fd, size_t size) {
    return mmap(NULL, size, PROT_READ, MAP_SHARED, fd, 0);
}

/* Usa sendfile para transferência rápida */
ssize_t ulx_kernel_sendfile(int out_fd, int in_fd, off_t *offset, size_t count) {
    return sendfile(out_fd, in_fd, offset, count);
}

/* Usa splice para zero-copy */
ssize_t ulx_kernel_splice(int fd_in, loff_t *off_in, int fd_out, loff_t *off_out, size_t len, unsigned int flags) {
    return splice(fd_in, off_in, fd_out, off_out, len, flags);
}

#endif
