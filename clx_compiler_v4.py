#!/usr/bin/env python3
"""
CLX Compiler V4 — Consolidação da Linguagem
============================================
Melhorias sobre V3:

  [1] Sistema de erros profissional
      - Linha + coluna em TODOS os erros/warnings
      - Classificação: FATAL / ERROR / WARNING / INFO
      - Relatório de diagnóstico ao final
      - Compilação não aborta em warnings

  [2] Spec da linguagem embutida
      - Tipos oficiais: int, float, bool, texto
      - Palavras-chave reservadas validadas
      - Regras de escopo aplicadas com clareza
      - Erros de redeclaração no mesmo escopo (fatal)
      - Coerção implícita int↔float permitida; resto é erro

  [3] Built-ins padronizados e documentados
      - escreva(...)        → printf com \n automático
      - escreva_fmt(fmt, .)  → printf direto
      - leia()              → fgets de stdin → texto
      - leia_int()          → scanf %d → int
      - leia_float()        → scanf %lf → float
      - tamanho(s)          → strlen → int
      - tipo_de(x)          → string literal com o tipo (tempo de compilação)
      - para_int(x)         → atoi / cast
      - para_float(x)       → atof / cast
      - sair(code)          → exit(code)
      - (mais em BUILTINS abaixo)

  [4] Diagnósticos
      - Resumo de erros ao final da compilação
      - --check-only: só valida sem compilar
      - --print-ast: imprime AST em texto
      - --print-c: mostra C gerado sem compilar
"""

import sys
import os
import subprocess
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple, Set
from enum import Enum


# ═══════════════════════════════════════════════════════════
# DIAGNÓSTICOS
# ═══════════════════════════════════════════════════════════

class Severity(Enum):
    INFO    = "INFO"
    WARNING = "WARNING"
    ERROR   = "ERRO"
    FATAL   = "FATAL"


@dataclass
class Diagnostic:
    severity: Severity
    message:  str
    line:     int  = 0
    column:   int  = 0
    hint:     str  = ""

    def __str__(self) -> str:
        loc  = f"linha {self.line}, col {self.column}" if self.line else "—"
        base = f"[{self.severity.value}] ({loc}) {self.message}"
        if self.hint:
            base += f"\n        → Dica: {self.hint}"
        return base


class Diagnostics:
    """Coletor central de diagnósticos."""

    def __init__(self, filename: str = ""):
        self.filename = filename
        self.items: List[Diagnostic] = []

    def add(self, sev: Severity, msg: str, line=0, col=0, hint=""):
        d = Diagnostic(sev, msg, line, col, hint)
        self.items.append(d)
        # warnings e infos: só acumulam
        # erros e fatais: print imediato para feedback rápido
        if sev in (Severity.ERROR, Severity.FATAL):
            print(f"  {d}")

    def info   (self, msg, line=0, col=0, hint=""): self.add(Severity.INFO,    msg, line, col, hint)
    def warning(self, msg, line=0, col=0, hint=""): self.add(Severity.WARNING, msg, line, col, hint)
    def error  (self, msg, line=0, col=0, hint=""): self.add(Severity.ERROR,   msg, line, col, hint)
    def fatal  (self, msg, line=0, col=0, hint=""): self.add(Severity.FATAL,   msg, line, col, hint)

    def has_errors(self) -> bool:
        return any(d.severity in (Severity.ERROR, Severity.FATAL) for d in self.items)

    def report(self):
        errors   = [d for d in self.items if d.severity in (Severity.ERROR, Severity.FATAL)]
        warnings = [d for d in self.items if d.severity == Severity.WARNING]

        if not errors and not warnings:
            print("[CLX] ✓ Nenhum problema encontrado.")
            return

        if warnings:
            print(f"\n[CLX] ── {len(warnings)} aviso(s) ──")
            for w in warnings:
                print(f"  {w}")

        if errors:
            print(f"\n[CLX] ── {len(errors)} erro(s) ──")
            # já foram impressos na hora, só conta


# ═══════════════════════════════════════════════════════════
# TOKEN TYPES
# ═══════════════════════════════════════════════════════════

class TokenType(Enum):
    # Literals
    INTEGER    = "INTEGER"
    FLOAT      = "FLOAT"
    STRING     = "STRING"
    BOOLEAN    = "BOOLEAN"
    NULL       = "NULL"

    # Keywords
    SE         = "se"
    SENAO      = "senao"
    PARA       = "para"
    ENQUANTO   = "enquanto"
    FACA       = "faca"        # do-while futuro
    FUNCAO     = "funcao"
    RETORNA    = "retorna"
    PARE       = "pare"        # break
    CONTINUA   = "continua"   # continue
    VAR        = "var"         # declaração explícita
    CONST      = "const"

    # Types (como palavras-chave de anotação)
    T_INT      = "int"
    T_FLOAT    = "float"
    T_BOOL     = "bool"
    T_TEXTO    = "texto"

    # Identifiers
    IDENTIFIER = "IDENTIFIER"

    # Arithmetic
    PLUS       = "+"
    MINUS      = "-"
    MULTIPLY   = "*"
    DIVIDE     = "/"
    MODULO     = "%"

    # Assignment
    ASSIGN     = "="
    PLUS_EQ    = "+="
    MINUS_EQ   = "-="
    MULT_EQ    = "*="
    DIV_EQ     = "/="

    # Comparison
    EQUAL         = "=="
    NOT_EQUAL     = "!="
    GREATER       = ">"
    LESS          = "<"
    GREATER_EQUAL = ">="
    LESS_EQUAL    = "<="

    # Logical
    AND = "&&"
    OR  = "||"
    NOT = "!"

    # Delimiters
    LPAREN    = "("
    RPAREN    = ")"
    LBRACE    = "{"
    RBRACE    = "}"
    LBRACKET  = "["
    RBRACKET  = "]"
    SEMICOLON = ";"
    COMMA     = ","
    COLON     = ":"
    DOT       = "."

    # Special
    NEWLINE = "NEWLINE"
    EOF     = "EOF"


# Palavras reservadas que NÃO podem ser usadas como identificadores
RESERVED_WORDS: Set[str] = {
    'se', 'senao', 'para', 'enquanto', 'faca',
    'funcao', 'retorna', 'pare', 'continua',
    'var', 'const',
    'int', 'float', 'bool', 'texto',
    'verdadeiro', 'falso', 'nulo',
}


@dataclass
class Token:
    type:   TokenType
    value:  object
    line:   int = 1
    column: int = 1

    def pos_str(self) -> str:
        return f"linha {self.line}, col {self.column}"


# ═══════════════════════════════════════════════════════════
# LEXER
# ═══════════════════════════════════════════════════════════

