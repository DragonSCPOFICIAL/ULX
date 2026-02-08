# ULX - Sintaxe Completa

## Introdução

ULX é uma linguagem super simples, mas poderosa. Cada comando faz exatamente o que você espera.

## Comentários

```ulx
// Comentário de linha única

/* Comentário
   de múltiplas
   linhas */
```

## Variáveis

### Declaração Implícita

```ulx
a = 10
b = 20
c = a + b
```

### Tipos Suportados

- **Inteiros**: `10`, `42`, `-5`
- **Strings**: `"texto"`, `'texto'`
- **Booleanos**: `verdadeiro`, `falso`
- **Nulo**: `nulo`

## Operadores

### Aritméticos

```ulx
a = 10 + 5    // Adição
b = 10 - 5    // Subtração
c = 10 * 5    // Multiplicação
d = 10 / 5    // Divisão
e = 10 % 3    // Módulo
f = 2 ^ 3     // Potência
```

### Comparação

```ulx
a == b        // Igual
a != b        // Diferente
a > b         // Maior
a < b         // Menor
a >= b        // Maior ou igual
a <= b        // Menor ou igual
```

### Lógicos

```ulx
a && b        // E (AND)
a || b        // OU (OR)
!a            // NÃO (NOT)
```

### Atribuição

```ulx
a = 10        // Atribuição simples
a += 5        // Atribuição com adição
a -= 5        // Atribuição com subtração
a *= 2        // Atribuição com multiplicação
a /= 2        // Atribuição com divisão
```

## Controle de Fluxo

### If/Else

```ulx
se (condicao) {
    // Código se verdadeiro
} senao se (outra_condicao) {
    // Código se outra condição verdadeira
} senao {
    // Código padrão
}
```

### While

```ulx
enquanto (condicao) {
    // Código repetido enquanto verdadeiro
}
```

### For

```ulx
para (i = 0; i < 10; i = i + 1) {
    // Código repetido 10 vezes
}
```

### Break e Continue

```ulx
para (i = 0; i < 10; i = i + 1) {
    se (i == 5) {
        continua  // Pula para próxima iteração
    }
    
    se (i == 8) {
        para      // Sai do loop
    }
    
    escreva(i)
}
```

## Funções

### Definição

```ulx
funcao saudacao(nome) {
    escreva("Olá, ")
    escreva(nome)
}

funcao soma(a, b) {
    resultado = a + b
    retorna resultado
}
```

### Chamada

```ulx
saudacao("João")
x = soma(10, 20)
```

### Funções Sem Parâmetros

```ulx
funcao ola() {
    escreva("Olá!")
}

ola()
```

### Funções Sem Retorno

```ulx
funcao imprime_numero(n) {
    escreva(n)
}

imprime_numero(42)
```

## I/O (Entrada/Saída)

### Escrever (Output)

```ulx
escreva("Texto")
escreva(10)
escreva(variavel)
escreva("Múltiplos ", "argumentos ", "aqui")
```

### Ler (Input)

```ulx
entrada = le()
```

### Ler Arquivo

```ulx
arquivo = abre("/caminho/arquivo.txt")
conteudo = le(arquivo)
fecha(arquivo)
```

### Escrever Arquivo

```ulx
arquivo = cria("/caminho/arquivo.txt")
escreve(arquivo, "conteúdo")
fecha(arquivo)
```

## Strings

### Concatenação

```ulx
nome = "João"
mensagem = "Olá, " + nome
escreva(mensagem)
```

### Comprimento

```ulx
texto = "Hello"
tamanho = tamanho(texto)
escreva(tamanho)  // 5
```

### Substring

```ulx
texto = "Hello"
parte = substring(texto, 0, 2)
escreva(parte)  // He
```

### Maiúscula/Minúscula

```ulx
texto = "Hello"
maiuscula = maiuscula(texto)
minuscula = minuscula(texto)
```

## Arrays

### Declaração

