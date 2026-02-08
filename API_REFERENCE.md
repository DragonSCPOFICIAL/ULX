# ULX Standard Library - Referência Completa da API

## Índice

1. [Syscalls do Kernel Linux](#syscalls)
2. [Manipulação de Strings](#strings)
3. [Manipulação de Memória](#memoria)
4. [Operações Matemáticas](#matematica)
5. [Conversão de Tipos](#conversao)
6. [I/O de Console](#console)
7. [Operações de Arquivo](#arquivos)
8. [Estruturas de Dados](#estruturas)
9. [Threading e Sincronização](#threading)
10. [Networking](#networking)
11. [Utilitários de Sistema](#sistema)
12. [Dragon Engine - UI](#dragon-engine)

---

## 1. Syscalls do Kernel Linux {#syscalls}

### I/O de Arquivos

#### `read(fd: i32, buffer: ptr, count: usize) -> isize`
Lê dados de um descritor de arquivo.
- **Parâmetros:**
  - `fd`: Descritor do arquivo
  - `buffer`: Buffer para armazenar os dados
  - `count`: Número de bytes a ler
- **Retorna:** Número de bytes lidos, ou -1 em caso de erro
- **Exemplo:**
```ulx
var buffer: i8[1024];
var bytes_read: isize = read(0, &buffer, 1024); // Lê do stdin
```

#### `write(fd: i32, buffer: ptr, count: usize) -> isize`
Escreve dados em um descritor de arquivo.
- **Parâmetros:**
  - `fd`: Descritor do arquivo
  - `buffer`: Buffer contendo os dados
  - `count`: Número de bytes a escrever
- **Retorna:** Número de bytes escritos, ou -1 em caso de erro

#### `open(path: ptr, flags: i32, mode: i32) -> i32`
Abre um arquivo.
- **Parâmetros:**
  - `path`: Caminho do arquivo
  - `flags`: Flags de abertura (O_RDONLY, O_WRONLY, O_RDWR, O_CREAT, etc.)
  - `mode`: Permissões do arquivo (quando O_CREAT é usado)
- **Retorna:** Descritor do arquivo, ou -1 em caso de erro

#### `close(fd: i32) -> i32`
Fecha um descritor de arquivo.
- **Parâmetros:**
  - `fd`: Descritor do arquivo
- **Retorna:** 0 em sucesso, -1 em erro

### Processos

#### `fork() -> i32`
Cria um novo processo duplicando o processo atual.
- **Retorna:** 
  - 0 no processo filho
  - PID do filho no processo pai
  - -1 em caso de erro

#### `execve(path: ptr, argv: ptr, envp: ptr) -> i32`
Executa um programa.
- **Parâmetros:**
  - `path`: Caminho do executável
  - `argv`: Array de argumentos
  - `envp`: Array de variáveis de ambiente
- **Retorna:** Não retorna em sucesso, -1 em erro

#### `exit(status: i32)`
Termina o processo atual.
- **Parâmetros:**
  - `status`: Código de saída

#### `waitpid(pid: i32, status: ptr, options: i32) -> i32`
Aguarda a mudança de estado de um processo filho.
- **Parâmetros:**
  - `pid`: PID do processo filho
  - `status`: Ponteiro para armazenar o status
  - `options`: Opções de espera
- **Retorna:** PID do processo que mudou de estado, ou -1 em erro

### Memória

#### `mmap(addr: ptr, length: usize, prot: i32, flags: i32, fd: i32, offset: i64) -> ptr`
Mapeia arquivos ou dispositivos na memória.
- **Retorna:** Ponteiro para a região mapeada, ou erro

#### `munmap(addr: ptr, length: usize) -> i32`
Remove o mapeamento de uma região de memória.

#### `brk(addr: ptr) -> ptr`
Altera o fim do segmento de dados do processo.

### Tempo

#### `nanosleep(req: ptr, rem: ptr) -> i32`
Pausa a execução por um tempo especificado.

#### `gettimeofday(tv: ptr, tz: ptr) -> i32`
Obtém a data e hora atual.

### Rede

#### `socket(domain: i32, type: i32, protocol: i32) -> i32`
Cria um endpoint para comunicação.

#### `bind(sockfd: i32, addr: ptr, addrlen: u32) -> i32`
Liga um socket a um endereço.

#### `listen(sockfd: i32, backlog: i32) -> i32`
Escuta por conexões em um socket.

#### `accept(sockfd: i32, addr: ptr, addrlen: ptr) -> i32`
Aceita uma conexão em um socket.

#### `connect(sockfd: i32, addr: ptr, addrlen: u32) -> i32`
Conecta um socket a um endereço remoto.

---

## 2. Manipulação de Strings {#strings}

### `strlen(s: ptr) -> usize`
Calcula o comprimento de uma string.
- **Exemplo:**
```ulx
var s: ptr = "Hello";
var len: usize = strlen(s); // len = 5
```

### `strcmp(s1: ptr, s2: ptr) -> i32`
Compara duas strings.
- **Retorna:**
  - 0 se forem iguais
  - < 0 se s1 < s2
  - > 0 se s1 > s2

### `strcpy(dest: ptr, src: ptr) -> ptr`
Copia uma string.

### `strcat(dest: ptr, src: ptr) -> ptr`
Concatena duas strings.

### `strncpy(dest: ptr, src: ptr, n: usize) -> ptr`
Copia até n caracteres de uma string.

### `strchr(s: ptr, c: i8) -> ptr`
Encontra a primeira ocorrência de um caractere.
- **Retorna:** Ponteiro para o caractere, ou 0 se não encontrado

### `strstr(haystack: ptr, needle: ptr) -> ptr`
Encontra a primeira ocorrência de uma substring.
- **Exemplo:**
```ulx
var texto: ptr = "Hello, World!";
var pos: ptr = strstr(texto, "World"); // pos aponta para "World!"
```

---

## 3. Manipulação de Memória {#memoria}

### `memset(s: ptr, c: i8, n: usize) -> ptr`
Preenche uma região de memória com um valor.
- **Exemplo:**
```ulx
var buffer: i8[100];
memset(&buffer, 0, 100); // Zera o buffer
```

### `memcpy(dest: ptr, src: ptr, n: usize) -> ptr`
Copia uma região de memória.

### `memmove(dest: ptr, src: ptr, n: usize) -> ptr`
Copia memória, suportando sobreposição.

### `memcmp(s1: ptr, s2: ptr, n: usize) -> i32`
Compara duas regiões de memória.

### Gerenciamento de Heap

#### `heap_init(size: usize) -> bool`
Inicializa o heap com um tamanho especificado.
- **Exemplo:**
```ulx
if (!heap_init(1048576)) { // 1MB
    println("Erro ao inicializar heap!");
}
```

#### `malloc(size: usize) -> ptr`
Aloca memória dinamicamente.
- **Exemplo:**
```ulx
var arr: ptr i32 = malloc(100 * 4); // Array de 100 inteiros
```

#### `free(ptr: ptr)`
Libera memória alocada (implementação simplificada).

---

## 4. Operações Matemáticas {#matematica}

### Básicas

#### `abs(x: i32) -> i32`
Valor absoluto.

#### `min(a: i32, b: i32) -> i32`
Retorna o menor valor.

#### `max(a: i32, b: i32) -> i32`
Retorna o maior valor.

### Avançadas

#### `pow(base: i32, exp: u32) -> i32`
Potenciação.
- **Exemplo:**
```ulx
var result: i32 = pow(2, 10); // result = 1024
```

#### `sqrt(x: i32) -> i32`
Raiz quadrada inteira.

#### `factorial(n: u32) -> u64`
Fatorial de um número.

#### `gcd(a: i32, b: i32) -> i32`
Máximo divisor comum.

#### `lcm(a: i32, b: i32) -> i32`
Mínimo múltiplo comum.

---

## 5. Conversão de Tipos {#conversao}

### `itoa(value: i32, buffer: ptr, base: i32) -> ptr`
Converte inteiro para string.
- **Parâmetros:**
  - `value`: Número a converter
  - `buffer`: Buffer para armazenar o resultado
  - `base`: Base numérica (2-36)
- **Exemplo:**
```ulx
var buffer: i8[32];
itoa(255, &buffer, 16); // buffer = "FF"
```

### `atoi(str: ptr) -> i32`
Converte string para inteiro.
- **Exemplo:**
```ulx
var num: i32 = atoi("12345"); // num = 12345
```

### `ftoa(value: f32, buffer: ptr, precision: i32) -> ptr`
Converte float para string com precisão especificada.
- **Exemplo:**
```ulx
var buffer: i8[64];
ftoa(3.14159, &buffer, 3); // buffer = "3.141"
```

---

## 6. I/O de Console {#console}

### Saída

#### `print(s: ptr) -> i32`
Imprime uma string no stdout.

#### `println(s: ptr) -> i32`
Imprime uma string seguida de nova linha.

#### `print_int(n: i32) -> i32`
Imprime um inteiro.

#### `print_hex(n: i32) -> i32`
Imprime um inteiro em hexadecimal.

#### `print_float(f: f32, precision: i32) -> i32`
Imprime um float com precisão especificada.

### Entrada

#### `getchar() -> i8`
Lê um caractere do stdin.

#### `readline(buffer: ptr, max_size: usize) -> i32`
Lê uma linha do stdin.
- **Exemplo:**
```ulx
var input: i8[256];
print("Digite algo: ");
readline(&input, 256);
```

---

## 7. Operações de Arquivo {#arquivos}

### Constantes

```ulx
const O_RDONLY: i32 = 0;
const O_WRONLY: i32 = 1;
const O_RDWR: i32 = 2;
const O_CREAT: i32 = 64;
const O_TRUNC: i32 = 512;
const O_APPEND: i32 = 1024;
```

### Funções de Alto Nível

#### `file_read_all(path: ptr, buffer: ptr, size: usize) -> isize`
Lê todo o conteúdo de um arquivo.
- **Exemplo:**
```ulx
var buffer: i8[1024];
var bytes: isize = file_read_all("dados.txt", &buffer, 1024);
```

#### `file_write_all(path: ptr, data: ptr, size: usize) -> isize`
Escreve dados em um arquivo.
- **Exemplo:**
```ulx
var data: ptr = "Conteúdo do arquivo\n";
file_write_all("output.txt", data, strlen(data));
```

#### `file_exists(path: ptr) -> bool`
Verifica se um arquivo existe.

#### `file_copy(src: ptr, dest: ptr) -> bool`
Copia um arquivo.
- **Exemplo:**
```ulx
if (file_copy("original.txt", "copia.txt")) {
    println("Arquivo copiado!");
}
```

---

## 8. Estruturas de Dados {#estruturas}

### Vector Dinâmico

#### Estrutura
```ulx
struct Vector {
    data: ptr;
    size: usize;
    capacity: usize;
}
```

#### `vector_new() -> Vector`
Cria um novo vector.

#### `vector_push(v: ptr Vector, value: i64)`
Adiciona um elemento ao final.

#### `vector_get(v: ptr Vector, index: usize) -> i64`
Obtém um elemento pelo índice.

#### `vector_set(v: ptr Vector, index: usize, value: i64)`
Define um elemento pelo índice.

**Exemplo completo:**
```ulx
var vec: Vector = vector_new();
vector_push(&vec, 10);
vector_push(&vec, 20);
vector_push(&vec, 30);

var value: i64 = vector_get(&vec, 1); // value = 20
vector_set(&vec, 1, 99); // Altera para 99
```

### HashMap

#### Estruturas
```ulx
struct HashMapEntry {
    key: ptr;
    value: i64;
    next: ptr HashMapEntry;
}

struct HashMap {
    buckets: ptr ptr HashMapEntry;
    size: usize;
    capacity: usize;
}
```

#### `hashmap_new(capacity: usize) -> HashMap`
Cria um novo hashmap.

#### `hashmap_set(map: ptr HashMap, key: ptr, value: i64)`
Define um par chave-valor.

#### `hashmap_get(map: ptr HashMap, key: ptr) -> i64`
Obtém um valor pela chave.

**Exemplo completo:**
```ulx
var map: HashMap = hashmap_new(16);
hashmap_set(&map, "nome", 42);
hashmap_set(&map, "idade", 25);

var idade: i64 = hashmap_get(&map, "idade"); // idade = 25
```

---

## 9. Threading e Sincronização {#threading}

### Syscalls

#### `clone(flags: i32, stack: ptr, ptid: ptr, ctid: ptr, newtls: ptr) -> i32`
Cria um novo processo/thread.

#### `futex(uaddr: ptr, op: i32, val: i32, timeout: ptr, uaddr2: ptr, val3: i32) -> i32`
Operações de sincronização em nível de usuário.

### Mutex

#### Estrutura
```ulx
struct Mutex {
    lock: i32;
}
```

#### `mutex_init(m: ptr Mutex)`
Inicializa um mutex.

#### `mutex_lock(m: ptr Mutex)`
Adquire o lock do mutex.

#### `mutex_unlock(m: ptr Mutex)`
Libera o lock do mutex.

**Exemplo completo:**
```ulx
global counter: i32 = 0;
global mutex: Mutex;

func increment() {
    mutex_lock(&mutex);
    counter = counter + 1;
    mutex_unlock(&mutex);
}

func main() -> i32 {
    mutex_init(&mutex);
    // Criar threads e incrementar contador
    return 0;
}
```

---

## 10. Networking {#networking}

### Constantes

```ulx
const AF_INET: i32 = 2;
const SOCK_STREAM: i32 = 1;  // TCP
const SOCK_DGRAM: i32 = 2;   // UDP
```

### Estrutura de Endereço

```ulx
struct SocketAddr {
    sin_family: u16;
    sin_port: u16;
    sin_addr: u32;
    sin_zero: i8[8];
}
```

### Funções Utilitárias

#### `htons(n: u16) -> u16`
Converte de host byte order para network byte order (16 bits).

#### `htonl(n: u32) -> u32`
Converte de host byte order para network byte order (32 bits).

#### `inet_addr(ip: ptr) -> u32`
Converte endereço IP em string para formato binário.
- **Exemplo:**
```ulx
var addr: u32 = inet_addr("192.168.1.1");
```

### Servidor TCP

#### `tcp_server_create(port: u16) -> i32`
Cria um servidor TCP.
- **Exemplo:**
```ulx
var server: i32 = tcp_server_create(8080);
if (server >= 0) {
    println("Servidor escutando na porta 8080");
}
```

### Cliente TCP

#### `tcp_client_connect(ip: ptr, port: u16) -> i32`
Conecta a um servidor TCP.
- **Exemplo:**
```ulx
var client: i32 = tcp_client_connect("127.0.0.1", 8080);
if (client >= 0) {
    println("Conectado ao servidor!");
}
```

---

## 11. Utilitários de Sistema {#sistema}

### Informações do Processo

#### `getpid() -> i32`
Retorna o PID do processo atual.

#### `getuid() -> i32`
Retorna o UID do usuário atual.

#### `getgid() -> i32`
Retorna o GID do grupo atual.

#### `kill(pid: i32, sig: i32) -> i32`
Envia um sinal para um processo.

### Tempo

#### `sleep(seconds: u32)`
Pausa a execução por segundos.

#### `usleep(microseconds: u64)`
Pausa a execução por microssegundos.

#### `get_timestamp_ms() -> u64`
Obtém o timestamp atual em milissegundos.
- **Exemplo:**
```ulx
var start: u64 = get_timestamp_ms();
// ... código a medir ...
var end: u64 = get_timestamp_ms();
var elapsed: u64 = end - start;
print_int(elapsed);
println(" ms");
```

---

## 12. Dragon Engine - UI {#dragon-engine}

### Estruturas

```ulx
struct DragonWindow {
    connection: ptr;
    window: u32;
    width: u32;
    height: u32;
    title: ptr;
}

struct DragonColor {
    r: u8;
    g: u8;
    b: u8;
    a: u8;
}
```

### Inicialização

#### `dragon_init() -> ptr`
Inicializa a conexão com o servidor X11.

#### `dragon_create_window(width: u32, height: u32, title: ptr) -> DragonWindow`
Cria uma janela gráfica.
- **Exemplo:**
```ulx
var conn: ptr = dragon_init();
var window: DragonWindow = dragon_create_window(800, 600, "Minha Janela");
```

### Desenho

#### `dragon_draw_rect(window: ptr DragonWindow, x: i32, y: i32, w: u32, h: u32, color: DragonColor)`
Desenha um retângulo.

#### `dragon_draw_circle(window: ptr DragonWindow, x: i32, y: i32, radius: u32, color: DragonColor)`
Desenha um círculo.

#### `dragon_draw_text(window: ptr DragonWindow, x: i32, y: i32, text: ptr, color: DragonColor)`
Desenha texto.

### Atualização e Eventos

#### `dragon_update(window: ptr DragonWindow)`
Atualiza o buffer da janela.

#### `dragon_poll_events(window: ptr DragonWindow) -> i32`
Processa eventos da janela.
- **Retorna:** Tipo de evento ou 0 se não houver eventos

**Exemplo completo:**
```ulx
var conn: ptr = dragon_init();
var window: DragonWindow = dragon_create_window(640, 480, "ULX App");

var red: DragonColor;
red.r = 255;
red.g = 0;
red.b = 0;
red.a = 255;

dragon_draw_rect(&window, 100, 100, 200, 150, red);
dragon_update(&window);

while (true) {
    var event: i32 = dragon_poll_events(&window);
    if (event != 0) break;
    usleep(16666); // ~60 FPS
}
```

---

## Exemplos Práticos

### Aplicação Web Simples

```ulx
func web_server() -> i32 {
    var server: i32 = tcp_server_create(8080);
    println("Servidor HTTP na porta 8080");
    
    while (true) {
        var addr: SocketAddr;
        var len: u32 = sizeof(SocketAddr);
        var client: i32 = accept(server, &addr, &len);
        
        var request: i8[4096];
        read(client, &request, 4096);
        
        var response: ptr = "HTTP/1.1 200 OK\r\n"
                           "Content-Type: text/html\r\n"
                           "\r\n"
                           "<h1>ULX Web Server</h1>";
        
        write(client, response, strlen(response));
        close(client);
    }
    
    return 0;
}
```

### Monitor de Sistema

```ulx
func system_monitor() -> i32 {
    while (true) {
        print("PID: ");
        print_int(getpid());
        print(" | Timestamp: ");
        print_int(get_timestamp_ms());
        println("");
        
        sleep(1);
    }
    return 0;
}
```

### Processamento de Texto

```ulx
func count_words(text: ptr) -> i32 {
    var count: i32 = 0;
    var in_word: bool = false;
    var i: i32 = 0;
    
    while (text[i] != 0) {
        if (text[i] == ' ' || text[i] == '\n' || text[i] == '\t') {
            in_word = false;
        } else if (!in_word) {
            in_word = true;
            count = count + 1;
        }
        i = i + 1;
    }
    
    return count;
}
```

---

## Performance e Otimização

### Dicas

1. **Use syscalls diretas** quando possível para máxima performance
2. **Aloque memória uma vez** ao invés de múltiplas alocações pequenas
3. **Use mutexes com moderação** - contenção excessiva reduz paralelismo
4. **Buffer I/O** - leia/escreva em grandes blocos
5. **Inline functions pequenas** para eliminar overhead de chamada

### Benchmarking

```ulx
func benchmark(iterations: i32) {
    var start: u64 = get_timestamp_ms();
    
    var i: i32 = 0;
    while (i < iterations) {
        // Código a medir
        i = i + 1;
    }
    
    var end: u64 = get_timestamp_ms();
    var ops_per_sec: i32 = iterations / ((end - start) / 1000);
    
    print("Operações por segundo: ");
    print_int(ops_per_sec);
    println("");
}
```

---

## Conclusão

Esta biblioteca ULX fornece todas as ferramentas necessárias para criar aplicações nativas Linux de alta performance, desde servidores de rede até interfaces gráficas, passando por processamento paralelo e manipulação de dados.

Para mais exemplos, consulte o arquivo `examples_showcase.ulx`.

**Versão:** 2.0.0  
**Data:** 2026  
**Licença:** MIT