class Lexer:
    def __init__(self, source: str, diag: Diagnostics):
        self.source = source
        self.diag   = diag
        self.pos    = 0
        self.line   = 1
        self.column = 1
        self.keywords: Dict[str, TokenType] = {
            'se':        TokenType.SE,
            'senao':     TokenType.SENAO,
            'para':      TokenType.PARA,
            'enquanto':  TokenType.ENQUANTO,
            'faca':      TokenType.FACA,
            'funcao':    TokenType.FUNCAO,
            'retorna':   TokenType.RETORNA,
            'pare':      TokenType.PARE,
            'continua':  TokenType.CONTINUA,
            'var':       TokenType.VAR,
            'const':     TokenType.CONST,
            'int':       TokenType.T_INT,
            'float':     TokenType.T_FLOAT,
            'bool':      TokenType.T_BOOL,
            'texto':     TokenType.T_TEXTO,
            'verdadeiro':TokenType.BOOLEAN,
            'falso':     TokenType.BOOLEAN,
            'nulo':      TokenType.NULL,
        }

    def cur(self) -> Optional[str]:
        return self.source[self.pos] if self.pos < len(self.source) else None

    def peek(self, n=1) -> Optional[str]:
        p = self.pos + n
        return self.source[p] if p < len(self.source) else None

    def advance(self):
        if self.cur() == '\n':
            self.line  += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1

    def skip_ws(self):
        while self.cur() and self.cur() in ' \t\r':
            self.advance()

    def skip_line_comment(self):
        while self.cur() and self.cur() != '\n':
            self.advance()

    def skip_block_comment(self):
        """/* ... */"""
        start_line = self.line
        self.advance(); self.advance()  # skip /*
        while self.cur():
            if self.cur() == '*' and self.peek() == '/':
                self.advance(); self.advance()
                return
            self.advance()
        self.diag.error("Comentário de bloco não fechado", start_line)

    def read_number(self) -> Token:
        s   = ''
        dot = False
        col = self.column
        ln  = self.line
        while self.cur() and (self.cur().isdigit() or self.cur() == '.'):
            if self.cur() == '.':
                if dot:
                    break
                # garante que não é range operator futuro
                if self.peek() and not self.peek().isdigit():
                    break
                dot = True
            s += self.cur()
            self.advance()
        if dot:
            return Token(TokenType.FLOAT, float(s), ln, col)
        return Token(TokenType.INTEGER, int(s), ln, col)

    def read_string(self) -> Token:
        quote = self.cur()
        col   = self.column
        ln    = self.line
        self.advance()
        value   = ''
        escapes = {'n': '\n', 't': '\t', 'r': '\r',
                   '\\': '\\', '"': '"', "'": "'", '0': '\0'}
        while self.cur() and self.cur() != quote:
            if self.cur() == '\n':
                self.diag.error("String não fechada antes do fim da linha", ln, col)
                break
            if self.cur() == '\\':
                self.advance()
                ch = self.cur()
                if ch in escapes:
                    value += escapes[ch]
                else:
                    self.diag.warning(f"Sequência de escape desconhecida '\\{ch}'", self.line, self.column)
                    value += ch
            else:
                value += self.cur()
            self.advance()
        self.advance()  # closing quote
        return Token(TokenType.STRING, value, ln, col)

    def read_identifier(self) -> Token:
        col  = self.column
        ln   = self.line
        name = ''
        while self.cur() and (self.cur().isalnum() or self.cur() == '_'):
            name += self.cur()
            self.advance()
        tt  = self.keywords.get(name, TokenType.IDENTIFIER)
        val = name
        if tt == TokenType.BOOLEAN:
            val = (name == 'verdadeiro')
        if tt == TokenType.NULL:
            val = None
        return Token(tt, val, ln, col)

    def tokenize(self) -> List[Token]:
        tokens = []
        two_char: Dict[str, TokenType] = {
            '==': TokenType.EQUAL,      '!=': TokenType.NOT_EQUAL,
            '>=': TokenType.GREATER_EQUAL, '<=': TokenType.LESS_EQUAL,
            '&&': TokenType.AND,        '||': TokenType.OR,
            '+=': TokenType.PLUS_EQ,   '-=': TokenType.MINUS_EQ,
            '*=': TokenType.MULT_EQ,   '/=': TokenType.DIV_EQ,
        }
        single: Dict[str, TokenType] = {
            '+': TokenType.PLUS,  '-': TokenType.MINUS,
            '*': TokenType.MULTIPLY, '/': TokenType.DIVIDE,
            '%': TokenType.MODULO,  '=': TokenType.ASSIGN,
            '>': TokenType.GREATER, '<': TokenType.LESS,
            '(': TokenType.LPAREN,  ')': TokenType.RPAREN,
            '{': TokenType.LBRACE,  '}': TokenType.RBRACE,
            '[': TokenType.LBRACKET,']': TokenType.RBRACKET,
            ';': TokenType.SEMICOLON, ',': TokenType.COMMA,
            ':': TokenType.COLON,   '.': TokenType.DOT,
            '!': TokenType.NOT,
        }

        while self.cur():
            self.skip_ws()
            if not self.cur():
                break

            # comentários
            if self.cur() == '/' and self.peek() == '/':
                self.skip_line_comment(); continue
            if self.cur() == '/' and self.peek() == '*':
                self.skip_block_comment(); continue

            if self.cur() == '\n':
                tokens.append(Token(TokenType.NEWLINE, '\n', self.line, self.column))
                self.advance(); continue

            if self.cur().isdigit():
                tokens.append(self.read_number()); continue

            if self.cur() in '"\'':
                tokens.append(self.read_string()); continue

            if self.cur().isalpha() or self.cur() == '_':
                tokens.append(self.read_identifier()); continue

            two = self.cur() + (self.peek() or '')
            if two in two_char:
                tokens.append(Token(two_char[two], two, self.line, self.column))
                self.advance(); self.advance(); continue

            if self.cur() in single:
                tokens.append(Token(single[self.cur()], self.cur(), self.line, self.column))
                self.advance(); continue

            self.diag.warning(
                f"Caractere desconhecido '{self.cur()}'",
                self.line, self.column
            )
            self.advance()

        tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return tokens


# ═══════════════════════════════════════════════════════════
# AST NODES
# ═══════════════════════════════════════════════════════════

@dataclass
class ASTNode:
    line:   int = field(default=0, compare=False, repr=False)
    column: int = field(default=0, compare=False, repr=False)

@dataclass
class Program(ASTNode):
    statements: List[ASTNode] = field(default_factory=list)

@dataclass
class IntegerLiteral(ASTNode):
    value: int = 0

@dataclass
class FloatLiteral(ASTNode):
    value: float = 0.0

@dataclass
class StringLiteral(ASTNode):
    value: str = ""

@dataclass
class BooleanLiteral(ASTNode):
    value: bool = False

@dataclass
class NullLiteral(ASTNode):
    pass

@dataclass
class Identifier(ASTNode):
    name: str = ""

@dataclass
class BinaryOp(ASTNode):
    left:     ASTNode = field(default_factory=lambda: IntegerLiteral())
    operator: str     = "+"
    right:    ASTNode = field(default_factory=lambda: IntegerLiteral())

@dataclass
class UnaryOp(ASTNode):
    operator: str    = "!"
    operand:  ASTNode = field(default_factory=lambda: IntegerLiteral())

@dataclass
class Assignment(ASTNode):
    target:   str    = ""
    value:    ASTNode = field(default_factory=lambda: IntegerLiteral())
    compound: str    = ""   # "", "+=", "-=", "*=", "/="

@dataclass
class VarDecl(ASTNode):
    """Declaração explícita: var x: int = expr  /  var x = expr"""
    name:      str              = ""
    type_hint: Optional[str]   = None   # "int" | "float" | "bool" | "texto" | None
    value:     Optional[ASTNode] = None
    is_const:  bool            = False

@dataclass
class FunctionCall(ASTNode):
    name:      str           = ""
    arguments: List[ASTNode] = field(default_factory=list)

@dataclass
class IfStatement(ASTNode):
    condition:  ASTNode          = field(default_factory=lambda: BooleanLiteral())
    then_block: List[ASTNode]    = field(default_factory=list)
    else_block: Optional[List[ASTNode]] = None

@dataclass
class ForLoop(ASTNode):
    init:      ASTNode       = field(default_factory=lambda: IntegerLiteral())
    condition: ASTNode       = field(default_factory=lambda: BooleanLiteral())
    increment: ASTNode       = field(default_factory=lambda: IntegerLiteral())
    body:      List[ASTNode] = field(default_factory=list)

@dataclass
class WhileLoop(ASTNode):
    condition: ASTNode       = field(default_factory=lambda: BooleanLiteral())
    body:      List[ASTNode] = field(default_factory=list)

@dataclass
class FunctionDecl(ASTNode):
    name:       str                     = ""
    params:     List[Tuple[str, Optional[str]]] = field(default_factory=list)  # (name, type_hint)
    return_hint:Optional[str]           = None
    body:       List[ASTNode]           = field(default_factory=list)

@dataclass
class ReturnStatement(ASTNode):
    value: Optional[ASTNode] = None

@dataclass
class BreakStatement(ASTNode):
    pass

