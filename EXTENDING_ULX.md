# Estendendo ULX - Criando Suas Próprias Linguagens

## Conceito

ULX é não apenas uma linguagem completa e independente, mas também uma **FUNDAÇÃO** para criar outras linguagens.

Se você quer criar sua própria linguagem com performance extrema, você pode:
1. Usar o compilador CLX como base
2. Estender a sintaxe ULX
3. Herdar toda a performance e otimizações

## Arquitetura Modular

```
┌─────────────────────────────────────┐
│         Sua Linguagem (XYZ)         │
│  (Estende ULX com novos recursos)   │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      CLX Compiler (Base)            │
│  (Otimizações, geração de código)   │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      LNX (Hardware/Linux)           │
│  (Binário nativo, performance)      │
└─────────────────────────────────────┘
```

## Como Estender ULX

### Passo 1: Copiar o Compilador

```bash
cp src/compiler/clx_compiler.py src/compiler/xyz_compiler.py
```

### Passo 2: Modificar o Parser

Adicione novos tipos de sintaxe ao método `parse_line()`:

```python
def parse_xyz_syntax(self, line):
    """Processa sintaxe específica de XYZ"""
    if line.startswith('xyz_comando'):
        # Sua lógica aqui
        return c_code
```

### Passo 3: Estender o Gerador de Código

Adicione novas otimizações ao `CLXOptimizer`:

```python
def xyz_optimization(self, code):
    """Otimização específica de XYZ"""
    # Sua otimização aqui
    return code
```

### Passo 4: Testar

```bash
python3 src/compiler/xyz_compiler.py seu_arquivo.xyz
```

## Exemplos de Extensão

### Exemplo 1: Adicionar Tipos de Dados

```python
def parse_line(self, line):
    # Suportar strings
    if 'texto' in line:
        # Processar como string
        pass
    
    # Suportar arrays
    if 'lista' in line:
        # Processar como array
        pass
```

### Exemplo 2: Adicionar Funções Avançadas

```python
def parse_funcao(self, line):
    """Processa definição de função"""
    if line.startswith('funcao'):
        match = re.search(r'funcao\s+(\w+)\s*\((.*?)\)', line)
        if match:
            name, params = match.groups()
            return f'int {name}({params}) {{'
```

### Exemplo 3: Adicionar Estruturas de Dados

```python
def parse_struct(self, line):
    """Processa estrutura de dados"""
    if line.startswith('estrutura'):
        # Gera struct em C
        pass
```

## Reutilizando Componentes ULX

### Usar o Otimizador

```python
from clx_compiler import CLXOptimizer

optimizer = CLXOptimizer()
code = optimizer.inline_constants(code)
code = optimizer.eliminate_dead_code(code)
```

### Usar o Gerador de Código

```python
from clx_compiler import CLXCompiler

compiler = CLXCompiler('seu_arquivo.xyz')
c_code = compiler.generate_c_code(tokens)
```

### Usar as Flags de Compilação

```python
compile_flags = [
    'gcc',
    '-O3',
    '-march=native',
    '-flto',
    '-ffast-math',
    # ... suas flags adicionais
]
```

## Estrutura de Diretórios para Extensões

```
ULX/
├── src/
│   ├── compiler/
│   │   ├── clx_compiler.py          (Base)
│   │   ├── xyz_compiler.py          (Sua extensão)
│   │   └── abc_compiler.py          (Outra extensão)
│   └── ...
├── examples/
│   ├── hello_world.ulx              (ULX)
│   ├── seu_programa.xyz             (Sua linguagem)
│   └── outro_programa.abc           (Outra linguagem)
├── docs/
│   ├── ULX_SYNTAX.md
│   ├── XYZ_SYNTAX.md                (Sua documentação)
│   └── ABC_SYNTAX.md
└── ...
```

## Boas Práticas

### 1. Manter Compatibilidade com ULX

Se sua linguagem estende ULX, garanta que código ULX válido também funcione em sua linguagem.

```python
# Bom: Estende ULX
class XYZCompiler(CLXCompiler):
    def parse_line(self, line):
        # Primeiro tenta sintaxe XYZ
        if line.startswith('xyz_'):
            return self.parse_xyz_syntax(line)
        
        # Depois tenta sintaxe ULX
        return super().parse_line(line)
```

### 2. Herdar Otimizações

```python
# Bom: Reutiliza otimizações
c_code = super().generate_c_code(tokens)
c_code = self.optimizer.xyz_optimization(c_code)
```

### 3. Documentar Sintaxe

Crie um arquivo `XYZ_SYNTAX.md` descrevendo sua linguagem.

### 4. Fornecer Exemplos

Crie exemplos em `examples/` mostrando como usar sua linguagem.

## Crescimento Exponencial

Quando você estende ULX:

1. **Você herda performance** - Todas as otimizações CLX
2. **Você herda velocidade** - Binários nativos ultra-rápidos
3. **Você herda comunidade** - Outros podem estender sua linguagem
4. **Você cria ecossistema** - Linguagens construídas sobre linguagens

```
ULX (Base)
├── XYZ (Estende ULX)
│   ├── XYZ+ (Estende XYZ)
│   └── XYZ-Web (Estende XYZ)
├── ABC (Estende ULX)
│   └── ABC-Game (Estende ABC)
└── DEF (Estende ULX)
```

## Contribuindo de Volta

Se você criar uma extensão interessante, considere:

1. Fazer um Pull Request para o repositório ULX
2. Documentar sua extensão
3. Fornecer exemplos
4. Ajudar a comunidade a usar sua linguagem

## Suporte

Para dúvidas sobre como estender ULX:

1. Veja os exemplos em `examples/`
2. Leia o código de `src/compiler/clx_compiler.py`
3. Estude `ULX_SYNTAX.md`
4. Crie sua própria extensão!

---

**Lembre-se:** ULX não é apenas uma linguagem, é uma PLATAFORMA para criar linguagens rápidas, leves e inteligentes.
