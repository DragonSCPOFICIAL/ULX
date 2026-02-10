# 🚀 ULX - Plano Completo de Melhorias e Modernização

## 📋 Índice
1. [Análise do Projeto Atual](#análise-do-projeto-atual)
2. [Melhorias no Compilador (CLX)](#melhorias-no-compilador-clx)
3. [Melhorias na Linguagem (ULX)](#melhorias-na-linguagem-ulx)
4. [Melhorias no Sistema de Tipos](#melhorias-no-sistema-de-tipos)
5. [Otimizações de Performance](#otimizações-de-performance)
6. [Sistema de Módulos e Pacotes](#sistema-de-módulos-e-pacotes)
7. [Ferramentas de Desenvolvimento](#ferramentas-de-desenvolvimento)
8. [Sistema de Testes](#sistema-de-testes)
9. [Documentação e Exemplos](#documentação-e-exemplos)
10. [Roadmap de Implementação](#roadmap-de-implementação)

---

## 📊 Análise do Projeto Atual

### ✅ Pontos Fortes
- **Conceito inovador**: Linguagem simples que compila para binários Linux nativos
- **Arquitetura bem definida**: ULX → CLX → LNX
- **Performance**: Usa syscalls diretos do kernel
- **Compatibilidade**: Funciona em qualquer Linux
- **Sintaxe intuitiva**: Fácil de aprender para brasileiros

### ⚠️ Áreas que Precisam de Melhoria

#### 1. **Compilador (CLX)**
- Parser muito básico usando regex
- Sem análise semântica robusta
- Sem verificação de tipos
- Sem otimizações de código intermediário
- Mensagens de erro pouco informativas

#### 2. **Linguagem (ULX)**
- Falta suporte a muitas features prometidas (arrays, dicionários, funções)
- Não implementa tratamento de erros (try/catch)
- Sem suporte a módulos
- Sem gerenciamento de memória explícito

#### 3. **Tooling**
- Sem debugger
- Sem REPL
- Sem formatador de código
- Sem LSP (Language Server Protocol)
- Sem package manager

#### 4. **Documentação**
- Exemplos limitados
- Falta tutorial completo
- Sem documentação da API interna

---

## 🔧 Melhorias no Compilador (CLX)

### 1. Parser Robusto com AST

**Problema Atual:**
```python
# clx_compiler_intelligent.py linha 168
def parse_line(self, line):
    if line.startswith('escreva('):
        content = line[line.find('(')+1:line.rfind(')')]
        # Parsing muito frágil
```

**Solução: Implementar um Parser com AST (Abstract Syntax Tree)**

```python
# clx/parser.py
from dataclasses import dataclass
from typing import List, Union, Optional
from enum import Enum

class TokenType(Enum):
    # Literals
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    
    # Identifiers
    IDENTIFIER = "IDENTIFIER"
    
    # Keywords
    SE = "SE"
    SENAO = "SENAO"
    PARA = "PARA"
    ENQUANTO = "ENQUANTO"
    FUNCAO = "FUNCAO"
    RETORNA = "RETORNA"
    
    # Operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    MODULO = "MODULO"
    ASSIGN = "ASSIGN"
    
    # Comparisons
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    GREATER = "GREATER"
    LESS = "LESS"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS_EQUAL = "LESS_EQUAL"
    
    # Delimiters
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    COMMA = "COMMA"
    SEMICOLON = "SEMICOLON"
    
    # Special
    NEWLINE = "NEWLINE"
    EOF = "EOF"

@dataclass
class Token:
    type: TokenType
    value: any
    line: int
    column: int

class Lexer:
    """Tokenizador robusto para ULX"""
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
        self.keywords = {
            'se': TokenType.SE,
            'senao': TokenType.SENAO,
            'para': TokenType.PARA,
            'enquanto': TokenType.ENQUANTO,
            'funcao': TokenType.FUNCAO,
            'retorna': TokenType.RETORNA,
            'verdadeiro': TokenType.BOOLEAN,
            'falso': TokenType.BOOLEAN,
            'escreva': TokenType.IDENTIFIER,
            'le': TokenType.IDENTIFIER,
        }
    
    def current_char(self) -> Optional[str]:
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek_char(self, offset=1) -> Optional[str]:
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self):
        if self.current_char() == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        if self.current_char() == '/' and self.peek_char() == '/':
            # Single line comment
            while self.current_char() and self.current_char() != '\n':
                self.advance()
        elif self.current_char() == '/' and self.peek_char() == '*':
            # Multi-line comment
            self.advance()  # /
            self.advance()  # *
            while self.current_char():
                if self.current_char() == '*' and self.peek_char() == '/':
                    self.advance()  # *
                    self.advance()  # /
                    break
                self.advance()
    
    def read_number(self) -> Token:
        start_col = self.column
        num_str = ''
        has_dot = False
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if has_dot:
                    raise SyntaxError(f"Invalid number at line {self.line}, column {self.column}")
                has_dot = True
            num_str += self.current_char()
            self.advance()
        
        if has_dot:
            return Token(TokenType.FLOAT, float(num_str), self.line, start_col)
        else:
            return Token(TokenType.INTEGER, int(num_str), self.line, start_col)
    
    def read_string(self) -> Token:
        start_col = self.column
        quote_char = self.current_char()
        self.advance()  # Skip opening quote
        
        string_value = ''
        while self.current_char() and self.current_char() != quote_char:
            if self.current_char() == '\\':
                self.advance()
                # Handle escape sequences
                escape_chars = {
                    'n': '\n',
                    't': '\t',
                    'r': '\r',
                    '\\': '\\',
                    '"': '"',
                    "'": "'"
                }
                if self.current_char() in escape_chars:
                    string_value += escape_chars[self.current_char()]
                else:
                    string_value += self.current_char()
            else:
                string_value += self.current_char()
            self.advance()
        
        if not self.current_char():
            raise SyntaxError(f"Unterminated string at line {self.line}, column {start_col}")
        
        self.advance()  # Skip closing quote
        return Token(TokenType.STRING, string_value, self.line, start_col)
    
    def read_identifier(self) -> Token:
        start_col = self.column
        identifier = ''
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            identifier += self.current_char()
            self.advance()
        
        token_type = self.keywords.get(identifier, TokenType.IDENTIFIER)
        value = identifier
        
        if token_type == TokenType.BOOLEAN:
            value = identifier == 'verdadeiro'
        
        return Token(token_type, value, self.line, start_col)
    
    def tokenize(self) -> List[Token]:
        while self.current_char():
            self.skip_whitespace()
            
            if not self.current_char():
                break
            
            # Comments
            if self.current_char() == '/' and (self.peek_char() == '/' or self.peek_char() == '*'):
                self.skip_comment()
                continue
            
            # Newline
            if self.current_char() == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\n', self.line, self.column))
                self.advance()
                continue
            
            # Numbers
            if self.current_char().isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Strings
            if self.current_char() in '"\'':
                self.tokens.append(self.read_string())
                continue
            
            # Identifiers and keywords
            if self.current_char().isalpha() or self.current_char() == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Operators and delimiters
            char = self.current_char()
            next_char = self.peek_char()
            
            two_char_ops = {
                '==': TokenType.EQUAL,
                '!=': TokenType.NOT_EQUAL,
                '>=': TokenType.GREATER_EQUAL,
                '<=': TokenType.LESS_EQUAL,
            }
            
            if char + (next_char or '') in two_char_ops:
                self.tokens.append(Token(two_char_ops[char + next_char], char + next_char, self.line, self.column))
                self.advance()
                self.advance()
                continue
            
            single_char_ops = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '%': TokenType.MODULO,
                '=': TokenType.ASSIGN,
                '>': TokenType.GREATER,
                '<': TokenType.LESS,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                ',': TokenType.COMMA,
                ';': TokenType.SEMICOLON,
            }
            
            if char in single_char_ops:
                self.tokens.append(Token(single_char_ops[char], char, self.line, self.column))
                self.advance()
                continue
            
            raise SyntaxError(f"Unexpected character '{char}' at line {self.line}, column {self.column}")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens


# AST Nodes
@dataclass
class ASTNode:
    pass

@dataclass
class Program(ASTNode):
    statements: List[ASTNode]

@dataclass
class IntegerLiteral(ASTNode):
    value: int

@dataclass
class FloatLiteral(ASTNode):
    value: float

@dataclass
class StringLiteral(ASTNode):
    value: str

@dataclass
class BooleanLiteral(ASTNode):
    value: bool

@dataclass
class Identifier(ASTNode):
    name: str

@dataclass
class BinaryOp(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode

@dataclass
class UnaryOp(ASTNode):
    operator: str
    operand: ASTNode

@dataclass
class Assignment(ASTNode):
    target: str
    value: ASTNode

@dataclass
class FunctionCall(ASTNode):
    name: str
    arguments: List[ASTNode]

@dataclass
class IfStatement(ASTNode):
    condition: ASTNode
    then_block: List[ASTNode]
    else_block: Optional[List[ASTNode]]

@dataclass
class ForLoop(ASTNode):
    init: ASTNode
    condition: ASTNode
    increment: ASTNode
    body: List[ASTNode]

@dataclass
class WhileLoop(ASTNode):
    condition: ASTNode
    body: List[ASTNode]

@dataclass
class FunctionDef(ASTNode):
    name: str
    parameters: List[str]
    body: List[ASTNode]

@dataclass
class ReturnStatement(ASTNode):
    value: Optional[ASTNode]

@dataclass
class ArrayLiteral(ASTNode):
    elements: List[ASTNode]

@dataclass
class ArrayAccess(ASTNode):
    array: ASTNode
    index: ASTNode


class Parser:
    """Parser que constrói AST a partir dos tokens"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def current_token(self) -> Token:
        if self.pos >= len(self.tokens):
            return self.tokens[-1]  # EOF
        return self.tokens[self.pos]
    
    def peek_token(self, offset=1) -> Token:
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]  # EOF
        return self.tokens[pos]
    
    def advance(self):
        self.pos += 1
    
    def expect(self, token_type: TokenType) -> Token:
        token = self.current_token()
        if token.type != token_type:
            raise SyntaxError(
                f"Expected {token_type.value} but got {token.type.value} "
                f"at line {token.line}, column {token.column}"
            )
        self.advance()
        return token
    
    def skip_newlines(self):
        while self.current_token().type == TokenType.NEWLINE:
            self.advance()
    
    def parse(self) -> Program:
        statements = []
        while self.current_token().type != TokenType.EOF:
            self.skip_newlines()
            if self.current_token().type == TokenType.EOF:
                break
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        return Program(statements)
    
    def parse_statement(self) -> Optional[ASTNode]:
        self.skip_newlines()
        
        token = self.current_token()
        
        # Function definition
        if token.type == TokenType.FUNCAO:
            return self.parse_function_def()
        
        # Return statement
        if token.type == TokenType.RETORNA:
            return self.parse_return()
        
        # If statement
        if token.type == TokenType.SE:
            return self.parse_if()
        
        # For loop
        if token.type == TokenType.PARA:
            return self.parse_for()
        
        # While loop
        if token.type == TokenType.ENQUANTO:
            return self.parse_while()
        
        # Assignment or function call
        if token.type == TokenType.IDENTIFIER:
            # Look ahead to determine if assignment or function call
            if self.peek_token().type == TokenType.ASSIGN:
                return self.parse_assignment()
            elif self.peek_token().type == TokenType.LPAREN:
                return self.parse_function_call()
        
        return None
    
    def parse_function_def(self) -> FunctionDef:
        self.expect(TokenType.FUNCAO)
        name = self.expect(TokenType.IDENTIFIER).value
        
        self.expect(TokenType.LPAREN)
        parameters = []
        if self.current_token().type != TokenType.RPAREN:
            parameters.append(self.expect(TokenType.IDENTIFIER).value)
            while self.current_token().type == TokenType.COMMA:
                self.advance()
                parameters.append(self.expect(TokenType.IDENTIFIER).value)
        self.expect(TokenType.RPAREN)
        
        self.skip_newlines()
        self.expect(TokenType.LBRACE)
        
        body = []
        self.skip_newlines()
        while self.current_token().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()
        
        self.expect(TokenType.RBRACE)
        
        return FunctionDef(name, parameters, body)
    
    def parse_return(self) -> ReturnStatement:
        self.expect(TokenType.RETORNA)
        
        if self.current_token().type in [TokenType.NEWLINE, TokenType.RBRACE]:
            return ReturnStatement(None)
        
        value = self.parse_expression()
        return ReturnStatement(value)
    
    def parse_if(self) -> IfStatement:
        self.expect(TokenType.SE)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        self.skip_newlines()
        self.expect(TokenType.LBRACE)
        
        then_block = []
        self.skip_newlines()
        while self.current_token().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                then_block.append(stmt)
            self.skip_newlines()
        
        self.expect(TokenType.RBRACE)
        
        else_block = None
        if self.current_token().type == TokenType.SENAO:
            self.advance()
            self.skip_newlines()
            
            if self.current_token().type == TokenType.SE:
                # else if
                else_block = [self.parse_if()]
            else:
                self.expect(TokenType.LBRACE)
                else_block = []
                self.skip_newlines()
                while self.current_token().type != TokenType.RBRACE:
                    stmt = self.parse_statement()
                    if stmt:
                        else_block.append(stmt)
                    self.skip_newlines()
                self.expect(TokenType.RBRACE)
        
        return IfStatement(condition, then_block, else_block)
    
    def parse_for(self) -> ForLoop:
        self.expect(TokenType.PARA)
        self.expect(TokenType.LPAREN)
        
        init = self.parse_assignment()
        self.expect(TokenType.SEMICOLON)
        
        condition = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        
        increment = self.parse_assignment()
        self.expect(TokenType.RPAREN)
        
        self.skip_newlines()
        self.expect(TokenType.LBRACE)
        
        body = []
        self.skip_newlines()
        while self.current_token().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()
        
        self.expect(TokenType.RBRACE)
        
        return ForLoop(init, condition, increment, body)
    
    def parse_while(self) -> WhileLoop:
        self.expect(TokenType.ENQUANTO)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        self.skip_newlines()
        self.expect(TokenType.LBRACE)
        
        body = []
        self.skip_newlines()
        while self.current_token().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()
        
        self.expect(TokenType.RBRACE)
        
        return WhileLoop(condition, body)
    
    def parse_assignment(self) -> Assignment:
        target = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        return Assignment(target, value)
    
    def parse_function_call(self) -> FunctionCall:
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.LPAREN)
        
        arguments = []
        if self.current_token().type != TokenType.RPAREN:
            arguments.append(self.parse_expression())
            while self.current_token().type == TokenType.COMMA:
                self.advance()
                arguments.append(self.parse_expression())
        
        self.expect(TokenType.RPAREN)
        
        return FunctionCall(name, arguments)
    
    def parse_expression(self) -> ASTNode:
        return self.parse_comparison()
    
    def parse_comparison(self) -> ASTNode:
        left = self.parse_additive()
        
        while self.current_token().type in [
            TokenType.EQUAL, TokenType.NOT_EQUAL,
            TokenType.GREATER, TokenType.LESS,
            TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL
        ]:
            op = self.current_token().value
            self.advance()
            right = self.parse_additive()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_additive(self) -> ASTNode:
        left = self.parse_multiplicative()
        
        while self.current_token().type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token().value
            self.advance()
            right = self.parse_multiplicative()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_multiplicative(self) -> ASTNode:
        left = self.parse_unary()
        
        while self.current_token().type in [TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO]:
            op = self.current_token().value
            self.advance()
            right = self.parse_unary()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_unary(self) -> ASTNode:
        if self.current_token().type in [TokenType.MINUS, TokenType.PLUS]:
            op = self.current_token().value
            self.advance()
            operand = self.parse_unary()
            return UnaryOp(op, operand)
        
        return self.parse_primary()
    
    def parse_primary(self) -> ASTNode:
        token = self.current_token()
        
        # Integer
        if token.type == TokenType.INTEGER:
            self.advance()
            return IntegerLiteral(token.value)
        
        # Float
        if token.type == TokenType.FLOAT:
            self.advance()
            return FloatLiteral(token.value)
        
        # String
        if token.type == TokenType.STRING:
            self.advance()
            return StringLiteral(token.value)
        
        # Boolean
        if token.type == TokenType.BOOLEAN:
            self.advance()
            return BooleanLiteral(token.value)
        
        # Identifier or function call
        if token.type == TokenType.IDENTIFIER:
            if self.peek_token().type == TokenType.LPAREN:
                return self.parse_function_call()
            elif self.peek_token().type == TokenType.LBRACKET:
                # Array access
                name = self.expect(TokenType.IDENTIFIER).value
                self.expect(TokenType.LBRACKET)
                index = self.parse_expression()
                self.expect(TokenType.RBRACKET)
                return ArrayAccess(Identifier(name), index)
            else:
                self.advance()
                return Identifier(token.value)
        
        # Parentheses
        if token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        # Array literal
        if token.type == TokenType.LBRACKET:
            self.advance()
            elements = []
            if self.current_token().type != TokenType.RBRACKET:
                elements.append(self.parse_expression())
                while self.current_token().type == TokenType.COMMA:
                    self.advance()
                    elements.append(self.parse_expression())
            self.expect(TokenType.RBRACKET)
            return ArrayLiteral(elements)
        
        raise SyntaxError(
            f"Unexpected token {token.type.value} at line {token.line}, column {token.column}"
        )
```

### 2. Análise Semântica

```python
# clx/semantic_analyzer.py
from typing import Dict, Set, Optional
from clx.parser import *

class SymbolTable:
    """Tabela de símbolos para rastreamento de variáveis e funções"""
    
    def __init__(self, parent: Optional['SymbolTable'] = None):
        self.parent = parent
        self.symbols: Dict[str, dict] = {}
    
    def define(self, name: str, symbol_type: str, value_type: Optional[str] = None):
        """Define um símbolo na tabela atual"""
        self.symbols[name] = {
            'type': symbol_type,  # 'variable', 'function', 'parameter'
            'value_type': value_type,  # 'int', 'float', 'string', 'bool', 'array'
            'used': False
        }
    
    def lookup(self, name: str) -> Optional[dict]:
        """Procura um símbolo na tabela atual ou nas tabelas pai"""
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None
    
    def mark_used(self, name: str):
        """Marca um símbolo como usado"""
        if name in self.symbols:
            self.symbols[name]['used'] = True
        elif self.parent:
            self.parent.mark_used(name)


class SemanticAnalyzer:
    """Analisador semântico que verifica tipos, escopo e uso de variáveis"""
    
    def __init__(self):
        self.global_scope = SymbolTable()
        self.current_scope = self.global_scope
        self.errors = []
        self.warnings = []
        
        # Funções built-in
        self.register_builtins()
    
    def register_builtins(self):
        """Registra funções built-in do ULX"""
        builtins = [
            'escreva', 'le', 'abre', 'fecha', 'cria',
            'escreve', 'existe', 'deleta', 'tamanho',
            'substring', 'maiuscula', 'minuscula', 'trim',
            'split', 'join', 'adiciona', 'remove'
        ]
        
        for builtin in builtins:
            self.global_scope.define(builtin, 'function')
    
    def error(self, message: str):
        """Adiciona um erro semântico"""
        self.errors.append(message)
    
    def warning(self, message: str):
        """Adiciona um warning"""
        self.warnings.append(message)
    
    def analyze(self, ast: Program) -> bool:
        """Analisa o AST e retorna True se não houver erros"""
        self.visit_program(ast)
        
        # Verifica variáveis não usadas
        self.check_unused_symbols()
        
        return len(self.errors) == 0
    
    def check_unused_symbols(self):
        """Verifica símbolos definidos mas não usados"""
        def check_scope(scope: SymbolTable):
            for name, info in scope.symbols.items():
                if info['type'] == 'variable' and not info['used']:
                    self.warning(f"Variável '{name}' definida mas nunca usada")
        
        check_scope(self.global_scope)
    
    def push_scope(self):
        """Cria um novo escopo"""
        self.current_scope = SymbolTable(self.current_scope)
    
    def pop_scope(self):
        """Volta para o escopo anterior"""
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent
    
    def visit_program(self, node: Program):
        for statement in node.statements:
            self.visit(statement)
    
    def visit(self, node: ASTNode):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)
    
    def generic_visit(self, node: ASTNode):
        pass
    
    def visit_FunctionDef(self, node: FunctionDef):
        # Define a função no escopo atual
        self.current_scope.define(node.name, 'function')
        
        # Cria novo escopo para o corpo da função
        self.push_scope()
        
        # Define os parâmetros
        for param in node.parameters:
            self.current_scope.define(param, 'parameter')
        
        # Visita o corpo
        for stmt in node.body:
            self.visit(stmt)
        
        self.pop_scope()
    
    def visit_Assignment(self, node: Assignment):
        # Verifica se a variável já foi definida
        symbol = self.current_scope.lookup(node.target)
        
        if not symbol:
            # Define nova variável
            value_type = self.infer_type(node.value)
            self.current_scope.define(node.target, 'variable', value_type)
        
        # Visita o valor
        self.visit(node.value)
    
    def visit_Identifier(self, node: Identifier):
        symbol = self.current_scope.lookup(node.name)
        
        if not symbol:
            self.error(f"Variável '{node.name}' usada antes de ser definida")
        else:
            self.current_scope.mark_used(node.name)
    
    def visit_FunctionCall(self, node: FunctionCall):
        symbol = self.current_scope.lookup(node.name)
        
        if not symbol:
            self.error(f"Função '{node.name}' não definida")
        elif symbol['type'] != 'function':
            self.error(f"'{node.name}' não é uma função")
        
        # Visita os argumentos
        for arg in node.arguments:
            self.visit(arg)
    
    def visit_IfStatement(self, node: IfStatement):
        self.visit(node.condition)
        
        self.push_scope()
        for stmt in node.then_block:
            self.visit(stmt)
        self.pop_scope()
        
        if node.else_block:
            self.push_scope()
            for stmt in node.else_block:
                self.visit(stmt)
            self.pop_scope()
    
    def visit_ForLoop(self, node: ForLoop):
        self.push_scope()
        self.visit(node.init)
        self.visit(node.condition)
        self.visit(node.increment)
        
        for stmt in node.body:
            self.visit(stmt)
        
        self.pop_scope()
    
    def visit_WhileLoop(self, node: WhileLoop):
        self.visit(node.condition)
        
        self.push_scope()
        for stmt in node.body:
            self.visit(stmt)
        self.pop_scope()
    
    def visit_BinaryOp(self, node: BinaryOp):
        self.visit(node.left)
        self.visit(node.right)
    
    def visit_UnaryOp(self, node: UnaryOp):
        self.visit(node.operand)
    
    def visit_ArrayAccess(self, node: ArrayAccess):
        self.visit(node.array)
        self.visit(node.index)
    
    def infer_type(self, node: ASTNode) -> str:
        """Infere o tipo de uma expressão"""
        if isinstance(node, IntegerLiteral):
            return 'int'
        elif isinstance(node, FloatLiteral):
            return 'float'
        elif isinstance(node, StringLiteral):
            return 'string'
        elif isinstance(node, BooleanLiteral):
            return 'bool'
        elif isinstance(node, ArrayLiteral):
            return 'array'
        elif isinstance(node, Identifier):
            symbol = self.current_scope.lookup(node.name)
            if symbol:
                return symbol.get('value_type', 'unknown')
        
        return 'unknown'
```

### 3. Gerador de Código C Melhorado

```python
# clx/code_generator.py
from clx.parser import *
from typing import List

class CCodeGenerator:
    """Gerador de código C a partir do AST"""
    
    def __init__(self):
        self.indent_level = 0
        self.code = []
        self.temp_var_counter = 0
    
    def indent(self) -> str:
        return '    ' * self.indent_level
    
    def emit(self, code: str):
        self.code.append(self.indent() + code)
    
    def new_temp_var(self) -> str:
        var = f'_tmp{self.temp_var_counter}'
        self.temp_var_counter += 1
        return var
    
    def generate(self, ast: Program) -> str:
        # Headers
        self.emit('#include <stdio.h>')
        self.emit('#include <stdlib.h>')
        self.emit('#include <string.h>')
        self.emit('#include <stdbool.h>')
        self.emit('#include <math.h>')
        self.emit('')
        
        # Optimization pragmas
        self.emit('#pragma GCC optimize("O3")')
        self.emit('#pragma GCC optimize("Ofast")')
        self.emit('')
        
        # Generate function declarations
        for stmt in ast.statements:
            if isinstance(stmt, FunctionDef):
                self.generate_function_declaration(stmt)
        
        self.emit('')
        
        # Generate function definitions
        for stmt in ast.statements:
            if isinstance(stmt, FunctionDef):
                self.generate_function(stmt)
                self.emit('')
        
        # Generate main
        self.emit('int main() {')
        self.indent_level += 1
        
        for stmt in ast.statements:
            if not isinstance(stmt, FunctionDef):
                self.generate_statement(stmt)
        
        self.emit('return 0;')
        self.indent_level -= 1
        self.emit('}')
        
        return '\n'.join(self.code)
    
    def generate_function_declaration(self, node: FunctionDef):
        params = ', '.join(f'int {p}' for p in node.parameters)
        self.emit(f'int {node.name}({params});')
    
    def generate_function(self, node: FunctionDef):
        params = ', '.join(f'int {p}' for p in node.parameters)
        self.emit(f'int {node.name}({params}) {{')
        self.indent_level += 1
        
        for stmt in node.body:
            self.generate_statement(stmt)
        
        # Default return if no explicit return
        if not node.body or not isinstance(node.body[-1], ReturnStatement):
            self.emit('return 0;')
        
        self.indent_level -= 1
        self.emit('}')
    
    def generate_statement(self, node: ASTNode):
        if isinstance(node, Assignment):
            self.generate_assignment(node)
        elif isinstance(node, FunctionCall):
            self.generate_function_call(node)
            self.emit(';')
        elif isinstance(node, IfStatement):
            self.generate_if(node)
        elif isinstance(node, ForLoop):
            self.generate_for(node)
        elif isinstance(node, WhileLoop):
            self.generate_while(node)
        elif isinstance(node, ReturnStatement):
            self.generate_return(node)
    
    def generate_assignment(self, node: Assignment):
        value = self.generate_expression(node.value)
        # Simple type inference for declaration
        if isinstance(node.value, StringLiteral):
            self.emit(f'const char* {node.target} = {value};')
        else:
            self.emit(f'int {node.target} = {value};')
    
    def generate_function_call(self, node: FunctionCall) -> str:
        # Built-in functions mapping
        builtin_map = {
            'escreva': self.generate_print,
            'le': 'getchar()',
            'tamanho': 'strlen',
        }
        
        if node.name in builtin_map:
            if callable(builtin_map[node.name]):
                return builtin_map[node.name](node)
            else:
                args = ', '.join(self.generate_expression(arg) for arg in node.arguments)
                return f'{builtin_map[node.name]}({args})'
        
        # Regular function call
        args = ', '.join(self.generate_expression(arg) for arg in node.arguments)
        return f'{node.name}({args})'
    
    def generate_print(self, node: FunctionCall) -> str:
        """Gera código para função escreva()"""
        result = []
        for arg in node.arguments:
            if isinstance(arg, StringLiteral):
                result.append(f'printf("%s", {self.generate_expression(arg)})')
            elif isinstance(arg, IntegerLiteral) or isinstance(arg, BinaryOp):
                result.append(f'printf("%d", {self.generate_expression(arg)})')
            elif isinstance(arg, FloatLiteral):
                result.append(f'printf("%f", {self.generate_expression(arg)})')
            elif isinstance(arg, Identifier):
                # Assume integer for now
                result.append(f'printf("%d", {self.generate_expression(arg)})')
        
        return '; '.join(result)
    
    def generate_if(self, node: IfStatement):
        condition = self.generate_expression(node.condition)
        self.emit(f'if ({condition}) {{')
        self.indent_level += 1
        
        for stmt in node.then_block:
            self.generate_statement(stmt)
        
        self.indent_level -= 1
        self.emit('}')
        
        if node.else_block:
            self.emit('else {')
            self.indent_level += 1
            
            for stmt in node.else_block:
                self.generate_statement(stmt)
            
            self.indent_level -= 1
            self.emit('}')
    
    def generate_for(self, node: ForLoop):
        init = self.generate_assignment_expr(node.init)
        condition = self.generate_expression(node.condition)
        increment = self.generate_assignment_expr(node.increment)
        
        self.emit(f'for ({init}; {condition}; {increment}) {{')
        self.indent_level += 1
        
        for stmt in node.body:
            self.generate_statement(stmt)
        
        self.indent_level -= 1
        self.emit('}')
    
    def generate_while(self, node: WhileLoop):
        condition = self.generate_expression(node.condition)
        self.emit(f'while ({condition}) {{')
        self.indent_level += 1
        
        for stmt in node.body:
            self.generate_statement(stmt)
        
        self.indent_level -= 1
        self.emit('}')
    
    def generate_return(self, node: ReturnStatement):
        if node.value:
            value = self.generate_expression(node.value)
            self.emit(f'return {value};')
        else:
            self.emit('return 0;')
    
    def generate_expression(self, node: ASTNode) -> str:
        if isinstance(node, IntegerLiteral):
            return str(node.value)
        elif isinstance(node, FloatLiteral):
            return str(node.value)
        elif isinstance(node, StringLiteral):
            return f'"{node.value}"'
        elif isinstance(node, BooleanLiteral):
            return 'true' if node.value else 'false'
        elif isinstance(node, Identifier):
            return node.name
        elif isinstance(node, BinaryOp):
            left = self.generate_expression(node.left)
            right = self.generate_expression(node.right)
            return f'({left} {node.operator} {right})'
        elif isinstance(node, UnaryOp):
            operand = self.generate_expression(node.operand)
            return f'{node.operator}({operand})'
        elif isinstance(node, FunctionCall):
            return self.generate_function_call(node)
        elif isinstance(node, ArrayAccess):
            array = self.generate_expression(node.array)
            index = self.generate_expression(node.index)
            return f'{array}[{index}]'
        
        return '0'
    
    def generate_assignment_expr(self, node: Assignment) -> str:
        value = self.generate_expression(node.value)
        return f'int {node.target} = {value}'
```

### 4. Compilador Principal Melhorado

```python
# clx/compiler.py
#!/usr/bin/env python3
"""
CLX Compiler - Compilador Completo com AST
"""

import sys
import os
import subprocess
from clx.lexer import Lexer
from clx.parser import Parser
from clx.semantic_analyzer import SemanticAnalyzer
from clx.code_generator import CCodeGenerator
from clx.optimizer import Optimizer

class CLXCompiler:
    def __init__(self, source_file: str):
        self.source_file = source_file
        self.source = None
        self.ast = None
    
    def read_source(self) -> bool:
        try:
            with open(self.source_file, 'r', encoding='utf-8') as f:
                self.source = f.read()
            return True
        except FileNotFoundError:
            print(f"[CLX] ✗ Erro: Arquivo '{self.source_file}' não encontrado")
            return False
    
    def compile(self) -> bool:
        if not self.read_source():
            return False
        
        print("\n[CLX] ╔════════════════════════════════════════╗")
        print("[CLX] ║   COMPILADOR CLX - VERSÃO 2.0          ║")
        print("[CLX] ║   Com AST e Análise Semântica          ║")
        print("[CLX] ╚════════════════════════════════════════╝\n")
        
        # Fase 1: Análise Léxica
        print("[CLX] Fase 1: Análise Léxica (Tokenização)")
        try:
            lexer = Lexer(self.source)
            tokens = lexer.tokenize()
            print(f"[CLX] ✓ {len(tokens)} tokens gerados")
        except SyntaxError as e:
            print(f"[CLX] ✗ Erro de Sintaxe: {e}")
            return False
        
        # Fase 2: Análise Sintática
        print("\n[CLX] Fase 2: Análise Sintática (Construção do AST)")
        try:
            parser = Parser(tokens)
            self.ast = parser.parse()
            print(f"[CLX] ✓ AST construído com {len(self.ast.statements)} statements")
        except SyntaxError as e:
            print(f"[CLX] ✗ Erro de Sintaxe: {e}")
            return False
        
        # Fase 3: Análise Semântica
        print("\n[CLX] Fase 3: Análise Semântica")
        analyzer = SemanticAnalyzer()
        if not analyzer.analyze(self.ast):
            print("[CLX] ✗ Erros semânticos encontrados:")
            for error in analyzer.errors:
                print(f"[CLX]   - {error}")
            return False
        
        if analyzer.warnings:
            print("[CLX] ⚠ Avisos:")
            for warning in analyzer.warnings:
                print(f"[CLX]   - {warning}")
        
        print("[CLX] ✓ Análise semântica concluída")
        
        # Fase 4: Geração de Código C
        print("\n[CLX] Fase 4: Geração de Código C")
        generator = CCodeGenerator()
        c_code = generator.generate(self.ast)
        
        c_file = self.source_file.replace('.ulx', '.c')
        with open(c_file, 'w') as f:
            f.write(c_code)
        print(f"[CLX] ✓ Código C gerado: {c_file}")
        
        # Fase 5: Otimização
        print("\n[CLX] Fase 5: Otimização")
        optimizer = Optimizer()
        compiler_flags = optimizer.get_compiler_flags()
        print(f"[CLX] ✓ Flags de otimização: {' '.join(compiler_flags[:5])}...")
        
        # Fase 6: Compilação para Binário
        print("\n[CLX] Fase 6: Compilação para Binário Nativo")
        binary_file = self.source_file.replace('.ulx', '')
        
        compile_command = compiler_flags + ['-static', '-s', c_file, '-o', binary_file, '-lm']
        
        try:
            result = subprocess.run(
                compile_command,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                size = os.path.getsize(binary_file)
                print(f"[CLX] ✓ Binário gerado: {binary_file}")
                print(f"[CLX] ✓ Tamanho: {size:,} bytes")
                print(f"\n[CLX] ╔════════════════════════════════════════╗")
                print("[CLX] ║   COMPILAÇÃO BEM-SUCEDIDA              ║")
                print("[CLX] ╚════════════════════════════════════════╝")
                print(f"\n[CLX] Execute com: ./{binary_file}\n")
                return True
            else:
                print(f"[CLX] ✗ Erro na compilação:")
                print(result.stderr)
                return False
        
        except FileNotFoundError:
            print("[CLX] ✗ Erro: gcc não encontrado")
            return False


def main():
    if len(sys.argv) < 2:
        print("Uso: ulxc <arquivo.ulx>")
        sys.exit(1)
    
    source_file = sys.argv[1]
    
    compiler = CLXCompiler(source_file)
    success = compiler.compile()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
```

---

## 🎯 Melhorias na Linguagem (ULX)

### 1. Sistema de Tipos Mais Rico

**Adicionar suporte completo para:**

```ulx
// Tipos básicos
inteiro = 42
decimal = 3.14
texto = "Hello"
booleano = verdadeiro

// Arrays tipados
numeros: inteiro[] = [1, 2, 3, 4, 5]
nomes: texto[] = ["Ana", "João", "Maria"]

// Dicionários/Maps
pessoa: mapa<texto, any> = {
    "nome": "João",
    "idade": 30,
    "ativo": verdadeiro
}

// Tuplas
coordenada: (decimal, decimal) = (10.5, 20.3)

// Tipos customizados (structs)
tipo Pessoa {
    nome: texto
    idade: inteiro
    email: texto
}

joao: Pessoa = Pessoa {
    nome: "João",
    idade: 30,
    email: "joao@example.com"
}
```

### 2. Funções de Primeira Classe

```ulx
// Funções anônimas (lambdas)
dobro = (x) => x * 2
soma = (a, b) => a + b

// Higher-order functions
funcao aplicar(func, valor) {
    retorna func(valor)
}

resultado = aplicar(dobro, 5)  // 10

// Closures
funcao criar_contador() {
    contador = 0
    
    retorna () => {
        contador = contador + 1
        retorna contador
    }
}

contador = criar_contador()
escreva(contador())  // 1
escreva(contador())  // 2
```

### 3. Pattern Matching

```ulx
funcao descrever(valor) {
    corresponde valor {
        0 => escreva("Zero")
        1 => escreva("Um")
        2..10 => escreva("Entre 2 e 10")
        _ => escreva("Outro valor")
    }
}

// Pattern matching com tipos
funcao processar(dado) {
    corresponde tipo(dado) {
        "inteiro" => escreva("É um número")
        "texto" => escreva("É uma string")
        "array" => escreva("É um array")
    }
}
```

### 4. Operador de Pipeline

```ulx
// Pipeline operator |>
resultado = [1, 2, 3, 4, 5]
    |> map((x) => x * 2)
    |> filter((x) => x > 5)
    |> reduce((acc, x) => acc + x, 0)

// Equivalente a:
temp1 = map([1, 2, 3, 4, 5], (x) => x * 2)
temp2 = filter(temp1, (x) => x > 5)
resultado = reduce(temp2, (acc, x) => acc + x, 0)
```

### 5. Async/Await (Futuramente)

```ulx
// Funções assíncronas
async funcao buscar_dados(url) {
    resposta = await http_get(url)
    dados = await json_parse(resposta)
    retorna dados
}

// Uso
async funcao main() {
    dados = await buscar_dados("https://api.example.com/data")
    escreva(dados)
}
```

---

## 📦 Sistema de Módulos e Pacotes

### Estrutura de Módulos

```ulx
// math.ulx
modulo math

exporta funcao somar(a, b) {
    retorna a + b
}

exporta funcao subtrair(a, b) {
    retorna a - b
}

funcao privada() {
    // Função privada, não exportada
}

// main.ulx
importa math

resultado = math.somar(10, 20)
escreva(resultado)

// Ou importar funções específicas
importa { somar, subtrair } de math

resultado = somar(10, 20)
```

### Package Manager (ulxpkg)

```bash
# Inicializar projeto
ulxpkg init

# Adicionar dependência
ulxpkg add http@1.0.0

# Instalar dependências
ulxpkg install

# Publicar pacote
ulxpkg publish
```

### Arquivo ulxpkg.json

```json
{
  "name": "meu-projeto",
  "version": "1.0.0",
  "description": "Meu projeto ULX",
  "main": "main.ulx",
  "dependencies": {
    "http": "^1.0.0",
    "json": "^2.1.0"
  },
  "devDependencies": {
    "test": "^1.0.0"
  }
}
```

---

## 🛠️ Ferramentas de Desenvolvimento

### 1. REPL Interativo

```python
# ulx_repl.py
#!/usr/bin/env python3
"""
ULX REPL - Read-Eval-Print Loop
"""

import readline
import sys
from clx.compiler import CLXCompiler

class ULXREPL:
    def __init__(self):
        self.history = []
        self.variables = {}
    
    def run(self):
        print("╔════════════════════════════════════════╗")
        print("║   ULX REPL - Modo Interativo           ║")
        print("║   Digite 'sair' para encerrar          ║")
        print("╚════════════════════════════════════════╝\n")
        
        while True:
            try:
                line = input("ulx> ")
                
                if line.strip() == 'sair':
                    print("Até logo!")
                    break
                
                if not line.strip():
                    continue
                
                # Adiciona ao histórico
                self.history.append(line)
                
                # Compila e executa
                self.evaluate(line)
            
            except KeyboardInterrupt:
                print("\nDigite 'sair' para encerrar")
            except EOFError:
                print("\nAté logo!")
                break
    
    def evaluate(self, code: str):
        # Salva código temporário
        temp_file = '/tmp/ulx_repl_temp.ulx'
        with open(temp_file, 'w') as f:
            # Adiciona contexto de variáveis
            for var, value in self.variables.items():
                f.write(f'{var} = {value}\n')
            f.write(code + '\n')
        
        # Compila
        compiler = CLXCompiler(temp_file)
        if compiler.compile():
            # Executa
            import subprocess
            result = subprocess.run(['/tmp/ulx_repl_temp'], capture_output=True, text=True)
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)


if __name__ == '__main__':
    repl = ULXREPL()
    repl.run()
```

### 2. Formatador de Código (ulxfmt)

```python
# ulxfmt.py
#!/usr/bin/env python3
"""
ULX Formatter - Formatador automático de código
"""

from clx.parser import Parser, Lexer
from clx.ast_formatter import ASTFormatter

class ULXFormatter:
    def __init__(self, source_file: str):
        self.source_file = source_file
        self.config = {
            'indent_size': 4,
            'max_line_length': 100,
            'space_around_operators': True,
            'newline_before_brace': False
        }
    
    def format(self) -> str:
        # Lê o arquivo
        with open(self.source_file, 'r') as f:
            source = f.read()
        
        # Parse
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Formata
        formatter = ASTFormatter(self.config)
        formatted_code = formatter.format(ast)
        
        return formatted_code
    
    def format_and_save(self):
        formatted = self.format()
        with open(self.source_file, 'w') as f:
            f.write(formatted)
        print(f"[ulxfmt] ✓ Arquivo formatado: {self.source_file}")


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Uso: ulxfmt <arquivo.ulx>")
        sys.exit(1)
    
    formatter = ULXFormatter(sys.argv[1])
    formatter.format_and_save()
```

### 3. LSP (Language Server Protocol)

```python
# ulx_lsp.py
#!/usr/bin/env python3
"""
ULX Language Server - Suporte para IDEs
"""

from pygls.server import LanguageServer
from pygls.lsp.methods import (
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_COMPLETION,
    TEXT_DOCUMENT_HOVER,
)
from pygls.lsp.types import (
    CompletionItem,
    CompletionList,
    CompletionParams,
    DidOpenTextDocumentParams,
    DidChangeTextDocumentParams,
    Hover,
    TextDocumentPositionParams,
)

from clx.parser import Lexer, Parser
from clx.semantic_analyzer import SemanticAnalyzer

class ULXLanguageServer(LanguageServer):
    def __init__(self):
        super().__init__()


server = ULXLanguageServer()


@server.feature(TEXT_DOCUMENT_DID_OPEN)
async def did_open(ls: ULXLanguageServer, params: DidOpenTextDocumentParams):
    """Chamado quando um arquivo é aberto"""
    uri = params.text_document.uri
    source = params.text_document.text
    
    # Analisa o código
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        # Reporta erros
        diagnostics = []
        for error in analyzer.errors:
            # Criar diagnostics
            pass
        
        ls.publish_diagnostics(uri, diagnostics)
    
    except Exception as e:
        # Log error
        pass


@server.feature(TEXT_DOCUMENT_COMPLETION)
async def completion(ls: ULXLanguageServer, params: CompletionParams):
    """Autocompletar"""
    items = [
        CompletionItem(label='escreva'),
        CompletionItem(label='le'),
        CompletionItem(label='para'),
        CompletionItem(label='se'),
        CompletionItem(label='senao'),
        CompletionItem(label='funcao'),
        CompletionItem(label='retorna'),
    ]
    
    return CompletionList(is_incomplete=False, items=items)


@server.feature(TEXT_DOCUMENT_HOVER)
async def hover(ls: ULXLanguageServer, params: TextDocumentPositionParams):
    """Mostrar informações ao passar o mouse"""
    # Retorna informações sobre símbolo
    return Hover(contents="Documentação do símbolo")


if __name__ == '__main__':
    server.start_io()
```

---

## 🧪 Sistema de Testes

### Framework de Testes

```ulx
// test_math.ulx
importa { assert, teste, grupo } de "teste"
importa { somar, subtrair } de "math"

grupo("Operações Matemáticas") {
    
    teste("deve somar dois números") {
        resultado = somar(2, 3)
        assert(resultado == 5, "2 + 3 deve ser 5")
    }
    
    teste("deve subtrair dois números") {
        resultado = subtrair(10, 3)
        assert(resultado == 7, "10 - 3 deve ser 7")
    }
}
```

### Test Runner

```python
# ulx_test.py
#!/usr/bin/env python3
"""
ULX Test Runner - Executa testes
"""

import os
import sys
import subprocess
from pathlib import Path

class TestRunner:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.tests_total = 0
    
    def discover_tests(self, directory: str = '.'):
        """Descobre arquivos de teste"""
        test_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.startswith('test_') and file.endswith('.ulx'):
                    test_files.append(os.path.join(root, file))
        return test_files
    
    def run_test_file(self, test_file: str):
        """Executa um arquivo de teste"""
        print(f"\n📝 Executando: {test_file}")
        
        # Compila
        from clx.compiler import CLXCompiler
        compiler = CLXCompiler(test_file)
        
        if not compiler.compile():
            print(f"✗ Falha na compilação de {test_file}")
            self.tests_failed += 1
            return
        
        # Executa
        binary = test_file.replace('.ulx', '')
        result = subprocess.run([binary], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ Todos os testes passaram em {test_file}")
            self.tests_passed += 1
        else:
            print(f"✗ Testes falharam em {test_file}")
            print(result.stdout)
            print(result.stderr)
            self.tests_failed += 1
        
        self.tests_total += 1
    
    def run_all_tests(self):
        """Executa todos os testes"""
        test_files = self.discover_tests()
        
        if not test_files:
            print("Nenhum arquivo de teste encontrado")
            return
        
        print(f"╔════════════════════════════════════════╗")
        print(f"║   ULX Test Runner                      ║")
        print(f"║   {len(test_files)} arquivo(s) de teste encontrado(s)   ║")
        print(f"╚════════════════════════════════════════╝")
        
        for test_file in test_files:
            self.run_test_file(test_file)
        
        # Resumo
        print(f"\n╔════════════════════════════════════════╗")
        print(f"║   RESUMO DOS TESTES                    ║")
        print(f"╚════════════════════════════════════════╝")
        print(f"Total: {self.tests_total}")
        print(f"✓ Passou: {self.tests_passed}")
        print(f"✗ Falhou: {self.tests_failed}")
        
        return self.tests_failed == 0


if __name__ == '__main__':
    runner = TestRunner()
    success = runner.run_all_tests()
    sys.exit(0 if success else 1)
```

---

## ⚡ Otimizações de Performance

### 1. Otimizador de Código Intermediário

```python
# clx/optimizer.py
from clx.parser import *
from typing import List

class ASTOptimizer:
    """Otimizador de AST - elimina código morto, constantes, etc"""
    
    def __init__(self):
        self.optimizations_applied = []
    
    def optimize(self, ast: Program) -> Program:
        """Aplica todas as otimizações"""
        ast = self.constant_folding(ast)
        ast = self.dead_code_elimination(ast)
        ast = self.common_subexpression_elimination(ast)
        
        return ast
    
    def constant_folding(self, ast: Program) -> Program:
        """Avalia expressões constantes em tempo de compilação"""
        # Exemplo: x = 2 + 3 => x = 5
        
        class ConstantFolder:
            def visit(self, node):
                if isinstance(node, BinaryOp):
                    left = self.visit(node.left)
                    right = self.visit(node.right)
                    
                    # Se ambos são literais, avalia
                    if isinstance(left, IntegerLiteral) and isinstance(right, IntegerLiteral):
                        ops = {
                            '+': lambda a, b: a + b,
                            '-': lambda a, b: a - b,
                            '*': lambda a, b: a * b,
                            '/': lambda a, b: a // b,
                            '%': lambda a, b: a % b,
                        }
                        
                        if node.operator in ops:
                            result = ops[node.operator](left.value, right.value)
                            return IntegerLiteral(result)
                    
                    return BinaryOp(left, node.operator, right)
                
                elif isinstance(node, Program):
                    return Program([self.visit(stmt) for stmt in node.statements])
                
                elif isinstance(node, Assignment):
                    return Assignment(node.target, self.visit(node.value))
                
                # ... outros casos
                
                return node
        
        folder = ConstantFolder()
        return folder.visit(ast)
    
    def dead_code_elimination(self, ast: Program) -> Program:
        """Remove código que nunca é executado"""
        # Exemplo: código após return, condições sempre falsas
        
        # ... implementação
        
        return ast
    
    def common_subexpression_elimination(self, ast: Program) -> Program:
        """Elimina cálculos duplicados"""
        # Exemplo: x = a + b; y = a + b => temp = a + b; x = temp; y = temp
        
        # ... implementação
        
        return ast
```

### 2. Otimizações Específicas de Hardware

```python
# clx/hardware_optimizer.py
import subprocess
import os

class HardwareOptimizer:
    def __init__(self):
        self.cpu_info = self.detect_cpu()
        self.has_gpu = self.detect_gpu()
    
    def detect_cpu(self):
        """Detecta características da CPU"""
        info = {}
        
        try:
            with open('/proc/cpuinfo', 'r') as f:
                content = f.read()
                info['cores'] = os.cpu_count()
                info['avx'] = 'avx' in content
                info['avx2'] = 'avx2' in content
                info['avx512'] = 'avx512' in content
                info['sse4'] = 'sse4' in content
        except:
            pass
        
        return info
    
    def detect_gpu(self):
        """Detecta GPU disponível"""
        try:
            # NVIDIA
            result = subprocess.run(['nvidia-smi'], capture_output=True)
            if result.returncode == 0:
                return {'vendor': 'nvidia', 'cuda': True}
            
            # AMD
            result = subprocess.run(['rocm-smi'], capture_output=True)
            if result.returncode == 0:
                return {'vendor': 'amd', 'rocm': True}
        except:
            pass
        
        return None
    
    def get_optimal_flags(self):
        """Retorna flags de compilação otimizadas para o hardware"""
        flags = ['gcc', '-O3', '-Ofast']
        
        # CPU flags
        flags.extend(['-march=native', '-mtune=native'])
        
        if self.cpu_info.get('avx2'):
            flags.append('-mavx2')
        
        if self.cpu_info.get('avx512'):
            flags.append('-mavx512f')
        
        # Vetorização
        flags.extend([
            '-ftree-vectorize',
            '-ffast-math',
            '-funroll-loops',
        ])
        
        # LTO (Link Time Optimization)
        flags.append('-flto')
        
        # Profiling guiado (se disponível)
        if os.path.exists('profile.data'):
            flags.extend(['-fprofile-use', '-fprofile-correction'])
        
        return flags
```

---

## 📚 Documentação e Exemplos Expandidos

### Exemplos Práticos

#### 1. Servidor HTTP Completo

```ulx
// servidor_http.ulx
importa { socket, bind, listen, accept, send, recv, close } de "rede"
importa { thread } de "concorrencia"

funcao atender_cliente(cliente_socket) {
    // Lê requisição
    requisicao = recv(cliente_socket, 1024)
    
    // Parse HTTP
    linhas = split(requisicao, "\r\n")
    primeira_linha = linhas[0]
    partes = split(primeira_linha, " ")
    
    metodo = partes[0]
    caminho = partes[1]
    
    // Roteamento
    resposta = ""
    
    corresponde caminho {
        "/" => {
            resposta = "HTTP/1.1 200 OK\r\n"
            resposta += "Content-Type: text/html\r\n"
            resposta += "\r\n"
            resposta += "<h1>Bem-vindo ao servidor ULX!</h1>"
        }
        
        "/api/info" => {
            resposta = "HTTP/1.1 200 OK\r\n"
            resposta += "Content-Type: application/json\r\n"
            resposta += "\r\n"
            resposta += '{"servidor": "ULX", "versao": "1.0"}'
        }
        
        _ => {
            resposta = "HTTP/1.1 404 Not Found\r\n"
            resposta += "\r\n"
            resposta += "404 - Página não encontrada"
        }
    }
    
    // Envia resposta
    send(cliente_socket, resposta)
    close(cliente_socket)
}

funcao main() {
    // Cria socket
    servidor = socket()
    bind(servidor, "0.0.0.0", 8080)
    listen(servidor, 100)
    
    escreva("Servidor rodando em http://localhost:8080")
    
    // Loop de aceitação
    enquanto (verdadeiro) {
        cliente = accept(servidor)
        
        // Atende em thread separada
        thread(atender_cliente, cliente)
    }
}
```

#### 2. CLI Tool (Ferramenta de Linha de Comando)

```ulx
// cli_tool.ulx
importa { args, exit } de "sistema"
importa { exists, read_file, write_file } de "arquivo"

funcao mostrar_ajuda() {
    escreva("Uso: minha_tool [comando] [opções]")
    escreva("")
    escreva("Comandos:")
    escreva("  processar <arquivo>  - Processa um arquivo")
    escreva("  listar               - Lista arquivos")
    escreva("  ajuda                - Mostra esta ajuda")
}

funcao processar_arquivo(nome_arquivo) {
    se (!exists(nome_arquivo)) {
        escreva("Erro: Arquivo não encontrado")
        exit(1)
    }
    
    conteudo = read_file(nome_arquivo)
    linhas = split(conteudo, "\n")
    
    escreva(f"Processando {nome_arquivo}...")
    escreva(f"Total de linhas: {tamanho(linhas)}")
    
    // Processamento
    para (linha em linhas) {
        // Faz algo com cada linha
    }
    
    escreva("Concluído!")
}

funcao main() {
    se (tamanho(args) < 2) {
        mostrar_ajuda()
        exit(0)
    }
    
    comando = args[1]
    
    corresponde comando {
        "processar" => {
            se (tamanho(args) < 3) {
                escreva("Erro: Especifique um arquivo")
                exit(1)
            }
            processar_arquivo(args[2])
        }
        
        "listar" => {
            // ... implementação
        }
        
        "ajuda" => {
            mostrar_ajuda()
        }
        
        _ => {
            escreva(f"Comando desconhecido: {comando}")
            mostrar_ajuda()
            exit(1)
        }
    }
}
```

#### 3. Web Scraper

```ulx
// scraper.ulx
importa { http_get } de "http"
importa { parse_html, select } de "html"
importa { write_json } de "json"

funcao scrape_noticias(url) {
    // Busca página
    escreva(f"Buscando {url}...")
    html = http_get(url)
    
    // Parse HTML
    doc = parse_html(html)
    
    // Extrai notícias
    noticias = []
    artigos = select(doc, "article.noticia")
    
    para (artigo em artigos) {
        titulo = select(artigo, "h2.titulo").text()
        resumo = select(artigo, "p.resumo").text()
        link = select(artigo, "a").attr("href")
        
        noticias.adiciona({
            "titulo": titulo,
            "resumo": resumo,
            "link": link
        })
    }
    
    retorna noticias
}

funcao main() {
    url = "https://example.com/noticias"
    
    noticias = scrape_noticias(url)
    
    escreva(f"Encontradas {tamanho(noticias)} notícias")
    
    // Salva em JSON
    write_json("noticias.json", noticias)
    escreva("Salvo em noticias.json")
}
```

---

## 🗓️ Roadmap de Implementação

### Fase 1: Fundação (1-2 meses)

**Semana 1-2: Parser e AST**
- [ ] Implementar Lexer completo com todos os tokens
- [ ] Implementar Parser robusto com AST
- [ ] Testes unitários para parser

**Semana 3-4: Análise Semântica**
- [ ] Implementar tabela de símbolos
- [ ] Análise de escopo
- [ ] Verificação de tipos básica
- [ ] Detecção de variáveis não usadas

**Semana 5-6: Gerador de Código**
- [ ] Gerador de código C a partir do AST
- [ ] Suporte completo para todas as estruturas
- [ ] Otimizações básicas

**Semana 7-8: Testes e Integração**
- [ ] Suite de testes abrangente
- [ ] Integração com compilador atual
- [ ] Documentação

### Fase 2: Features da Linguagem (2-3 meses)

**Mês 1: Tipos e Estruturas**
- [ ] Sistema de tipos completo
- [ ] Arrays dinâmicos
- [ ] Dicionários/Maps
- [ ] Structs customizados
- [ ] Type checking robusto

**Mês 2: Funções Avançadas**
- [ ] Funções de primeira classe
- [ ] Closures
- [ ] Lambdas
- [ ] Pattern matching
- [ ] Operator overloading

**Mês 3: Módulos**
- [ ] Sistema de import/export
- [ ] Namespaces
- [ ] Package manager básico
- [ ] Repositório de pacotes

### Fase 3: Tooling (1-2 meses)

**Semana 1-2: REPL**
- [ ] REPL interativo
- [ ] Histórico de comandos
- [ ] Auto-completar

**Semana 3-4: Formatter e Linter**
- [ ] Formatador automático (ulxfmt)
- [ ] Linter com regras customizáveis
- [ ] Integração com editores

**Semana 5-6: LSP**
- [ ] Language Server Protocol
- [ ] Autocomplete inteligente
- [ ] Go to definition
- [ ] Find references
- [ ] Hover documentation

**Semana 7-8: Debugger**
- [ ] Debugger integrado
- [ ] Breakpoints
- [ ] Step through
- [ ] Inspect variables

### Fase 4: Performance e Otimizações (1-2 meses)

**Semana 1-2: Otimizador**
- [ ] Constant folding
- [ ] Dead code elimination
- [ ] Common subexpression elimination
- [ ] Loop unrolling

**Semana 3-4: JIT Compilation (Opcional)**
- [ ] Just-In-Time compilation para hot paths
- [ ] Profile-guided optimization
- [ ] Inline caching

**Semana 5-6: Otimizações de Hardware**
- [ ] Detecção automática de SIMD
- [ ] Vetorização automática
- [ ] Suporte a GPU (opcional)

**Semana 7-8: Benchmarks**
- [ ] Suite de benchmarks
- [ ] Comparação com outras linguagens
- [ ] Otimização baseada em perfil

### Fase 5: Ecossistema (2-3 meses)

**Mês 1: Standard Library**
- [ ] Biblioteca padrão completa
- [ ] Módulos de I/O
- [ ] Networking
- [ ] HTTP client/server
- [ ] JSON/XML parsing
- [ ] Criptografia
- [ ] Compressão

**Mês 2: Package Ecosystem**
- [ ] Package registry
- [ ] CLI para gerenciamento de pacotes
- [ ] Documentação automática
- [ ] Continuous Integration

**Mês 3: Documentação e Comunidade**
- [ ] Site oficial
- [ ] Tutorial completo
- [ ] Guia de estilo
- [ ] Exemplos práticos
- [ ] Blog e newsletter

---

## 📊 Métricas de Sucesso

### Performance
- [ ] Compilação 10x mais rápida que a versão atual
- [ ] Binários 20% menores
- [ ] Tempo de execução comparável a C
- [ ] Uso de memória otimizado

### Developer Experience
- [ ] Mensagens de erro claras e úteis
- [ ] Tempo de setup < 5 minutos
- [ ] IDE support completo
- [ ] Documentação completa

### Ecossistema
- [ ] 50+ pacotes na biblioteca padrão
- [ ] 100+ pacotes da comunidade
- [ ] 1000+ estrelas no GitHub
- [ ] Comunidade ativa

---

## 🎯 Conclusão

Este plano de melhorias transformará o ULX de uma linguagem experimental em uma linguagem de produção completa e poderosa. As melhorias propostas abordam todos os aspectos críticos:

1. **Compilador robusto** com parser, análise semântica e otimizações
2. **Linguagem expressiva** com features modernas
3. **Tooling profissional** (REPL, LSP, debugger, formatter)
4. **Performance otimizada** com otimizações inteligentes
5. **Ecossistema rico** com package manager e standard library
6. **Documentação completa** e exemplos práticos

O projeto ULX tem grande potencial e, com essas melhorias, pode se tornar uma alternativa real para desenvolvimento de sistemas em Linux!