@dataclass
class ContinueStatement(ASTNode):
    pass


# ═══════════════════════════════════════════════════════════
# PARSER
# ═══════════════════════════════════════════════════════════

class Parser:
    def __init__(self, tokens: List[Token], diag: Diagnostics):
        self.tokens = tokens
        self.diag   = diag
        self.pos    = 0

    def cur(self) -> Token:
        return self.tokens[min(self.pos, len(self.tokens) - 1)]

    def peek_next(self) -> Token:
        return self.tokens[min(self.pos + 1, len(self.tokens) - 1)]

    def peek2(self) -> Token:
        return self.tokens[min(self.pos + 2, len(self.tokens) - 1)]

    def advance(self) -> Token:
        t = self.cur()
        self.pos += 1
        return t

    def expect(self, tt: TokenType) -> Token:
        if self.cur().type != tt:
            self.diag.error(
                f"Esperado '{tt.value}', encontrado '{self.cur().value}' ({self.cur().type.value})",
                self.cur().line, self.cur().column,
                hint=f"Verifique a sintaxe perto de '{self.cur().value}'"
            )
            # recovery: não avança, deixa o caller continuar
            return self.cur()
        return self.advance()

    def match(self, *types: TokenType) -> bool:
        return self.cur().type in types

    def skip_newlines(self):
        while self.match(TokenType.NEWLINE):
            self.advance()

    def skip_semi_newlines(self):
        while self.match(TokenType.NEWLINE, TokenType.SEMICOLON):
            self.advance()

    # ── top level ─────────────────────────────────────────

    def parse(self) -> Program:
        prog = Program(line=1, column=1)
        while not self.match(TokenType.EOF):
            self.skip_semi_newlines()
            if self.match(TokenType.EOF): break
            s = self.parse_statement()
            if s:
                prog.statements.append(s)
            self.skip_semi_newlines()
        return prog

    def parse_statement(self) -> Optional[ASTNode]:
        self.skip_newlines()
        t = self.cur()

        if t.type == TokenType.FUNCAO:
            return self.parse_function_decl()
        if t.type == TokenType.SE:
            return self.parse_if()
        if t.type == TokenType.PARA:
            return self.parse_for()
        if t.type == TokenType.ENQUANTO:
            return self.parse_while()
        if t.type == TokenType.RETORNA:
            return self.parse_return()
        if t.type == TokenType.PARE:
            self.advance()
            return BreakStatement(line=t.line, column=t.column)
        if t.type == TokenType.CONTINUA:
            self.advance()
            return ContinueStatement(line=t.line, column=t.column)
        if t.type in (TokenType.VAR, TokenType.CONST):
            return self.parse_var_decl()
        if t.type == TokenType.IDENTIFIER:
            return self.parse_identifier_stmt()

        # token irreconhecível — pula para não travar
        self.diag.warning(
            f"Token inesperado '{t.value}' ignorado",
            t.line, t.column
        )
        self.advance()
        return None

    # ── declarations ──────────────────────────────────────

    def parse_var_decl(self) -> VarDecl:
        is_const = self.cur().type == TokenType.CONST
        t = self.advance()  # var / const
        name_tok = self.expect(TokenType.IDENTIFIER)
        type_hint = None
        if self.match(TokenType.COLON):
            self.advance()
            type_hint = self._read_type_hint()
        value = None
        if self.match(TokenType.ASSIGN):
            self.advance()
            value = self.parse_expression()
        return VarDecl(
            name=name_tok.value, type_hint=type_hint,
            value=value, is_const=is_const,
            line=t.line, column=t.column
        )

    def _read_type_hint(self) -> str:
        t = self.cur()
        if t.type in (TokenType.T_INT, TokenType.T_FLOAT,
                      TokenType.T_BOOL, TokenType.T_TEXTO,
                      TokenType.IDENTIFIER):
            self.advance()
            return str(t.value)
        self.diag.error(
            f"Tipo desconhecido '{t.value}'", t.line, t.column,
            hint="Tipos válidos: int, float, bool, texto"
        )
        return "int"

    def parse_function_decl(self) -> FunctionDecl:
        t = self.advance()  # 'funcao'
        name_tok = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.LPAREN)
        params = []
        if not self.match(TokenType.RPAREN):
            params.append(self._read_param())
            while self.match(TokenType.COMMA):
                self.advance()
                params.append(self._read_param())
        self.expect(TokenType.RPAREN)
        return_hint = None
        if self.match(TokenType.COLON):
            self.advance()
            return_hint = self._read_type_hint()
        self.skip_newlines()
        self.expect(TokenType.LBRACE)
        body = self.parse_block()
        self.expect(TokenType.RBRACE)
        return FunctionDecl(
            name=name_tok.value, params=params,
            return_hint=return_hint, body=body,
            line=t.line, column=t.column
        )

    def _read_param(self) -> Tuple[str, Optional[str]]:
        name = self.expect(TokenType.IDENTIFIER).value
        hint = None
        if self.match(TokenType.COLON):
            self.advance()
            hint = self._read_type_hint()
        return (name, hint)

    # ── control flow ──────────────────────────────────────

    def parse_if(self) -> IfStatement:
        t = self.advance()
        self.expect(TokenType.LPAREN)
        cond = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.skip_newlines()
        self.expect(TokenType.LBRACE)
        then_block = self.parse_block()
        self.expect(TokenType.RBRACE)
        else_block = None
        self.skip_newlines()
        if self.match(TokenType.SENAO):
            self.advance()
            self.skip_newlines()
            # suporta "senao se" (else-if)
            if self.match(TokenType.SE):
                else_block = [self.parse_if()]
            else:
                self.expect(TokenType.LBRACE)
                else_block = self.parse_block()
                self.expect(TokenType.RBRACE)
        return IfStatement(condition=cond, then_block=then_block, else_block=else_block,
                           line=t.line, column=t.column)

    def parse_while(self) -> WhileLoop:
        t = self.advance()
        self.expect(TokenType.LPAREN)
        cond = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.skip_newlines()
        self.expect(TokenType.LBRACE)
        body = self.parse_block()
        self.expect(TokenType.RBRACE)
        return WhileLoop(condition=cond, body=body, line=t.line, column=t.column)

    def parse_for(self) -> ForLoop:
        t = self.advance()
        self.expect(TokenType.LPAREN)
        init = self._parse_for_clause()
        self.expect(TokenType.SEMICOLON)
        cond = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        inc  = self._parse_for_clause()
        self.expect(TokenType.RPAREN)
        self.skip_newlines()
        self.expect(TokenType.LBRACE)
        body = self.parse_block()
        self.expect(TokenType.RBRACE)
        return ForLoop(init=init, condition=cond, increment=inc, body=body,
                       line=t.line, column=t.column)

    def _parse_for_clause(self) -> ASTNode:
        if self.match(TokenType.VAR):
            return self.parse_var_decl()
        if (self.match(TokenType.IDENTIFIER) and
                self.peek_next().type in (TokenType.ASSIGN, TokenType.PLUS_EQ,
                                          TokenType.MINUS_EQ, TokenType.MULT_EQ,
                                          TokenType.DIV_EQ)):
            return self.parse_identifier_stmt()
        return self.parse_expression()

    def parse_return(self) -> ReturnStatement:
        t = self.advance()
        value = None
        if not self.match(TokenType.NEWLINE, TokenType.SEMICOLON,
                          TokenType.RBRACE, TokenType.EOF):
            value = self.parse_expression()
        return ReturnStatement(value=value, line=t.line, column=t.column)

    def parse_block(self) -> List[ASTNode]:
        stmts = []
        self.skip_semi_newlines()
        while not self.match(TokenType.RBRACE, TokenType.EOF):
            s = self.parse_statement()
            if s:
                stmts.append(s)
            self.skip_semi_newlines()
        return stmts

    # ── identifier statements ─────────────────────────────

    def parse_identifier_stmt(self) -> Optional[ASTNode]:
        t    = self.advance()   # identifier
        name = t.value

        # compound assignment: x += expr
        compound_map = {
            TokenType.PLUS_EQ:  "+=",
            TokenType.MINUS_EQ: "-=",
            TokenType.MULT_EQ:  "*=",
            TokenType.DIV_EQ:   "/=",
        }
        if self.cur().type in compound_map:
            op = compound_map[self.advance().type]
            val = self.parse_expression()
            return Assignment(target=name, value=val, compound=op,
                              line=t.line, column=t.column)

        if self.match(TokenType.ASSIGN):
            self.advance()
            val = self.parse_expression()
            return Assignment(target=name, value=val, compound="",
                              line=t.line, column=t.column)

        if self.match(TokenType.LPAREN):
            self.advance()
            args = self._parse_args()
            self.expect(TokenType.RPAREN)
            return FunctionCall(name=name, arguments=args,
                                line=t.line, column=t.column)

        return Identifier(name=name, line=t.line, column=t.column)

    def _parse_args(self) -> List[ASTNode]:
        args = []
        if not self.match(TokenType.RPAREN):
            args.append(self.parse_expression())
            while self.match(TokenType.COMMA):
                self.advance()
                args.append(self.parse_expression())
        return args

    # ── expressions ───────────────────────────────────────

    def parse_expression(self) -> ASTNode:
        return self.parse_logical_or()

    def parse_logical_or(self) -> ASTNode:
        left = self.parse_logical_and()
        while self.match(TokenType.OR):
            op   = self.advance().value
            left = BinaryOp(left=left, operator=op, right=self.parse_logical_and())
        return left

    def parse_logical_and(self) -> ASTNode:
        left = self.parse_comparison()
        while self.match(TokenType.AND):
            op   = self.advance().value
            left = BinaryOp(left=left, operator=op, right=self.parse_comparison())
        return left

    def parse_comparison(self) -> ASTNode:
        left = self.parse_additive()
        while self.match(TokenType.EQUAL, TokenType.NOT_EQUAL,
                         TokenType.GREATER, TokenType.LESS,
                         TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL):
            op   = self.advance().value
            left = BinaryOp(left=left, operator=op, right=self.parse_additive())
        return left

    def parse_additive(self) -> ASTNode:
        left = self.parse_multiplicative()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op   = self.advance().value
            left = BinaryOp(left=left, operator=op, right=self.parse_multiplicative())
        return left

    def parse_multiplicative(self) -> ASTNode:
        left = self.parse_unary()
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op   = self.advance().value
            left = BinaryOp(left=left, operator=op, right=self.parse_unary())
        return left

    def parse_unary(self) -> ASTNode:
        if self.match(TokenType.NOT):
            t = self.advance()
            return UnaryOp(operator='!', operand=self.parse_unary(),
                           line=t.line, column=t.column)
        if self.match(TokenType.MINUS):
            t = self.advance()
            return UnaryOp(operator='-', operand=self.parse_unary(),
                           line=t.line, column=t.column)
        return self.parse_primary()

    def parse_primary(self) -> ASTNode:
        t = self.cur()

        if t.type == TokenType.INTEGER:
            self.advance(); return IntegerLiteral(value=t.value, line=t.line, column=t.column)
        if t.type == TokenType.FLOAT:
            self.advance(); return FloatLiteral(value=t.value, line=t.line, column=t.column)
        if t.type == TokenType.STRING:
            self.advance(); return StringLiteral(value=t.value, line=t.line, column=t.column)
        if t.type == TokenType.BOOLEAN:
            self.advance(); return BooleanLiteral(value=t.value, line=t.line, column=t.column)
        if t.type == TokenType.NULL:
            self.advance(); return NullLiteral(line=t.line, column=t.column)

        if t.type == TokenType.IDENTIFIER:
            name = self.advance().value
            if self.match(TokenType.LPAREN):
                self.advance()
                args = self._parse_args()
                self.expect(TokenType.RPAREN)
                return FunctionCall(name=name, arguments=args, line=t.line, column=t.column)
            return Identifier(name=name, line=t.line, column=t.column)

        if t.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr

        self.diag.warning(
            f"Expressão inesperada '{t.value}' — usando 0",
            t.line, t.column
        )
        self.advance()
        return IntegerLiteral(value=0, line=t.line, column=t.column)


