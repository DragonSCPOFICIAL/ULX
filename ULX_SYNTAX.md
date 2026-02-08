# ULX - A Linguagem Mais Fácil do Mundo

## O Conceito

**ULX é tão fácil que parece mágica.**

Você escreve código simples e direto. O compilador CLX faz toda a complexidade invisível para você.

---

## Tudo que Você Precisa Saber

### 1. Imprimir Algo
```ulx
escreva("Olá!")
```

Pronto. É literalmente isso.

### 2. Guardar um Número
```ulx
x = 42
escreva(x)
```

### 3. Guardar um Texto
```ulx
nome = "Maria"
escreva(nome)
```

### 4. Fazer Contas
```ulx
a = 10
b = 20
c = a + b
escreva(c)
```

### 5. Tomar uma Decisão
```ulx
idade = 18

se (idade >= 18) {
    escreva("Você é maior de idade")
} senao {
    escreva("Você é menor de idade")
}
```

### 6. Repetir Algo
```ulx
para (i = 1; i <= 10; i = i + 1) {
    escreva(i)
}
```

### 7. Criar uma Função
```ulx
funcao saudar(nome) {
    escreva("Olá, " + nome)
}

saudar("João")
```

---

## Operadores (Só os Essenciais)

```
+   soma
-   subtração
*   multiplicação
/   divisão
%   resto da divisão

==  igual
!=  diferente
>   maior
<   menor
>=  maior ou igual
<=  menor ou igual

e   AND
ou  OR
nao NOT
```

---

## Palavras Mágicas (Reserve)

```
escreva        imprime na tela
leia           lê do teclado
se             condição
senao          senão
para           loop com contador
enquanto       loop com condição
funcao         define função
retorne        retorna valor
```

---

## Exemplos Reais (Super Simples)

### Exemplo 1: Hello World
```ulx
escreva("Olá, mundo!")
```

Fim. É tudo que você precisa.

### Exemplo 2: Seu Primeiro Programa
```ulx
nome = "você"
escreva("Bem-vindo, " + nome + "!")
escreva("Este é seu primeiro programa em ULX")
```

### Exemplo 3: Calculadora
```ulx
a = 10
b = 5

escreva(a + b)
escreva(a - b)
escreva(a * b)
escreva(a / b)
```

### Exemplo 4: Contagem
```ulx
para (i = 1; i <= 5; i = i + 1) {
    escreva(i)
}
```

### Exemplo 5: Adivinhação
```ulx
numero_secreto = 42
palpite = 50

se (palpite == numero_secreto) {
    escreva("Acertou!")
} senao {
    se (palpite > numero_secreto) {
        escreva("Seu palpite é maior")
    } senao {
        escreva("Seu palpite é menor")
    }
}
```

---

## O Segredo: CLX Faz a Mágica

Você escreve **código simples**. O compilador CLX:

1. **Analisa** o que você escreveu
2. **Otimiza** para ficar rápido
3. **Gera Assembly** (LNX) nativo para seu processador
4. **Cria um Binário** executável
5. **Integra com Linux** (syscalls, hardware, tudo)

**Você não precisa pensar em nada disso.**

---

## Regras Simples

1. **Sem ponto-e-vírgula** - quebra de linha é suficiente
2. **Indentação importa** - use espaços para blocos
3. **Tudo é simples** - sem tipos complexos, sem classes, sem herança
4. **Nomes claros** - `idade` em vez de `x`
5. **Comentários com `//`** - tudo depois é ignorado

---

## Filosofia

> "A linguagem deve ser tão fácil que uma criança consegue usar. A complexidade fica escondida no compilador."

ULX não é para impressionar programadores. É para **democratizar a programação**.

Se você consegue escrever um email, consegue escrever um programa em ULX.

---

## Próximos Passos

1. Instale ULX: `./INSTALL.sh`
2. Crie um arquivo `seu_programa.ulx`
3. Compile: `ulxc seu_programa.ulx`
4. Execute: `./seu_programa`

Pronto. Você criou um programa nativo que roda no Linux.

**Sem frameworks. Sem dependências. Sem complexidade.**

Só você e o poder do seu computador.
