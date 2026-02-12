#!/usr/bin/env python3
"""
Parser ULX - Análise sintática da linguagem ULX
Usa Recursive Descent + Pratt Parsing para expressões
"""

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union, Any
from abc import ABC, abstractmethod


class TokenType(Enum):
    """Tipos de tokens da linguagem ULX"""
    # Palavras reservadas
    FUNCAO = "funcao"
    RETORNE = "retorne"
    SE = "se"
    SENAO = "senao"
    ENQUANTO = "enquanto"
    PARA = "para"
    FACA = "faca"
    ESCREVA = "escreva"
    LEIA = "leia"
    ABRE = "abre"
    FECHA = "fecha"
    LE = "le"
    VAR = "var"
    CONST = "const"
    INTEIRO = "inteiro"
    REAL = "real"
    TEXTO = "texto"
    BOOLEANO = "booleano"
    RETORNA = "retorna"
    
    # Literais
    NUMERO = auto()
    STRING = auto()
    BOOL = auto()
    
    # Identificadores
    IDENTIFICADOR = auto()
    
    # Operadores
    MAIS = "+"
    MENOS = "-"
    VEZES = "*"
    DIVIDIDO = "/"
    MODULO = "%"
    IGUAL = "=="
    DIFERENTE = "!="
    MENOR = "<"
    MAIOR = ">"
    MENOR_IGUAL = "<="
    MAIOR_IGUAL = ">="
    E = "&&"
    OU = "||"
    NAO = "!"
    ATRIBUICAO = "="
    
    # Delimitadores
    PARENTESE_ESQ = "("
    PARENTESE_DIR = ")"
    CHAVE_ESQ = "{"
    CHAVE_DIR = "}"
    COLCHETE_ESQ = "["
    COLCHETE_DIR = "]"
    PONTO_VIRGULA = ";"
    VIRGULA = ","
    PONTO = "."
    DOIS_PONTOS = ":"
    
    # Especiais
    NOVA_LINHA = auto()
    ESPACO = auto()
    TAB = auto()
    COMENTARIO = auto()
    EOF = auto()
    INVALIDO = auto()


@dataclass
class Token:
    """Token da linguagem ULX"""
    type: TokenType
    value: str
    line: int
    column: int
    
    def __str__(self):
        return f"Token({self.type}, '{self.value}', line={self.line}, col={self.column})"