# ═══════════════════════════════════════════════════════════
# TIPO SYSTEM
# ═══════════════════════════════════════════════════════════

class CLXType(Enum):
    INT     = "int"
    FLOAT   = "float"
    BOOL    = "bool"
    TEXTO   = "texto"    # string
    VOID    = "void"
    UNKNOWN = "?"

_C_TYPE = {
    CLXType.INT:   "int",
    CLXType.FLOAT: "double",
    CLXType.BOOL:  "bool",
    CLXType.TEXTO: "char*",
    CLXType.VOID:  "void",
}

_HINT_MAP: Dict[str, CLXType] = {
    "int":   CLXType.INT,
    "float": CLXType.FLOAT,
    "bool":  CLXType.BOOL,
    "texto": CLXType.TEXTO,
}

def c_type(t: CLXType) -> str:
    return _C_TYPE.get(t, "int")

def printf_fmt(t: CLXType) -> str:
    return {
        CLXType.INT:   "%d",
        CLXType.FLOAT: "%g",
        CLXType.BOOL:  "%d",
        CLXType.TEXTO: "%s",
    }.get(t, "%d")

def hint_to_type(hint: Optional[str]) -> CLXType:
    if hint is None: return CLXType.UNKNOWN
    return _HINT_MAP.get(hint, CLXType.UNKNOWN)

def promote(a: CLXType, b: CLXType) -> CLXType:
    if a == CLXType.FLOAT or b == CLXType.FLOAT: return CLXType.FLOAT
    if a == CLXType.INT   or b == CLXType.INT:   return CLXType.INT
    if a == CLXType.BOOL  or b == CLXType.BOOL:  return CLXType.BOOL
    return CLXType.TEXTO

def coercible(from_: CLXType, to: CLXType) -> bool:
    """Retorna True se a coerção implícita é permitida."""
    if from_ == to: return True
    if from_ == CLXType.UNKNOWN or to == CLXType.UNKNOWN: return True
    # int ↔ float: ok
    if {from_, to} == {CLXType.INT, CLXType.FLOAT}: return True
    # int → bool: ok (qualquer inteiro vira bool)
    if from_ == CLXType.INT and to == CLXType.BOOL: return True
    return False


# ═══════════════════════════════════════════════════════════
# TABELA DE SÍMBOLOS
# ═══════════════════════════════════════════════════════════

@dataclass
class Symbol:
    name:     str
    type:     CLXType
    is_const: bool = False
    is_param: bool = False
    line:     int  = 0

@dataclass
class FuncSig:
    name:        str
    param_types: List[CLXType]
    return_type: CLXType
    is_builtin:  bool = False

# Built-ins registrados
_BUILTINS: Dict[str, FuncSig] = {
    'escreva':       FuncSig('escreva',       [],               CLXType.VOID,  True),
    'escreva_fmt':   FuncSig('escreva_fmt',   [],               CLXType.VOID,  True),
    'leia':          FuncSig('leia',          [],               CLXType.TEXTO, True),
    'leia_int':      FuncSig('leia_int',      [],               CLXType.INT,   True),
    'leia_float':    FuncSig('leia_float',    [],               CLXType.FLOAT, True),
    'tamanho':       FuncSig('tamanho',       [CLXType.TEXTO],  CLXType.INT,   True),
    'tipo_de':       FuncSig('tipo_de',       [CLXType.UNKNOWN],CLXType.TEXTO, True),
    'para_int':      FuncSig('para_int',      [CLXType.UNKNOWN],CLXType.INT,   True),
    'para_float':    FuncSig('para_float',    [CLXType.UNKNOWN],CLXType.FLOAT, True),
    'para_texto':    FuncSig('para_texto',    [CLXType.UNKNOWN],CLXType.TEXTO, True),
    'sair':          FuncSig('sair',          [CLXType.INT],    CLXType.VOID,  True),
    'aleatorio':     FuncSig('aleatorio',     [CLXType.INT,CLXType.INT], CLXType.INT, True),
    'raiz':          FuncSig('raiz',          [CLXType.FLOAT],  CLXType.FLOAT, True),
    'potencia':      FuncSig('potencia',      [CLXType.FLOAT,CLXType.FLOAT], CLXType.FLOAT, True),
    'abs_val':       FuncSig('abs_val',       [CLXType.INT],    CLXType.INT,   True),
}


