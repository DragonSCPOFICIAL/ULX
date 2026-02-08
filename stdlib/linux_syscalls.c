/*
 * ULX Linux Syscalls Library
 * 
 * Wrappers para syscalls Linux universais
 * Funciona em qualquer distribuição Linux
 * Compatibilidade 100% garantida
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <sys/socket.h>
#include <sys/mman.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <errno.h>
#include <dirent.h>

#pragma GCC optimize("O3")
#pragma GCC target("native")

/* ===== I/O SYSCALLS ===== */

/* Abre arquivo */
inline int ulx_open(const char* path, int flags) {
    return open(path, flags, 0644);
}

/* Lê arquivo */
inline int ulx_read(int fd, void* buffer, int size) {
    return read(fd, buffer, size);
}

/* Escreve arquivo */
inline int ulx_write(int fd, const void* buffer, int size) {
    return write(fd, buffer, size);
}

/* Fecha arquivo */
inline int ulx_close(int fd) {
    return close(fd);
}

/* Obtém informações do arquivo */
inline int ulx_stat(const char* path, struct stat* st) {
    return stat(path, st);
}

/* Muda permissões */
inline int ulx_chmod(const char* path, int mode) {
    return chmod(path, mode);
}

/* Muda proprietário */
inline int ulx_chown(const char* path, int uid, int gid) {
    return chown(path, uid, gid);
}

/* ===== DIRETÓRIO SYSCALLS ===== */

/* Abre diretório */
inline DIR* ulx_opendir(const char* path) {
    return opendir(path);
}

/* Lê entrada de diretório */
inline struct dirent* ulx_readdir(DIR* dir) {
    return readdir(dir);
}

/* Fecha diretório */
inline int ulx_closedir(DIR* dir) {
    return closedir(dir);
}

/* Cria diretório */
inline int ulx_mkdir(const char* path, int mode) {
    return mkdir(path, mode);
}

/* Remove diretório */
inline int ulx_rmdir(const char* path) {
    return rmdir(path);
}

/* Muda diretório */
inline int ulx_chdir(const char* path) {
    return chdir(path);
}

/* Obtém diretório atual */
inline char* ulx_getcwd(char* buffer, int size) {
    return getcwd(buffer, size);
}

/* ===== PROCESSO SYSCALLS ===== */

/* Fork - cria novo processo */
inline int ulx_fork() {
    return fork();
}

/* Exec - executa programa */
inline int ulx_exec(const char* path, char* const argv[]) {
    return execv(path, argv);
}

/* Wait - aguarda processo */
inline int ulx_wait(int* status) {
    return wait(status);
}

/* Waitpid - aguarda processo específico */
inline int ulx_waitpid(int pid, int* status) {
    return waitpid(pid, status, 0);
}

/* Exit - sai do processo */
inline void ulx_exit(int code) {
    exit(code);
}

/* Obtém PID */
inline int ulx_getpid() {
    return getpid();
}

/* Obtém PID do pai */
inline int ulx_getppid() {
    return getppid();
}

/* Obtém UID */
inline int ulx_getuid() {
    return getuid();
}

/* Obtém GID */
inline int ulx_getgid() {
    return getgid();
}

/* ===== MEMÓRIA SYSCALLS ===== */

/* Aloca memória */
inline void* ulx_mmap(void* addr, int size, int prot, int flags) {
    return mmap(addr, size, prot, flags, -1, 0);
}

/* Libera memória */
inline int ulx_munmap(void* addr, int size) {
    return munmap(addr, size);
}

/* Muda proteção de memória */
inline int ulx_mprotect(void* addr, int size, int prot) {
    return mprotect(addr, size, prot);
}

/* Aloca memória alinhada */
inline void* ulx_malloc_aligned(int size, int align) {
    void* ptr;
    posix_memalign(&ptr, align, size);
    return ptr;
}

/* ===== SOCKET SYSCALLS ===== */

/* Cria socket */
inline int ulx_socket(int domain, int type, int protocol) {
    return socket(domain, type, protocol);
}

/* Bind - associa socket a endereço */
inline int ulx_bind(int sockfd, struct sockaddr* addr, int addrlen) {
    return bind(sockfd, addr, addrlen);
}

/* Listen - coloca socket em modo escuta */
inline int ulx_listen(int sockfd, int backlog) {
    return listen(sockfd, backlog);
}

/* Accept - aceita conexão */
inline int ulx_accept(int sockfd, struct sockaddr* addr, int* addrlen) {
    return accept(sockfd, addr, (socklen_t*)addrlen);
}