```ulx
numeros = [1, 2, 3, 4, 5]
nomes = ["João", "Maria", "Pedro"]
```

### Acesso

```ulx
primeiro = numeros[0]
segundo = numeros[1]
```

### Tamanho

```ulx
tamanho_array = tamanho(numeros)
```

### Adicionar

```ulx
numeros = [1, 2, 3]
adiciona(numeros, 4)
```

### Remover

```ulx
numeros = [1, 2, 3, 4, 5]
remove(numeros, 2)  // Remove índice 2
```

### Iteração

```ulx
numeros = [1, 2, 3, 4, 5]

para (i = 0; i < tamanho(numeros); i = i + 1) {
    escreva(numeros[i])
}
```

## Dicionários

### Declaração

```ulx
pessoa = {
    "nome": "João",
    "idade": 30,
    "cidade": "São Paulo"
}
```

### Acesso

```ulx
nome = pessoa["nome"]
idade = pessoa["idade"]
```

### Modificação

```ulx
pessoa["idade"] = 31
pessoa["email"] = "joao@example.com"
```

### Iteração

```ulx
pessoa = {"nome": "João", "idade": 30}

para (chave em pessoa) {
    valor = pessoa[chave]
    escreva(chave + ": " + valor)
}
```

## Exceções

### Try/Catch

```ulx
tenta {
    arquivo = abre("/arquivo_inexistente.txt")
    conteudo = le(arquivo)
} captura (erro) {
    escreva("Erro: " + erro)
}
```

### Throw

```ulx
funcao divide(a, b) {
    se (b == 0) {
        lanca "Divisão por zero!"
    }
    retorna a / b
}
```

## Operações com Arquivo

### Abrir

```ulx
arquivo = abre("/caminho/arquivo.txt")
```

### Ler

```ulx
conteudo = le(arquivo)
```

### Escrever

```ulx
escreve(arquivo, "novo conteúdo")
```

### Fechar

```ulx
fecha(arquivo)
```

### Verificar Existência

```ulx
se (existe("/caminho/arquivo.txt")) {
    escreva("Arquivo existe")
}
```

### Deletar

```ulx
deleta("/caminho/arquivo.txt")
```

## Operações com Diretório

### Abrir

```ulx
diretorio = abre_dir("/caminho")
```

### Listar

```ulx
diretorio = abre_dir(".")
arquivo = le_dir(diretorio)

enquanto (arquivo != "") {
    escreva(arquivo)
    arquivo = le_dir(diretorio)
}

fecha_dir(diretorio)
```

### Criar

```ulx
cria_dir("/novo/diretorio")
```

### Remover

```ulx
remove_dir("/diretorio/vazio")
```

## Operações de Processo

### Executar Comando

```ulx
resultado = executa("ls -la")
escreva(resultado)
```

### Fork (Criar Processo)

```ulx
pid = fork()

se (pid == 0) {
    // Processo filho
    escreva("Sou o filho")
} senao {
    // Processo pai
    escreva("Sou o pai")
    espera(pid)
}
```

### Exit (Sair)

```ulx
sai(0)  // Sai com código 0
```

## Operações de Rede

### Criar Socket

```ulx
socket = cria_socket()
```

### Conectar

```ulx
conecta(socket, "localhost", 8080)
```

### Bind

```ulx
socket = cria_socket()
conecta(socket, "0.0.0.0", 8080)
```

### Listen

```ulx
escuta(socket, 10)
```

### Accept

```ulx
cliente = aceita(socket)
```

### Send

```ulx
envia(socket, "mensagem")
```

### Receive

```ulx
mensagem = recebe(socket)
```

### Close

```ulx
fecha(socket)
```

## Funções Embutidas

### Matemática

```ulx
abs(-5)          // Valor absoluto
sqrt(16)         // Raiz quadrada
pow(2, 3)        // Potência
floor(3.7)       // Arredonda para baixo
ceil(3.2)        // Arredonda para cima
round(3.5)       // Arredonda
sin(0)           // Seno
cos(0)           // Cosseno
tan(0)           // Tangente
```