class Scope:
    def __init__(self, parent: Optional['Scope'] = None, name: str = "global"):
        self.parent    = parent
        self.name      = name
        self.symbols:  Dict[str, Symbol]  = {}
        self.functions: Dict[str, FuncSig] = dict(_BUILTINS) if parent is None else {}

    def declare_var(self, sym: Symbol, diag: Diagnostics):
        if sym.name in self.symbols:
            diag.error(
                f"Variável '{sym.name}' já declarada neste escopo",
                sym.line,
                hint=f"Use um nome diferente ou atribua com '{sym.name} = valor'"
            )
            return
        self.symbols[sym.name] = sym

    def assign_var(self, name: str, new_type: CLXType, diag: Diagnostics, line=0) -> bool:
        """Atualiza tipo de variável existente. Retorna True se encontrou."""
        if name in self.symbols:
            sym = self.symbols[name]
            if sym.is_const:
                diag.error(f"Não é possível reatribuir constante '{name}'", line,
                           hint="Declare sem 'const' se precisar modificar")
                return True
            if not coercible(new_type, sym.type):
                diag.error(
                    f"Tipo incompatível: '{name}' é {sym.type.value}, "
                    f"mas recebeu {new_type.value}",
                    line,
                    hint="Use para_int(), para_float() ou para_texto() para converter"
                )
            return True
        if self.parent:
            return self.parent.assign_var(name, new_type, diag, line)
        return False

    def lookup(self, name: str) -> Optional[Symbol]:
        if name in self.symbols: return self.symbols[name]
        if self.parent:          return self.parent.lookup(name)
        return None

    def declare_func(self, sig: FuncSig):
        root = self
        while root.parent: root = root.parent
        root.functions[sig.name] = sig

    def lookup_func(self, name: str) -> Optional[FuncSig]:
        root = self
        while root.parent: root = root.parent
        return root.functions.get(name)

    def child(self, name: str = "") -> 'Scope':
        return Scope(parent=self, name=name)


# ═══════════════════════════════════════════════════════════
# TYPE CHECKER
# ═══════════════════════════════════════════════════════════

class TypeChecker:
    def __init__(self, diag: Diagnostics):
        self.diag         = diag
        self.global_scope = Scope(name="global")
        self.cur_scope    = self.global_scope
        self.node_types:  Dict[int, CLXType] = {}
        self.node_scopes: Dict[int, Scope]   = {}   # escopo de FunctionDecl
        self.fn_return:   CLXType            = CLXType.VOID
        self.in_loop:     int                = 0    # contador de loops aninhados

    def annotate(self, node: ASTNode, t: CLXType):
        self.node_types[id(node)] = t

    def typeof(self, node: ASTNode) -> CLXType:
        return self.node_types.get(id(node), CLXType.UNKNOWN)

    def check(self, node: ASTNode) -> CLXType:
        m = f"check_{type(node).__name__}"
        return getattr(self, m, lambda n: CLXType.UNKNOWN)(node)

    # ── literals ──────────────────────────────────────────

    def check_Program(self, n: Program):
        for s in n.statements: self.check(s)
        return CLXType.VOID

    def check_IntegerLiteral (self, n): self.annotate(n, CLXType.INT);   return CLXType.INT
    def check_FloatLiteral   (self, n): self.annotate(n, CLXType.FLOAT); return CLXType.FLOAT
    def check_StringLiteral  (self, n): self.annotate(n, CLXType.TEXTO); return CLXType.TEXTO
    def check_BooleanLiteral (self, n): self.annotate(n, CLXType.BOOL);  return CLXType.BOOL
    def check_NullLiteral    (self, n): self.annotate(n, CLXType.UNKNOWN); return CLXType.UNKNOWN

    def check_Identifier(self, n: Identifier) -> CLXType:
        sym = self.cur_scope.lookup(n.name)
        if sym is None:
            self.diag.error(f"Variável '{n.name}' não declarada", n.line, n.column,
                            hint="Declare com 'var nome = valor' antes de usar")
            self.annotate(n, CLXType.UNKNOWN)
            return CLXType.UNKNOWN
        self.annotate(n, sym.type)
        return sym.type

    def check_VarDecl(self, n: VarDecl) -> CLXType:
        val_type = self.check(n.value) if n.value else CLXType.UNKNOWN
        explicit = hint_to_type(n.type_hint)
        final    = explicit if explicit != CLXType.UNKNOWN else val_type
        if final == CLXType.UNKNOWN:
            self.diag.warning(
                f"Tipo de '{n.name}' não pode ser inferido — assumindo int",
                n.line, n.column
            )
            final = CLXType.INT
        if explicit != CLXType.UNKNOWN and val_type != CLXType.UNKNOWN:
            if not coercible(val_type, explicit):
                self.diag.error(
                    f"'{n.name}': tipo declarado '{explicit.value}' "
                    f"incompatível com valor '{val_type.value}'",
                    n.line, n.column
                )
        sym = Symbol(name=n.name, type=final, is_const=n.is_const, line=n.line)
        self.cur_scope.declare_var(sym, self.diag)
        self.annotate(n, final)
        return final

    def check_Assignment(self, n: Assignment) -> CLXType:
        val_type = self.check(n.value)
        existing = self.cur_scope.lookup(n.target)
        if existing is None:
            # declaração implícita — permitida fora de funções
            sym = Symbol(name=n.target, type=val_type if val_type != CLXType.UNKNOWN else CLXType.INT,
                         line=n.line)
            self.cur_scope.symbols[n.target] = sym
        else:
            self.cur_scope.assign_var(n.target, val_type, self.diag, n.line)
        self.annotate(n, val_type)
        return val_type

    def check_BinaryOp(self, n: BinaryOp) -> CLXType:
        lt = self.check(n.left)
        rt = self.check(n.right)
        cmp_ops = {'==','!=','>','<','>=','<=','&&','||'}
        if n.operator in cmp_ops:
            t = CLXType.BOOL
        elif n.operator in {'+','-','*','/','%'}:
            t = promote(lt, rt)
        else:
            t = CLXType.INT
        self.annotate(n, t); return t

    def check_UnaryOp(self, n: UnaryOp) -> CLXType:
        t = self.check(n.operand)
        if n.operator == '!': t = CLXType.BOOL
        self.annotate(n, t); return t

    def check_FunctionCall(self, n: FunctionCall) -> CLXType:
        for a in n.arguments: self.check(a)
        sig = self.cur_scope.lookup_func(n.name)
        if sig is None:
            self.diag.error(
                f"Função '{n.name}' não declarada",
                n.line, n.column,
                hint="Declare com 'funcao nome(params) { ... }' antes de chamar"
            )
            self.annotate(n, CLXType.UNKNOWN)
            return CLXType.UNKNOWN
        self.annotate(n, sig.return_type)
        return sig.return_type

    def check_IfStatement(self, n: IfStatement):
        self.check(n.condition)
        old = self.cur_scope
        self.cur_scope = old.child("if-then")
        for s in n.then_block: self.check(s)
        self.cur_scope = old
        if n.else_block:
            self.cur_scope = old.child("if-else")
            for s in n.else_block: self.check(s)
            self.cur_scope = old
        return CLXType.VOID

    def check_WhileLoop(self, n: WhileLoop):
        self.check(n.condition)
        self.in_loop += 1
        old = self.cur_scope
        self.cur_scope = old.child("while")
        for s in n.body: self.check(s)
        self.cur_scope = old
        self.in_loop -= 1
        return CLXType.VOID

    def check_ForLoop(self, n: ForLoop):
        old = self.cur_scope
        self.cur_scope = old.child("for")
        self.in_loop += 1
        self.check(n.init)
        self.check(n.condition)
        self.check(n.increment)
        for s in n.body: self.check(s)
        self.in_loop -= 1
        self.cur_scope = old
        return CLXType.VOID

    def check_FunctionDecl(self, n: FunctionDecl):
        ret = hint_to_type(n.return_hint) if n.return_hint else CLXType.VOID
        param_types = [hint_to_type(h) for _, h in n.params]
        sig = FuncSig(name=n.name, param_types=param_types, return_type=ret)
        self.global_scope.declare_func(sig)

        fn_scope = self.global_scope.child(f"fn:{n.name}")
        for (pname, phint), ptype in zip(n.params, param_types):
            actual = ptype if ptype != CLXType.UNKNOWN else CLXType.INT
            fn_scope.symbols[pname] = Symbol(pname, actual, is_param=True, line=n.line)
        self.node_scopes[id(n)] = fn_scope

        old           = self.cur_scope
        self.cur_scope = fn_scope
        prev_ret      = self.fn_return
        self.fn_return = ret

        for s in n.body: self.check(s)

        self.fn_return = prev_ret
        self.cur_scope = old
        self.annotate(n, ret)
        return ret

    def check_ReturnStatement(self, n: ReturnStatement):
        if n.value:
            t = self.check(n.value)
            if self.fn_return != CLXType.VOID and not coercible(t, self.fn_return):
                self.diag.error(
                    f"Retorno do tipo '{t.value}', "
                    f"mas função espera '{self.fn_return.value}'",
                    n.line, n.column
                )
            self.fn_return = t   # refina se ainda era UNKNOWN
            self.annotate(n, t)
            return t
        return CLXType.VOID

    def check_BreakStatement(self, n: BreakStatement):
        if self.in_loop == 0:
            self.diag.error("'pare' fora de um loop", n.line, n.column)
        return CLXType.VOID

    def check_ContinueStatement(self, n: ContinueStatement):
        if self.in_loop == 0:
            self.diag.error("'continua' fora de um loop", n.line, n.column)
        return CLXType.VOID