class Lexer:
    """Analisador léxico (tokenizer) para ULX"""
    
    KEYWORDS = {
        'funcao': TokenType.FUNCAO,
        'retorne': TokenType.RETORNE,
        'se': TokenType.SE,
        'senao': TokenType.SENAO,
        'enquanto': TokenType.ENQUANTO,
        'para': TokenType.PARA,
        'faca': TokenType.FACA,
        'escreva': TokenType.ESCREVA,
        'leia': TokenType.LEIA,
        'abre': TokenType.ABRE,
        'fecha': TokenType.FECHA,
        'le': TokenType.LE,
        'var': TokenType.VAR,
        'const': TokenType.CONST,
        'inteiro': TokenType.INTEIRO,
        'real': TokenType.REAL,
        'texto': TokenType.TEXTO,
        'booleano': TokenType.BOOLEANO,
        'retorna': TokenType.RETORNA,
        'verdadeiro': TokenType.BOOL,
        'falso': TokenType.BOOL,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def error(self, msg: str):
        raise SyntaxError(f"{msg} at line {self.line}, column {self.column}")
    
    def peek(self, offset: int = 0) -> str:
        pos = self.pos + offset
        if pos >= len(self.source):
            return '\0'
        return self.source[pos]
    
    def advance(self) -> str:
        char = self.peek()
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def skip_whitespace(self):
        while self.peek() in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        if self.peek() == '/' and self.peek(1) == '/':
            while self.peek() != '\n' and self.peek() != '\0':
                self.advance()
        elif self.peek() == '/' and self.peek(1) == '*':
            self.advance()  # /
            self.advance()  # *
            while not (self.peek() == '*' and self.peek(1) == '/'):
                if self.peek() == '\0':
                    self.error("Unterminated comment")
                self.advance()
            self.advance()  # *
            self.advance()  # /
    
    def read_string(self) -> Token:
        start_line = self.line
        start_col = self.column
        self.advance()  # "
        value = ""
        while self.peek() != '"' and self.peek() != '\0':
            if self.peek() == '\\':
                self.advance()
                escape = self.advance()
                if escape == 'n':
                    value += '\n'
                elif escape == 't':
                    value += '\t'
                elif escape == '\\':
                    value += '\\'
                elif escape == '"':
                    value += '"'
                else:
                    self.error(f"Unknown escape sequence: \\{escape}")
            else:
                value += self.advance()
        if self.peek() != '"':
            self.error("Unterminated string")
        self.advance()  # "
        return Token(TokenType.STRING, value, start_line, start_col)
    
    def read_number(self) -> Token:
        start_line = self.line
        start_col = self.column
        value = ""
        is_float = False
        
        while self.peek().isdigit():
            value += self.advance()
        
        if self.peek() == '.' and self.peek(1).isdigit():
            is_float = True
            value += self.advance()  # .
            while self.peek().isdigit():
                value += self.advance()
        
        if self.peek() in 'eE':
            is_float = True
            value += self.advance()
            if self.peek() in '+-':
                value += self.advance()
            while self.peek().isdigit():
                value += self.advance()
        
        return Token(TokenType.NUMERO, value, start_line, start_col)
    
    def read_identifier(self) -> Token:
        start_line = self.line
        start_col = self.column
        value = ""
        
        while self.peek().isalnum() or self.peek() == '_':
            value += self.advance()
        
        token_type = self.KEYWORDS.get(value, TokenType.IDENTIFICADOR)
        return Token(token_type, value, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        while self.peek() != '\0':
            self.skip_whitespace()
            
            if self.peek() == '\0':
                break
            
            # Comentários
            if self.peek() == '/' and (self.peek(1) == '/' or self.peek(1) == '*'):
                self.skip_comment()
                continue
            
            start_line = self.line
            start_col = self.column
            char = self.peek()
            
            # Strings
            if char == '"':
                self.tokens.append(self.read_string())
                continue
            
            # Números
            if char.isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Identificadores
            if char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Operadores de dois caracteres
            two_char = char + self.peek(1)
            two_char_tokens = {
                '==': TokenType.IGUAL,
                '!=': TokenType.DIFERENTE,
                '<=': TokenType.MENOR_IGUAL,
                '>=': TokenType.MAIOR_IGUAL,
                '&&': TokenType.E,
                '||': TokenType.OU,
            }
            if two_char in two_char_tokens:
                self.advance()
                self.advance()
                self.tokens.append(Token(two_char_tokens[two_char], two_char, start_line, start_col))
                continue
            
            # Operadores e delimitadores de um caractere
            single_char_tokens = {
                '+': TokenType.MAIS,
                '-': TokenType.MENOS,
                '*': TokenType.VEZES,
                '/': TokenType.DIVIDIDO,
                '%': TokenType.MODULO,
                '<': TokenType.MENOR,
                '>': TokenType.MAIOR,
                '!': TokenType.NAO,
                '=': TokenType.ATRIBUICAO,
                '(': TokenType.PARENTESE_ESQ,
                ')': TokenType.PARENTESE_DIR,
                '{': TokenType.CHAVE_ESQ,
                '}': TokenType.CHAVE_DIR,
                '[': TokenType.COLCHETE_ESQ,
                ']': TokenType.COLCHETE_DIR,
                ';': TokenType.PONTO_VIRGULA,
                ',': TokenType.VIRGULA,
                '.': TokenType.PONTO,
                ':': TokenType.DOIS_PONTOS,
            }
            
            if char in single_char_tokens:
                self.advance()
                self.tokens.append(Token(single_char_tokens[char], char, start_line, start_col))
                continue
            
            # Nova linha
            if char == '\n':
                self.advance()
                continue
            
            self.error(f"Invalid character: {char}")
        
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens


# ==================== AST ====================

@dataclass
class ASTNode(ABC):
    """Nó base da AST"""
    pass


@dataclass
class Program(ASTNode):
    """Programa completo"""
    declarations: List[ASTNode] = field(default_factory=list)


@dataclass
class FunctionDecl(ASTNode):
    """Declaração de função"""
    name: str = ""
    params: List[tuple] = field(default_factory=list)  # (name, type)
    return_type: str = "void"
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class VarDecl(ASTNode):
    """Declaração de variável"""
    name: str = ""
    var_type: str = ""
    initializer: Optional[ASTNode] = None


@dataclass
class Expression(ASTNode, ABC):
    """Expressão base"""
    pass


@dataclass
class BinaryExpr(Expression):
    """Expressão binária"""
    left: Expression = None
    operator: str = ""
    right: Expression = None


@dataclass
class UnaryExpr(Expression):
    """Expressão unária"""
    operator: str = ""
    operand: Expression = None


@dataclass
class LiteralExpr(Expression):
    """Literal"""
    value: Any = None
    literal_type: str = ""


@dataclass
class IdentifierExpr(Expression):
    """Identificador"""
    name: str = ""


@dataclass
class CallExpr(Expression):
    """Chamada de função"""
    callee: str = ""
    arguments: List[Expression] = field(default_factory=list)


@dataclass
class AssignmentExpr(Expression):
    """Atribuição"""
    target: str = ""
    value: Expression = None


@dataclass
class Statement(ASTNode, ABC):
    """Statement base"""
    pass


@dataclass
class ExprStmt(Statement):
    """Statement de expressão"""
    expression: Expression = None


@dataclass
class IfStmt(Statement):
    """Statement if"""
    condition: Expression = None
    then_branch: List[Statement] = field(default_factory=list)
    else_branch: List[Statement] = field(default_factory=list)


@dataclass
class WhileStmt(Statement):
    """Statement while"""
    condition: Expression = None
    body: List[Statement] = field(default_factory=list)


@dataclass
class ForStmt(Statement):
    """Statement for"""
    init: Optional[Statement] = None
    condition: Optional[Expression] = None
    increment: Optional[Expression] = None
    body: List[Statement] = field(default_factory=list)


@dataclass
class ReturnStmt(Statement):
    """Statement return"""
    value: Optional[Expression] = None


@dataclass
class WriteStmt(Statement):
    """Statement escreva"""
    expression: Expression = None


@dataclass
class ReadStmt(Statement):
    """Statement leia"""
    target: str = ""


@dataclass
class OpenStmt(Statement):
    """Statement abre"""
    path: Expression = None


@dataclass
class CloseStmt(Statement):
    """Statement fecha"""
    target: str = ""


@dataclass
class ReadFileStmt(Statement):
    """Statement le (arquivo)"""
    target: str = ""


class Parser:
    """Parser Recursive Descent para ULX"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def error(self, msg: str):
        token = self.current()
        raise SyntaxError(f"{msg} at line {token.line}, column {token.column}")
    
    def current(self) -> Token:
        if self.pos >= len(self.tokens):
            return self.tokens[-1]  # EOF
        return self.tokens[self.pos]
    
    def peek(self, offset: int = 0) -> Token:
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[pos]
    
    def advance(self) -> Token:
        token = self.current()
        self.pos += 1
        return token
    
    def match(self, *types: TokenType) -> bool:
        return self.current().type in types
    
    def consume(self, type: TokenType, msg: str = None) -> Token:
        if not self.match(type):
            self.error(msg or f"Expected {type}")
        return self.advance()
    
    def parse(self) -> Program:
        """Entry point: parse programa completo"""
        program = Program()
        while not self.match(TokenType.EOF):
            program.declarations.append(self.declaration())
        return program
    
    def declaration(self) -> ASTNode:
        """Parse declaração (função ou variável)"""
        if self.match(TokenType.FUNCAO):
            return self.function_declaration()
        elif self.match(TokenType.VAR):
            return self.var_declaration()
        elif self.match(TokenType.CONST):
            return self.const_declaration()
        else:
            return self.statement()
    
    def function_declaration(self) -> FunctionDecl:
        """Parse declaração de função"""
        self.consume(TokenType.FUNCAO)
        name = self.consume(TokenType.IDENTIFICADOR, "Expected function name").value
        
        self.consume(TokenType.PARENTESE_ESQ)
        params = []
        if not self.match(TokenType.PARENTESE_DIR):
            while True:
                param_name = self.consume(TokenType.IDENTIFICADOR, "Expected parameter name").value
                param_type = "inteiro"  # Default type
                if self.match(TokenType.DOIS_PONTOS):
                    self.advance()
                    param_type = self.type_annotation()
                params.append((param_name, param_type))
                if not self.match(TokenType.VIRGULA):
                    break
                self.advance()
        self.consume(TokenType.PARENTESE_DIR)
        
        return_type = "void"
        if self.match(TokenType.DOIS_PONTOS):
            self.advance()
            return_type = self.type_annotation()
        
        self.consume(TokenType.CHAVE_ESQ)
        body = []
        while not self.match(TokenType.CHAVE_DIR):
            body.append(self.declaration())
        self.consume(TokenType.CHAVE_DIR)
        
        return FunctionDecl(name, params, return_type, body)
    
    def var_declaration(self) -> VarDecl:
        """Parse declaração de variável"""
        self.consume(TokenType.VAR)
        name = self.consume(TokenType.IDENTIFICADOR, "Expected variable name").value
        
        var_type = ""
        if self.match(TokenType.DOIS_PONTOS):
            self.advance()
            var_type = self.type_annotation()
        
        initializer = None
        if self.match(TokenType.ATRIBUICAO):
            self.advance()
            initializer = self.expression()
        
        self.consume(TokenType.PONTO_VIRGULA)
        return VarDecl(name, var_type, initializer)
    
    def const_declaration(self) -> VarDecl:
        """Parse declaração de constante"""
        self.consume(TokenType.CONST)
        name = self.consume(TokenType.IDENTIFICADOR, "Expected constant name").value
        
        const_type = ""
        if self.match(TokenType.DOIS_PONTOS):
            self.advance()
            const_type = self.type_annotation()
        
        self.consume(TokenType.ATRIBUICAO)
        initializer = self.expression()
        self.consume(TokenType.PONTO_VIRGULA)
        return VarDecl(name, const_type, initializer)
    
    def type_annotation(self) -> str:
        """Parse anotação de tipo"""
        if self.match(TokenType.INTEIRO):
            self.advance()
            return "inteiro"
        elif self.match(TokenType.REAL):
            self.advance()
            return "real"
        elif self.match(TokenType.TEXTO):
            self.advance()
            return "texto"
        elif self.match(TokenType.BOOLEANO):
            self.advance()
            return "booleano"
        else:
            self.error("Expected type annotation")
    
    def statement(self) -> Statement:
        """Parse statement"""
        if self.match(TokenType.SE):
            return self.if_statement()
        elif self.match(TokenType.ENQUANTO):
            return self.while_statement()
        elif self.match(TokenType.PARA):
            return self.for_statement()
        elif self.match(TokenType.RETORNE):
            return self.return_statement()
        elif self.match(TokenType.ESCREVA):
            return self.write_statement()
        elif self.match(TokenType.LEIA):
            return self.read_statement()
        elif self.match(TokenType.ABRE):
            return self.open_statement()
        elif self.match(TokenType.FECHA):
            return self.close_statement()
        elif self.match(TokenType.LE):
            return self.readfile_statement()
        else:
            return self.expression_statement()
    
    def if_statement(self) -> IfStmt:
        """Parse if statement"""
        self.consume(TokenType.SE)
        self.consume(TokenType.PARENTESE_ESQ)
        condition = self.expression()
        self.consume(TokenType.PARENTESE_DIR)
        
        self.consume(TokenType.CHAVE_ESQ)
        then_branch = []
        while not self.match(TokenType.CHAVE_DIR):
            then_branch.append(self.declaration())
        self.consume(TokenType.CHAVE_DIR)
        
        else_branch = []
        if self.match(TokenType.SENAO):
            self.advance()
            self.consume(TokenType.CHAVE_ESQ)
            while not self.match(TokenType.CHAVE_DIR):
                else_branch.append(self.declaration())
            self.consume(TokenType.CHAVE_DIR)
        
        return IfStmt(condition, then_branch, else_branch)
    
    def while_statement(self) -> WhileStmt:
        """Parse while statement"""
        self.consume(TokenType.ENQUANTO)
        self.consume(TokenType.PARENTESE_ESQ)
        condition = self.expression()
        self.consume(TokenType.PARENTESE_DIR)
        
        self.consume(TokenType.CHAVE_ESQ)
        body = []
        while not self.match(TokenType.CHAVE_DIR):
            body.append(self.declaration())
        self.consume(TokenType.CHAVE_DIR)
        
        return WhileStmt(condition, body)
    
    def for_statement(self) -> ForStmt:
        """Parse for statement"""
        self.consume(TokenType.PARA)
        self.consume(TokenType.PARENTESE_ESQ)
        
        init = None
        if not self.match(TokenType.PONTO_VIRGULA):
            if self.match(TokenType.VAR):
                init = self.var_declaration()
            else:
                init = self.expression_statement()
        else:
            self.consume(TokenType.PONTO_VIRGULA)
        
        condition = None
        if not self.match(TokenType.PONTO_VIRGULA):
            condition = self.expression()
        self.consume(TokenType.PONTO_VIRGULA)
        
        increment = None
        if not self.match(TokenType.PARENTESE_DIR):
            increment = self.expression()
        self.consume(TokenType.PARENTESE_DIR)
        
        self.consume(TokenType.CHAVE_ESQ)
        body = []
        while not self.match(TokenType.CHAVE_DIR):
            body.append(self.declaration())
        self.consume(TokenType.CHAVE_DIR)
        
        return ForStmt(init, condition, increment, body)
    
    def return_statement(self) -> ReturnStmt:
        """Parse return statement"""
        self.consume(TokenType.RETORNE)
        value = None
        if not self.match(TokenType.PONTO_VIRGULA):
            value = self.expression()
        self.consume(TokenType.PONTO_VIRGULA)
        return ReturnStmt(value)
    
    def write_statement(self) -> WriteStmt:
        """Parse escreva statement"""
        self.consume(TokenType.ESCREVA)
        self.consume(TokenType.PARENTESE_ESQ)
        expr = self.expression()
        self.consume(TokenType.PARENTESE_DIR)
        self.consume(TokenType.PONTO_VIRGULA)
        return WriteStmt(expr)
    
    def read_statement(self) -> ReadStmt:
        """Parse leia statement"""
        self.consume(TokenType.LEIA)
        self.consume(TokenType.PARENTESE_ESQ)
        target = self.consume(TokenType.IDENTIFICADOR, "Expected variable name").value
        self.consume(TokenType.PARENTESE_DIR)
        self.consume(TokenType.PONTO_VIRGULA)
        return ReadStmt(target)
    
    def open_statement(self) -> OpenStmt:
        """Parse abre statement"""
        self.consume(TokenType.ABRE)
        self.consume(TokenType.PARENTESE_ESQ)
        path = self.expression()
        self.consume(TokenType.PARENTESE_DIR)
        self.consume(TokenType.PONTO_VIRGULA)
        return OpenStmt(path)
    
    def close_statement(self) -> CloseStmt:
        """Parse fecha statement"""
        self.consume(TokenType.FECHA)
        self.consume(TokenType.PARENTESE_ESQ)
        target = self.consume(TokenType.IDENTIFICADOR, "Expected variable name").value
        self.consume(TokenType.PARENTESE_DIR)
        self.consume(TokenType.PONTO_VIRGULA)
        return CloseStmt(target)
    
    def readfile_statement(self) -> ReadFileStmt:
        """Parse le statement (arquivo)"""
        self.consume(TokenType.LE)
        self.consume(TokenType.PARENTESE_ESQ)
        target = self.consume(TokenType.IDENTIFICADOR, "Expected variable name").value
        self.consume(TokenType.PARENTESE_DIR)
        self.consume(TokenType.PONTO_VIRGULA)
        return ReadFileStmt(target)
    
    def expression_statement(self) -> ExprStmt:
        """Parse expression statement"""
        expr = self.expression()
        self.consume(TokenType.PONTO_VIRGULA)
        return ExprStmt(expr)
    
    # ==================== EXPRESSÕES (Pratt Parser) ====================
    
    def expression(self) -> Expression:
        """Parse expressão (precedência mais baixa)"""
        return self.assignment()
    
    def assignment(self) -> Expression:
        """Parse atribuição"""
        expr = self.or_expr()
        
        if self.match(TokenType.ATRIBUICAO):
            self.advance()
            value = self.assignment()
            if isinstance(expr, IdentifierExpr):
                return AssignmentExpr(expr.name, value)
            self.error("Invalid assignment target")
        
        return expr
    
    def or_expr(self) -> Expression:
        """Parse OR lógico"""
        expr = self.and_expr()
        while self.match(TokenType.OU):
            op = self.advance().value
            right = self.and_expr()
            expr = BinaryExpr(expr, op, right)
        return expr
    
    def and_expr(self) -> Expression:
        """Parse AND lógico"""
        expr = self.equality()
        while self.match(TokenType.E):
            op = self.advance().value
            right = self.equality()
            expr = BinaryExpr(expr, op, right)
        return expr
    
    def equality(self) -> Expression:
        """Parse igualdade"""
        expr = self.comparison()
        while self.match(TokenType.IGUAL, TokenType.DIFERENTE):
            op = self.advance().value
            right = self.comparison()
            expr = BinaryExpr(expr, op, right)
        return expr
    
    def comparison(self) -> Expression:
        """Parse comparação"""
        expr = self.term()
        while self.match(TokenType.MAIOR, TokenType.MAIOR_IGUAL, TokenType.MENOR, TokenType.MENOR_IGUAL):
            op = self.advance().value
            right = self.term()
            expr = BinaryExpr(expr, op, right)
        return expr
    
    def term(self) -> Expression:
        """Parse termo (+, -)"""
        expr = self.factor()
        while self.match(TokenType.MAIS, TokenType.MENOS):
            op = self.advance().value
            right = self.factor()
            expr = BinaryExpr(expr, op, right)
        return expr
    
    def factor(self) -> Expression:
        """Parse fator (*, /, %)"""
        expr = self.unary()
        while self.match(TokenType.VEZES, TokenType.DIVIDIDO, TokenType.MODULO):
            op = self.advance().value
            right = self.unary()
            expr = BinaryExpr(expr, op, right)
        return expr
    
    def unary(self) -> Expression:
        """Parse unário (!, -)"""
        if self.match(TokenType.NAO, TokenType.MENOS):
            op = self.advance().value
            operand = self.unary()
            return UnaryExpr(op, operand)
        return self.call()
    
    def call(self) -> Expression:
        """Parse chamada de função"""
        expr = self.primary()
        
        while self.match(TokenType.PARENTESE_ESQ):
            self.advance()
            if isinstance(expr, IdentifierExpr):
                args = []
                if not self.match(TokenType.PARENTESE_DIR):
                    while True:
                        args.append(self.expression())
                        if not self.match(TokenType.VIRGULA):
                            break
                        self.advance()
                self.consume(TokenType.PARENTESE_DIR)
                expr = CallExpr(expr.name, args)
            else:
                self.error("Can only call functions")
        
        return expr
    
    def primary(self) -> Expression:
        """Parse primário (literal, identificador, grupo)"""
        if self.match(TokenType.BOOL):
            value = self.advance().value
            return LiteralExpr(value == "verdadeiro", "booleano")
        
        if self.match(TokenType.NUMERO):
            token = self.advance()
            if '.' in token.value or 'e' in token.value.lower():
                return LiteralExpr(float(token.value), "real")
            return LiteralExpr(int(token.value), "inteiro")
        
        if self.match(TokenType.STRING):
            return LiteralExpr(self.advance().value, "texto")
        
        if self.match(TokenType.IDENTIFICADOR):
            return IdentifierExpr(self.advance().value)
        
        if self.match(TokenType.PARENTESE_ESQ):
            self.advance()
            expr = self.expression()
            self.consume(TokenType.PARENTESE_DIR)
            return expr
        
        self.error(f"Unexpected token: {self.current().value}")


def parse_source(source: str) -> Program:
    """Função utilitária para parse de código fonte ULX"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()


if __name__ == "__main__":
    # Teste
    source = """
    funcao main() {
        var x: inteiro = 10;
        var y = 20;
        
        se (x < y) {
            escreva(x);
        } senao {
            escreva(y);
        }
        
        retorne 0;
    }
    """
    
    try:
        ast = parse_source(source)
        print("Parse successful!")
        print(f"Declarations: {len(ast.declarations)}")
    except SyntaxError as e:
        print(f"Error: {e}")