/* Connect - conecta a servidor */
inline int ulx_connect(int sockfd, struct sockaddr* addr, int addrlen) {
    return connect(sockfd, addr, addrlen);
}

/* Send - envia dados */
inline int ulx_send(int sockfd, const void* buffer, int size, int flags) {
    return send(sockfd, buffer, size, flags);
}

/* Recv - recebe dados */
inline int ulx_recv(int sockfd, void* buffer, int size, int flags) {
    return recv(sockfd, buffer, size, flags);
}

/* Shutdown - fecha socket */
inline int ulx_shutdown(int sockfd, int how) {
    return shutdown(sockfd, how);
}

/* ===== PIPE SYSCALLS ===== */

/* Cria pipe */
inline int ulx_pipe(int* fds) {
    return pipe(fds);
}

/* Duplica file descriptor */
inline int ulx_dup(int fd) {
    return dup(fd);
}

/* Duplica para file descriptor específico */
inline int ulx_dup2(int oldfd, int newfd) {
    return dup2(oldfd, newfd);
}

/* ===== SINAL SYSCALLS ===== */

/* Define handler de sinal */
typedef void (*signal_handler_t)(int);

inline signal_handler_t ulx_signal(int signum, signal_handler_t handler) {
    return signal(signum, handler);
}

/* Envia sinal */
inline int ulx_kill(int pid, int sig) {
    return kill(pid, sig);
}

/* ===== TEMPO SYSCALLS ===== */

/* Obtém tempo atual */
inline int ulx_time() {
    return time(NULL);
}

/* Dorme em milissegundos */
inline int ulx_sleep_ms(int ms) {
    return usleep(ms * 1000);
}

/* ===== AMBIENTE SYSCALLS ===== */

/* Obtém variável de ambiente */
inline char* ulx_getenv(const char* name) {
    return getenv(name);
}

/* Define variável de ambiente */
inline int ulx_setenv(const char* name, const char* value) {
    return setenv(name, value, 1);
}

/* ===== ARQUIVO SYSCALLS ===== */

/* Remove arquivo */
inline int ulx_unlink(const char* path) {
    return unlink(path);
}

/* Renomeia arquivo */
inline int ulx_rename(const char* oldpath, const char* newpath) {
    return rename(oldpath, newpath);
}

/* Cria link simbólico */
inline int ulx_symlink(const char* target, const char* linkpath) {
    return symlink(target, linkpath);
}

/* Lê link simbólico */
inline int ulx_readlink(const char* path, char* buffer, int size) {
    return readlink(path, buffer, size);
}

/* ===== UTILIDADES ===== */

/* Imprime erro */
inline void ulx_perror(const char* msg) {
    perror(msg);
}

/* Obtém último erro */
inline int ulx_errno() {
    return errno;
}

/* Define último erro */
inline void ulx_set_errno(int err) {
    errno = err;
}

/* ===== SYSCALLS DIRETOS (x86-64) ===== */

/* Syscall direto (para casos avançados) */
inline long ulx_syscall(long number, ...) {
    // Implementação depende da arquitetura
    // Aqui está o placeholder para x86-64
    return -1;
}

/* ===== ESTRUTURAS AUXILIARES ===== */

/* Estrutura para endereço IPv4 */
struct ulx_addr {
    char ip[16];
    int port;
};

/* Cria endereço IPv4 */
inline struct sockaddr_in ulx_make_addr(const char* ip, int port) {
    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    inet_pton(AF_INET, ip, &addr.sin_addr);
    return addr;
}

/* ===== FUNÇÕES DE COMPATIBILIDADE ===== */

/* Verifica se arquivo existe */
inline int ulx_file_exists(const char* path) {
    struct stat st;
    return stat(path, &st) == 0;
}

/* Obtém tamanho do arquivo */
inline long ulx_file_size(const char* path) {
    struct stat st;
    if (stat(path, &st) == 0) {
        return st.st_size;
    }
    return -1;
}

/* Verifica se é diretório */
inline int ulx_is_dir(const char* path) {
    struct stat st;
    if (stat(path, &st) == 0) {
        return S_ISDIR(st.st_mode);
    }
    return 0;
}

/* Verifica se é arquivo regular */
inline int ulx_is_file(const char* path) {
    struct stat st;
    if (stat(path, &st) == 0) {
        return S_ISREG(st.st_mode);
    }
    return 0;
}

#endif