# ═══════════════════════════════════════════════════════════
# CODE GENERATOR
# ═══════════════════════════════════════════════════════════

class CCodeGenerator:
    def __init__(self, checker: TypeChecker):
        self.checker       = checker
        self.code          = []
        self.indent_level  = 0
        # rastreia variáveis declaradas em cada escopo em geração
        self._declared:    Dict[int, Set[str]] = {}
        self._scope_stack: List[Scope]         = [checker.global_scope]
        self._tmp_counter  = 0

    def _scope(self) -> Scope:
        return self._scope_stack[-1]

    def _push(self, s: Scope):
        self._scope_stack.append(s)

    def _pop(self):
        self._scope_stack.pop()

    def _sid(self) -> int:
        return id(self._scope())

    def _was_declared(self, name: str) -> bool:
        sid = self._sid()
        return name in self._declared.get(sid, set())

    def _mark(self, name: str):
        sid = self._sid()
        self._declared.setdefault(sid, set()).add(name)

    def _fresh_tmp(self) -> str:
        self._tmp_counter += 1
        return f"_clx_tmp{self._tmp_counter}"

    def ind(self) -> str:
        return '    ' * self.indent_level

    def emit(self, line: str):
        self.code.append(self.ind() + line)

    def blank(self):
        self.code.append('')

    # ── top-level ─────────────────────────────────────────

    def generate(self, ast: Program) -> str:
        self.emit('#include <stdio.h>')
        self.emit('#include <stdlib.h>')
        self.emit('#include <string.h>')
        self.emit('#include <stdbool.h>')
        self.emit('#include <math.h>')
        self.emit('#include <time.h>')
        self.blank()
        self.emit('#pragma GCC optimize("O3,Ofast")')
        self.blank()
        # helper: itoa simples para para_texto(int)
        self.emit('static char _clx_numbuf[64];')
        self.blank()

        funcs  = [s for s in ast.statements if isinstance(s, FunctionDecl)]
        others = [s for s in ast.statements if not isinstance(s, FunctionDecl)]

        # forward declarations
        for fd in funcs:
            self._emit_forward(fd)
        if funcs: self.blank()

        # function bodies
        for fd in funcs:
            self._emit_function(fd)
            self.blank()

        # main
        self.emit('int main(void) {')
        self.indent_level += 1
        self.emit('srand((unsigned)time(NULL));')
        for s in others:
            self._stmt(s)
        self.emit('return 0;')
        self.indent_level -= 1
        self.emit('}')
        return '\n'.join(self.code)

    # ── functions ─────────────────────────────────────────

    def _fn_sig_str(self, node: FunctionDecl) -> str:
        sig      = self.checker.global_scope.lookup_func(node.name)
        ret_type = sig.return_type if sig else CLXType.VOID
        ret_c    = c_type(ret_type) if ret_type != CLXType.UNKNOWN else "int"

        fn_scope  = self.checker.node_scopes.get(id(node))
        param_parts = []
        for (pname, _) in node.params:
            psym  = fn_scope.symbols.get(pname) if fn_scope else None
            ptype = psym.type if psym else CLXType.INT
            param_parts.append(f"{c_type(ptype)} {pname}")
        params_c = ', '.join(param_parts) if param_parts else 'void'
        return f'{ret_c} {node.name}({params_c})'

    def _emit_forward(self, node: FunctionDecl):
        self.emit(self._fn_sig_str(node) + ';')

    def _emit_function(self, node: FunctionDecl):
        self.emit(self._fn_sig_str(node) + ' {')
        self.indent_level += 1

        fn_scope = self.checker.node_scopes.get(id(node))
        child    = fn_scope if fn_scope else self._scope().child(f"fn:{node.name}")
        self._push(child)
        # marcar params como já declarados
        for pname, _ in node.params:
            self._mark(pname)

        for s in node.body:
            self._stmt(s)

        self._pop()
        self.indent_level -= 1
        self.emit('}')

    # ── statements ────────────────────────────────────────

    def _stmt(self, node: ASTNode):
        if isinstance(node, VarDecl):
            self._var_decl(node)
        elif isinstance(node, Assignment):
            self._assignment(node)
        elif isinstance(node, FunctionCall):
            self.emit(self._call(node) + ';')
        elif isinstance(node, IfStatement):
            self._if(node)
        elif isinstance(node, WhileLoop):
            self._while(node)
        elif isinstance(node, ForLoop):
            self._for(node)
        elif isinstance(node, ReturnStatement):
            if node.value:
                self.emit(f'return {self._expr(node.value)};')
            else:
                self.emit('return;')
        elif isinstance(node, BreakStatement):
            self.emit('break;')
        elif isinstance(node, ContinueStatement):
            self.emit('continue;')

    def _var_decl(self, node: VarDecl):
        val_type = self.checker.typeof(node)
        if val_type == CLXType.UNKNOWN: val_type = CLXType.INT
        ct = c_type(val_type)
        if node.value:
            val = self._expr(node.value)
        else:
            # default value por tipo
            defaults = {CLXType.INT:'0', CLXType.FLOAT:'0.0',
                        CLXType.BOOL:'false', CLXType.TEXTO:'""'}
            val = defaults.get(val_type, '0')
        qual = 'const ' if node.is_const else ''
        self.emit(f'{qual}{ct} {node.name} = {val};')
        self._mark(node.name)

    def _assignment(self, node: Assignment):
        val  = self._expr(node.value)
        typ  = self.checker.typeof(node.value)
        if typ == CLXType.UNKNOWN: typ = CLXType.INT

        # compound: x += e → x = x + e
        if node.compound:
            op = node.compound[:-1]  # "+= " → "+"
            if self._was_declared(node.target):
                self.emit(f'{node.target} {node.compound} {val};')
            else:
                self._mark(node.target)
                self.emit(f'{c_type(typ)} {node.target} = {val};')
            return

        if self._was_declared(node.target):
            self.emit(f'{node.target} = {val};')
        else:
            self._mark(node.target)
            # texto precisa de espaço maior; usamos char array ou ponteiro
            if typ == CLXType.TEXTO:
                self.emit(f'char* {node.target} = {val};')
            else:
                self.emit(f'{c_type(typ)} {node.target} = {val};')

    def _if(self, node: IfStatement):
        self.emit(f'if ({self._expr(node.condition)}) {{')
        self.indent_level += 1
        child = self._scope().child()
        self._push(child)
        for s in node.then_block: self._stmt(s)
        self._pop()
        self.indent_level -= 1
        if node.else_block is not None:
            self.emit('} else {')
            self.indent_level += 1
            child2 = self._scope().child()
            self._push(child2)
            for s in node.else_block: self._stmt(s)
            self._pop()
            self.indent_level -= 1
        self.emit('}')

    def _while(self, node: WhileLoop):
        self.emit(f'while ({self._expr(node.condition)}) {{')
        self.indent_level += 1
        child = self._scope().child()
        self._push(child)
        for s in node.body: self._stmt(s)
        self._pop()
        self.indent_level -= 1
        self.emit('}')

    def _for(self, node: ForLoop):
        child = self._scope().child()
        self._push(child)

        if isinstance(node.init, (VarDecl, Assignment)):
            if isinstance(node.init, VarDecl):
                vt   = self.checker.typeof(node.init)
                if vt == CLXType.UNKNOWN: vt = CLXType.INT
                val  = self._expr(node.init.value) if node.init.value else '0'
                init = f'{c_type(vt)} {node.init.name} = {val}'
                self._mark(node.init.name)
            else:
                typ  = self.checker.typeof(node.init.value)
                if typ in (CLXType.UNKNOWN, CLXType.TEXTO): typ = CLXType.INT
                val  = self._expr(node.init.value)
                if self._was_declared(node.init.target):
                    init = f'{node.init.target} = {val}'
                else:
                    init = f'{c_type(typ)} {node.init.target} = {val}'
                    self._mark(node.init.target)
        else:
            init = self._expr(node.init)

        cond = self._expr(node.condition)

        if isinstance(node.increment, Assignment):
            if node.increment.compound:
                inc = f'{node.increment.target} {node.increment.compound} {self._expr(node.increment.value)}'
            else:
                inc = f'{node.increment.target} = {self._expr(node.increment.value)}'
        else:
            inc = self._expr(node.increment)

        self.emit(f'for ({init}; {cond}; {inc}) {{')
        self.indent_level += 1
        for s in node.body: self._stmt(s)
        self.indent_level -= 1
        self.emit('}')
        self._pop()

    # ── expressions ───────────────────────────────────────

    def _expr(self, node: ASTNode) -> str:
        if isinstance(node, IntegerLiteral): return str(node.value)
        if isinstance(node, FloatLiteral):
            s = str(node.value)
            return s if '.' in s else s + '.0'
        if isinstance(node, StringLiteral):
            esc = (node.value
                   .replace('\\','\\\\').replace('"','\\"')
                   .replace('\n','\\n').replace('\t','\\t').replace('\r','\\r'))
            return f'"{esc}"'
        if isinstance(node, BooleanLiteral):
            return 'true' if node.value else 'false'
        if isinstance(node, NullLiteral):
            return 'NULL'
        if isinstance(node, Identifier):
            return node.name
        if isinstance(node, BinaryOp):
            l = self._expr(node.left)
            r = self._expr(node.right)
            return f'({l} {node.operator} {r})'
        if isinstance(node, UnaryOp):
            return f'({node.operator}{self._expr(node.operand)})'
        if isinstance(node, FunctionCall):
            return self._call(node)
        if isinstance(node, Assignment):
            return f'({node.target} = {self._expr(node.value)})'
        return '0'

    # ── built-in calls ────────────────────────────────────

    def _call(self, node: FunctionCall) -> str:
        n    = node.name
        args = node.arguments

        if n == 'escreva':
            parts = []
            for a in args:
                t   = self.checker.typeof(a)
                fmt = printf_fmt(t)
                parts.append(f'printf("{fmt}\\n", {self._expr(a)})')
            return '; '.join(parts) if parts else 'printf("\\n")'

        if n == 'escreva_fmt':
            # escreva_fmt("Olá %s, você tem %d anos", nome, idade)
            fmt_parts = [self._expr(a) for a in args]
            return f'printf({", ".join(fmt_parts)})'

        if n == 'leia':
            tmp = self._fresh_tmp()
            # emite declaração do buffer antes e retorna o ponteiro
            self.emit(f'char {tmp}[1024];')
            self.emit(f'fgets({tmp}, 1024, stdin);')
            # remove \n
            self.emit(f'{tmp}[strcspn({tmp}, "\\n")] = 0;')
            return tmp

        if n == 'leia_int':
            tmp = self._fresh_tmp()
            self.emit(f'int {tmp};')
            self.emit(f'scanf("%d", &{tmp});')
            return tmp

        if n == 'leia_float':
            tmp = self._fresh_tmp()
            self.emit(f'double {tmp};')
            self.emit(f'scanf("%lf", &{tmp});')
            return tmp

        if n == 'tamanho':
            return f'(int)strlen({self._expr(args[0])})'

        if n == 'tipo_de':
            t = self.checker.typeof(args[0]) if args else CLXType.UNKNOWN
            names = {CLXType.INT:"int", CLXType.FLOAT:"float",
                     CLXType.BOOL:"bool", CLXType.TEXTO:"texto",
                     CLXType.VOID:"void", CLXType.UNKNOWN:"?"}
            return f'"{names.get(t, "?")}"'

        if n == 'para_int':
            a = self._expr(args[0])
            t = self.checker.typeof(args[0]) if args else CLXType.UNKNOWN
            if t == CLXType.TEXTO:  return f'atoi({a})'
            if t == CLXType.FLOAT:  return f'(int)({a})'
            return a

        if n == 'para_float':
            a = self._expr(args[0])
            t = self.checker.typeof(args[0]) if args else CLXType.UNKNOWN
            if t == CLXType.TEXTO:  return f'atof({a})'
            if t == CLXType.INT:    return f'(double)({a})'
            return a

        if n == 'para_texto':
            a = self._expr(args[0])
            t = self.checker.typeof(args[0]) if args else CLXType.UNKNOWN
            if t == CLXType.INT:
                return f'(sprintf(_clx_numbuf, "%d", {a}), _clx_numbuf)'
            if t == CLXType.FLOAT:
                return f'(sprintf(_clx_numbuf, "%g", {a}), _clx_numbuf)'
            return a

        if n == 'sair':
            code = self._expr(args[0]) if args else '0'
            return f'exit({code})'

        if n == 'aleatorio':
            lo = self._expr(args[0]) if len(args) > 0 else '0'
            hi = self._expr(args[1]) if len(args) > 1 else '100'
            return f'({lo} + rand() % ({hi} - {lo} + 1))'

        if n == 'raiz':
            return f'sqrt({self._expr(args[0])})'

        if n == 'potencia':
            return f'pow({self._expr(args[0])}, {self._expr(args[1])})'

        if n == 'abs_val':
            return f'abs({self._expr(args[0])})'

        # user-defined
        parts = ', '.join(self._expr(a) for a in args)
        return f'{n}({parts})'