### String

```ulx
tamanho("texto")           // Comprimento
substring("hello", 0, 2)   // Extrai substring
maiuscula("hello")         // Maiúscula
minuscula("HELLO")         // Minúscula
trim("  texto  ")          // Remove espaços
split("a,b,c", ",")        // Divide string
join(["a", "b"], ",")      // Junta array
```

### Array

```ulx
tamanho([1, 2, 3])         // Comprimento
adiciona([1, 2], 3)        // Adiciona elemento
remove([1, 2, 3], 1)       // Remove por índice
contém([1, 2, 3], 2)       // Verifica se contém
índice([1, 2, 3], 2)       // Encontra índice
```

### Tipo

```ulx
tipo(10)                   // "inteiro"
tipo("texto")              // "string"
tipo([1, 2])               // "array"
tipo({})                   // "dicionário"
```

### Conversão

```ulx
inteiro("42")              // Converte para inteiro
texto(42)                  // Converte para string
booleano(1)                // Converte para booleano
```

## Exemplos Completos

### Hello World

```ulx
escreva("Olá, mundo!")
```

### Fibonacci

```ulx
funcao fibonacci(n) {
    se (n <= 1) {
        retorna n
    }
    retorna fibonacci(n - 1) + fibonacci(n - 2)
}

para (i = 0; i < 10; i = i + 1) {
    escreva(fibonacci(i))
}
```

### Ler e Processar Arquivo

```ulx
arquivo = abre("/etc/passwd")
conteudo = le(arquivo)
fecha(arquivo)

linhas = split(conteudo, "\n")

para (i = 0; i < tamanho(linhas); i = i + 1) {
    linha = linhas[i]
    escreva(linha)
}
```

### Servidor HTTP Simples

```ulx
socket = cria_socket()
conecta(socket, "0.0.0.0", 8080)
escuta(socket, 10)

escreva("Servidor rodando na porta 8080")

para (i = 0; i < 100; i = i + 1) {
    cliente = aceita(socket)
    
    requisicao = recebe(cliente)
    
    resposta = "HTTP/1.1 200 OK\r\nContent-Length: 5\r\n\r\nHello"
    envia(cliente, resposta)
    
    fecha(cliente)
}

fecha(socket)
```

### Processamento de Dados

```ulx
numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

soma = 0
para (i = 0; i < tamanho(numeros); i = i + 1) {
    soma = soma + numeros[i]
}

media = soma / tamanho(numeros)
escreva("Soma: " + soma)
escreva("Média: " + media)
```

## Boas Práticas

### 1. Use Nomes Descritivos

```ulx
// ✓ Bom
idade_usuario = 25
nome_completo = "João Silva"

// ✗ Ruim
a = 25
n = "João Silva"
```

### 2. Adicione Comentários

```ulx
// Calcula a média de notas
soma = nota1 + nota2 + nota3
media = soma / 3
```

### 3. Use Funções para Reutilizar Código

```ulx
// ✓ Bom
funcao calcula_media(a, b, c) {
    retorna (a + b + c) / 3
}

m1 = calcula_media(7, 8, 9)
m2 = calcula_media(6, 7, 8)

// ✗ Ruim
m1 = (7 + 8 + 9) / 3
m2 = (6 + 7 + 8) / 3
```

### 4. Trate Erros

```ulx
tenta {
    arquivo = abre("/arquivo.txt")
    conteudo = le(arquivo)
    fecha(arquivo)
} captura (erro) {
    escreva("Erro ao ler arquivo: " + erro)
}
```

## Conclusão

**ULX é simples, mas poderosa!**

- ✅ Sintaxe intuitiva
- ✅ Sem complexidade desnecessária
- ✅ Funciona em qualquer Linux
- ✅ Performance de C puro

**Comece a programar agora!** 🚀