# ═══════════════════════════════════════════════════════════
# AST PRINTER  (--print-ast)
# ═══════════════════════════════════════════════════════════

def print_ast(node: ASTNode, indent: int = 0):
    prefix = "  " * indent
    name   = type(node).__name__
    if isinstance(node, IntegerLiteral):  print(f"{prefix}Int({node.value})")
    elif isinstance(node, FloatLiteral):  print(f"{prefix}Float({node.value})")
    elif isinstance(node, StringLiteral): print(f"{prefix}Str({repr(node.value)})")
    elif isinstance(node, BooleanLiteral):print(f"{prefix}Bool({node.value})")
    elif isinstance(node, Identifier):    print(f"{prefix}Id({node.name})")
    elif isinstance(node, BinaryOp):
        print(f"{prefix}BinOp[{node.operator}]")
        print_ast(node.left,  indent+1)
        print_ast(node.right, indent+1)
    elif isinstance(node, UnaryOp):
        print(f"{prefix}UnaryOp[{node.operator}]")
        print_ast(node.operand, indent+1)
    elif isinstance(node, Assignment):
        print(f"{prefix}Assign[{node.target}] {node.compound}")
        print_ast(node.value, indent+1)
    elif isinstance(node, VarDecl):
        q = "const " if node.is_const else ""
        print(f"{prefix}VarDecl[{q}{node.name}: {node.type_hint}]")
        if node.value: print_ast(node.value, indent+1)
    elif isinstance(node, FunctionCall):
        print(f"{prefix}Call[{node.name}]")
        for a in node.arguments: print_ast(a, indent+1)
    elif isinstance(node, FunctionDecl):
        params = ', '.join(f"{n}:{t}" for n,t in node.params)
        print(f"{prefix}FuncDecl[{node.name}({params}) → {node.return_hint}]")
        for s in node.body: print_ast(s, indent+1)
    elif isinstance(node, IfStatement):
        print(f"{prefix}If")
        print_ast(node.condition, indent+1)
        print(f"{prefix}  Then:")
        for s in node.then_block: print_ast(s, indent+2)
        if node.else_block:
            print(f"{prefix}  Else:")
            for s in node.else_block: print_ast(s, indent+2)
    elif isinstance(node, WhileLoop):
        print(f"{prefix}While")
        print_ast(node.condition, indent+1)
        for s in node.body: print_ast(s, indent+1)
    elif isinstance(node, ForLoop):
        print(f"{prefix}For")
        print_ast(node.init,      indent+1)
        print_ast(node.condition, indent+1)
        print_ast(node.increment, indent+1)
        for s in node.body: print_ast(s, indent+1)
    elif isinstance(node, ReturnStatement):
        print(f"{prefix}Return")
        if node.value: print_ast(node.value, indent+1)
    elif isinstance(node, BreakStatement):    print(f"{prefix}Break")
    elif isinstance(node, ContinueStatement): print(f"{prefix}Continue")
    elif isinstance(node, Program):
        print(f"{prefix}Program ({len(node.statements)} stmts)")
        for s in node.statements: print_ast(s, indent+1)
    else:
        print(f"{prefix}{name}")


# ═══════════════════════════════════════════════════════════
# COMPILER
# ═══════════════════════════════════════════════════════════

class CLXCompilerV4:
    def __init__(self, source_file: str, flags: Dict[str, bool]):
        self.source_file = source_file
        self.flags       = flags
        self.source:     Optional[str]     = None
        self.ast:        Optional[Program] = None
        self.diag        = Diagnostics(source_file)

    def read(self) -> bool:
        try:
            with open(self.source_file, 'r', encoding='utf-8') as f:
                self.source = f.read()
            return True
        except FileNotFoundError:
            self.diag.fatal(f"Arquivo '{self.source_file}' não encontrado")
            return False

    def run(self) -> bool:
        if not self.read():
            self.diag.report(); return False

        _banner("COMPILADOR CLX V4 — LINGUAGEM CONSOLIDADA")

        # ── 1. Léxico ──────────────────────────────────────
        _step("1", "Análise Léxica")
        try:
            lexer  = Lexer(self.source, self.diag)
            tokens = lexer.tokenize()
            _ok(f"{len(tokens)} tokens gerados")
        except Exception as e:
            self.diag.fatal(f"Lexer travou: {e}")
            self.diag.report(); return False

        # ── 2. Sintático ───────────────────────────────────
        _step("2", "Análise Sintática (AST)")
        try:
            parser   = Parser(tokens, self.diag)
            self.ast = parser.parse()
            _ok(f"AST: {len(self.ast.statements)} declarações no topo")
        except Exception as e:
            self.diag.fatal(f"Parser travou: {e}")
            self.diag.report(); return False

        if self.flags.get('print_ast'):
            print("\n──── AST ────")
            print_ast(self.ast)
            print("────────────\n")

        # ── 3. Tipos e Escopos ─────────────────────────────
        _step("3", "Tipos e Escopos")
        try:
            checker = TypeChecker(self.diag)
            checker.check(self.ast)
            if self.diag.has_errors():
                self.diag.report()
                _fail("Erros de semântica impedem a compilação")
                return False
            _ok("Tipos inferidos, escopos validados")
        except Exception as e:
            self.diag.fatal(f"TypeChecker travou: {e}")
            self.diag.report(); return False

        if self.flags.get('check_only'):
            _ok("--check-only: nenhum arquivo gerado")
            self.diag.report()
            return True

        # ── 4. Geração de C ────────────────────────────────
        _step("4", "Geração de Código C")
        c_file = self.source_file.replace('.ulx', '.c')
        try:
            codegen = CCodeGenerator(checker)
            c_code  = codegen.generate(self.ast)
            with open(c_file, 'w', encoding='utf-8') as f:
                f.write(c_code)
            _ok(f"C gerado: {c_file}")
            if self.flags.get('print_c'):
                print("\n──── C gerado ────")
                print(c_code)
                print("──────────────────\n")
        except Exception as e:
            self.diag.fatal(f"CodeGen travou: {e}")
            self.diag.report(); return False

        # ── 5. Compilação ──────────────────────────────────
        _step("5", "Compilação para binário nativo")
        binary = self.source_file.replace('.ulx', '')
        cmd    = ['gcc', '-O3', '-march=native', '-mtune=native',
                  '-flto', '-ffast-math', '-s',
                  c_file, '-o', binary, '-lm']
        try:
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0:
                size = os.path.getsize(binary)
                _ok(f"Binário: {binary}  ({size:,} bytes)")
                self.diag.report()
                _banner("COMPILAÇÃO BEM-SUCEDIDA")
                print(f"[CLX] Execute: ./{binary}\n")
                return True
            else:
                self.diag.fatal("gcc retornou erro:")
                print(res.stderr)
                self.diag.report(); return False
        except FileNotFoundError:
            self.diag.fatal("gcc não encontrado no PATH")
            self.diag.report(); return False


# ═══════════════════════════════════════════════════════════
# HELPERS DE OUTPUT
# ═══════════════════════════════════════════════════════════

def _banner(msg: str):
    w = 48
    print(f"\n[CLX] ╔{'═'*w}╗")
    print(f"[CLX] ║  {msg:<{w-2}}  ║")
    print(f"[CLX] ╚{'═'*w}╝\n")

def _step(n, msg): print(f"[CLX] Fase {n}: {msg}")
def _ok(msg):      print(f"[CLX]   ✓ {msg}")
def _fail(msg):    print(f"[CLX]   ✗ {msg}")


# ═══════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════

def usage():
    print("""
Uso: python3 clx_compiler_v4.py [opções] <arquivo.ulx>

Opções:
  --check-only    Valida sem compilar
  --print-ast     Imprime a AST em texto
  --print-c       Mostra o código C gerado
  --help          Esta mensagem
""")

def main():
    args  = sys.argv[1:]
    flags = {}
    files = []

    for a in args:
        if a == '--check-only': flags['check_only'] = True
        elif a == '--print-ast': flags['print_ast'] = True
        elif a == '--print-c':  flags['print_c']  = True
        elif a in ('--help', '-h'): usage(); sys.exit(0)
        elif a.startswith('--'):
            print(f"[CLX] Opção desconhecida: {a}"); usage(); sys.exit(1)
        else:
            files.append(a)

    if not files:
        usage(); sys.exit(1)

    compiler = CLXCompilerV4(files[0], flags)
    sys.exit(0 if compiler.run() else 1)


if __name__ == '__main__':
    main()
