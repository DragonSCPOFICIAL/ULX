#!/usr/bin/env python3
"""
ULXC - Compilador ULX Completo
Integra lexer, parser, IR, codegen e ELF generation
"""

import sys
import os
import subprocess
import tempfile
import argparse
from pathlib import Path

# Importar módulos do compilador
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from ulx_parser import parse_source, TokenType
    from ulx_ir import (
        Module, Function, BasicBlock, Instruction, Value, Constant,
        Type, TypeKind, TypeI8, TypeI16, TypeI32, TypeI64, TypeF32, 
        TypeF64, TypePtr, TypeVoid, Opcode, ICmpPredicate, IRBuilder,
        ArrayType, FunctionType
    )
except ImportError as e:
    print(f"Error importing compiler modules: {e}")
    sys.exit(1)


class TypeChecker:
    """Verificador de tipos"""
    
    def __init__(self):
        self.symbol_table = {}
        self.function_table = {}
    
    def check_program(self, ast):
        """Verifica tipos do programa completo"""
        for decl in ast.declarations:
            self.check_declaration(decl)
    
    def check_declaration(self, decl):
        """Verifica declaração"""
        from ulx_parser import FunctionDecl, VarDecl
        
        if isinstance(decl, FunctionDecl):
            self.check_function(decl)
        elif isinstance(decl, VarDecl):
            self.check_var_decl(decl)
    
    def check_function(self, func):
        """Verifica função"""
        # Registrar função
        param_types = [self.string_to_type(p[1]) for p in func.params]
        ret_type = self.string_to_type(func.return_type)
        self.function_table[func.name] = FunctionType(ret_type, param_types)
        
        # Verificar corpo
        for stmt in func.body:
            self.check_statement(stmt)
    
    def check_var_decl(self, var):
        """Verifica declaração de variável"""
        var_type = self.string_to_type(var.var_type) if var.var_type else None
        
        if var.initializer:
            init_type = self.check_expression(var.initializer)
            if var_type is None:
                var_type = init_type
            elif var_type != init_type:
                raise TypeError(f"Type mismatch in variable declaration: {var.name}")
        
        self.symbol_table[var.name] = var_type
    
    def check_statement(self, stmt):
        """Verifica statement"""
        from ulx_parser import (
            IfStmt, WhileStmt, ForStmt, ReturnStmt, WriteStmt,
            ReadStmt, ExprStmt, AssignmentExpr
        )
        
        if isinstance(stmt, IfStmt):
            cond_type = self.check_expression(stmt.condition)
            for s in stmt.then_branch:
                self.check_statement(s)
            for s in stmt.else_branch:
                self.check_statement(s)
        
        elif isinstance(stmt, WhileStmt):
            cond_type = self.check_expression(stmt.condition)
            for s in stmt.body:
                self.check_statement(s)
        
        elif isinstance(stmt, ForStmt):
            if stmt.init:
                self.check_statement(stmt.init)
            if stmt.condition:
                self.check_expression(stmt.condition)
            if stmt.increment:
                self.check_expression(stmt.increment)
            for s in stmt.body:
                self.check_statement(s)
        
        elif isinstance(stmt, ReturnStmt):
            if stmt.value:
                self.check_expression(stmt.value)
        
        elif isinstance(stmt, WriteStmt):
            self.check_expression(stmt.expression)
        
        elif isinstance(stmt, ReadStmt):
            pass  # TODO
        
        elif isinstance(stmt, ExprStmt):
            self.check_expression(stmt.expression)
    
    def check_expression(self, expr):
        """Verifica expressão e retorna tipo"""
        from ulx_parser import (
            BinaryExpr, UnaryExpr, LiteralExpr, IdentifierExpr,
            CallExpr, AssignmentExpr
        )
        
        if isinstance(expr, LiteralExpr):
            return self.string_to_type(expr.literal_type)
        
        elif isinstance(expr, IdentifierExpr):
            if expr.name in self.symbol_table:
                return self.symbol_table[expr.name]
            raise NameError(f"Undefined variable: {expr.name}")
        
        elif isinstance(expr, BinaryExpr):
            left_type = self.check_expression(expr.left)
            right_type = self.check_expression(expr.right)
            
            if expr.operator in ['+', '-', '*', '/', '%']:
                if left_type != right_type:
                    raise TypeError(f"Type mismatch in binary operation")
                return left_type
            
            elif expr.operator in ['==', '!=', '<', '>', '<=', '>=']:
                return TypeI8  # Boolean
            
            elif expr.operator in ['&&', '||']:
                return TypeI8  # Boolean
        
        elif isinstance(expr, UnaryExpr):
            operand_type = self.check_expression(expr.operand)
            return operand_type
        
        elif isinstance(expr, CallExpr):
            if expr.callee in self.function_table:
                func_type = self.function_table[expr.callee]
                return func_type.ret_type
            raise NameError(f"Undefined function: {expr.callee}")
        
        elif isinstance(expr, AssignmentExpr):
            target_type = self.symbol_table.get(expr.target)
            value_type = self.check_expression(expr.value)
            if target_type != value_type:
                raise TypeError(f"Type mismatch in assignment")
            return target_type
        
        return TypeI32  # Default
    
    def string_to_type(self, type_str: str) -> Type:
        """Converte string de tipo para Type"""
        type_map = {
            'inteiro': TypeI32,
            'real': TypeF64,
            'texto': TypePtr,
            'booleano': TypeI8,
            'void': TypeVoid,
            'i8': TypeI8,
            'i16': TypeI16,
            'i32': TypeI32,
            'i64': TypeI64,
            'f32': TypeF32,
            'f64': TypeF64,
        }
        return type_map.get(type_str, TypeI32)


class ASTtoIR:
    """Converte AST para ULX-IR"""
    
    def __init__(self):
        self.module = None
        self.builder = None
        self.symbol_table = {}
        self.function_table = {}
        self.temp_counter = 0
    
    def convert(self, ast) -> Module:
        """Converte AST para módulo IR"""
        self.module = Module("main")
        
        # Primeira passa: registrar funções
        for decl in ast.declarations:
            if hasattr(decl, 'name'):
                self.register_function(decl)
        
        # Segunda passa: gerar código
        for decl in ast.declarations:
            self.convert_declaration(decl)
        
        return self.module
    
    def register_function(self, func):
        """Registra função na tabela"""
        from ulx_parser import FunctionDecl
        
        if isinstance(func, FunctionDecl):
            params = []
            for param_name, param_type in func.params:
                ptype = self.string_to_type(param_type)
                params.append(Value(f"%{param_name}", ptype))
            
            ret_type = self.string_to_type(func.return_type)
            
            ir_func = Function(func.name, ret_type, params)
            self.module.add_function(ir_func)
            self.function_table[func.name] = ir_func
    
    def convert_declaration(self, decl):
        """Converte declaração"""
        from ulx_parser import FunctionDecl, VarDecl
        
        if isinstance(decl, FunctionDecl):
            self.convert_function(decl)
        elif isinstance(decl, VarDecl):
            self.convert_var_decl(decl)
    
    def convert_function(self, func):
        """Converte função"""
        ir_func = self.function_table.get(func.name)
        if not ir_func:
            return
        
        self.builder = IRBuilder(self.module)
        self.builder.set_function(ir_func)
        
        # Registrar parâmetros
        for param in ir_func.params:
            self.symbol_table[param.name[1:]] = param
        
        # Converter corpo
        for stmt in func.body:
            self.convert_statement(stmt)
    
    def convert_var_decl(self, var):
        """Converte declaração de variável"""
        var_type = self.string_to_type(var.var_type) if var.var_type else TypeI32
        
        # Alocar espaço
        ptr = self.builder.alloca(var_type, f"%{var.name}")
        self.symbol_table[var.name] = ptr
        
        # Inicializar se houver valor
        if var.initializer:
            value = self.convert_expression(var.initializer)
            self.builder.store(value, ptr)
    
    def convert_statement(self, stmt):
        """Converte statement"""
        from ulx_parser import (
            IfStmt, WhileStmt, ForStmt, ReturnStmt, WriteStmt,
            ReadStmt, ExprStmt, VarDecl
        )
        
        if isinstance(stmt, IfStmt):
            self.convert_if(stmt)
        
        elif isinstance(stmt, WhileStmt):
            self.convert_while(stmt)
        
        elif isinstance(stmt, ForStmt):
            self.convert_for(stmt)
        
        elif isinstance(stmt, ReturnStmt):
            if stmt.value:
                value = self.convert_expression(stmt.value)
                self.builder.ret(value)
            else:
                self.builder.ret()
        
        elif isinstance(stmt, WriteStmt):
            value = self.convert_expression(stmt.expression)
            # Chamar função de escrita (simplificado)
            # Na prática, chamaria write syscall
        
        elif isinstance(stmt, ReadStmt):
            pass  # TODO
        
        elif isinstance(stmt, ExprStmt):
            self.convert_expression(stmt.expression)
        
        elif isinstance(stmt, VarDecl):
            self.convert_var_decl(stmt)
    
    def convert_if(self, stmt):
        """Converte if statement"""
        from ulx_parser import IfStmt
        
        # Criar blocos
        then_block = self.builder.create_block("if.then")
        else_block = self.builder.create_block("if.else")
        end_block = self.builder.create_block("if.end")
        
        # Converter condição
        cond = self.convert_expression(stmt.condition)
        
        # Branch condicional
        self.builder.cond_br(cond, then_block, else_block)
        
        # Bloco then
        self.builder.set_block(then_block)
        for s in stmt.then_branch:
            self.convert_statement(s)
        if not then_block.instructions or then_block.instructions[-1].opcode not in [Opcode.RET, Opcode.BR]:
            self.builder.br(end_block)
        
        # Bloco else
        self.builder.set_block(else_block)
        for s in stmt.else_branch:
            self.convert_statement(s)
        if not else_block.instructions or else_block.instructions[-1].opcode not in [Opcode.RET, Opcode.BR]:
            self.builder.br(end_block)
        
        # Bloco end
        self.builder.set_block(end_block)
    
    def convert_while(self, stmt):
        """Converte while statement"""
        # Criar blocos
        cond_block = self.builder.create_block("while.cond")
        body_block = self.builder.create_block("while.body")
        end_block = self.builder.create_block("while.end")
        
        # Jump para condição
        self.builder.br(cond_block)
        
        # Bloco de condição
        self.builder.set_block(cond_block)
        cond = self.convert_expression(stmt.condition)
        self.builder.cond_br(cond, body_block, end_block)
        
        # Bloco do corpo
        self.builder.set_block(body_block)
        for s in stmt.body:
            self.convert_statement(s)
        if not body_block.instructions or body_block.instructions[-1].opcode not in [Opcode.RET, Opcode.BR]:
            self.builder.br(cond_block)
        
        # Bloco end
        self.builder.set_block(end_block)
    
    def convert_for(self, stmt):
        """Converte for statement"""
        # Inicialização
        if stmt.init:
            self.convert_statement(stmt.init)
        
        # Criar blocos
        cond_block = self.builder.create_block("for.cond")
        body_block = self.builder.create_block("for.body")
        inc_block = self.builder.create_block("for.inc")
        end_block = self.builder.create_block("for.end")
        
        # Jump para condição
        self.builder.br(cond_block)
        
        # Bloco de condição
        self.builder.set_block(cond_block)
        if stmt.condition:
            cond = self.convert_expression(stmt.condition)
            self.builder.cond_br(cond, body_block, end_block)
        else:
            self.builder.br(body_block)
        
        # Bloco do corpo
        self.builder.set_block(body_block)
        for s in stmt.body:
            self.convert_statement(s)
        if not body_block.instructions or body_block.instructions[-1].opcode not in [Opcode.RET, Opcode.BR]:
            self.builder.br(inc_block)
        
        # Bloco de incremento
        self.builder.set_block(inc_block)
        if stmt.increment:
            self.convert_expression(stmt.increment)
        self.builder.br(cond_block)
        
        # Bloco end
        self.builder.set_block(end_block)
    
    def convert_expression(self, expr) -> Value:
        """Converte expressão para valor IR"""
        from ulx_parser import (
            BinaryExpr, UnaryExpr, LiteralExpr, IdentifierExpr,
            CallExpr, AssignmentExpr
        )
        
        if isinstance(expr, LiteralExpr):
            return self.convert_literal(expr)
        
        elif isinstance(expr, IdentifierExpr):
            ptr = self.symbol_table.get(expr.name)
            if ptr:
                return self.builder.load(ptr)
            raise NameError(f"Undefined variable: {expr.name}")
        
        elif isinstance(expr, BinaryExpr):
            return self.convert_binary(expr)
        
        elif isinstance(expr, UnaryExpr):
            operand = self.convert_expression(expr.operand)
            if expr.operator == '-':
                zero = Constant(operand.type, 0)
                return self.builder.sub(zero, operand)
            elif expr.operator == '!':
                zero = Constant(operand.type, 0)
                return self.builder.icmp(ICmpPredicate.EQ, operand, zero)
            return operand
        
        elif isinstance(expr, CallExpr):
            return self.convert_call(expr)
        
        elif isinstance(expr, AssignmentExpr):
            ptr = self.symbol_table.get(expr.target)
            if ptr:
                value = self.convert_expression(expr.value)
                self.builder.store(value, ptr)
                return value
            raise NameError(f"Undefined variable: {expr.target}")
        
        return Constant(TypeI32, 0)
    
    def convert_literal(self, expr) -> Constant:
        """Converte literal"""
        if expr.literal_type == 'inteiro':
            return Constant(TypeI32, int(expr.value))
        elif expr.literal_type == 'real':
            return Constant(TypeF64, float(expr.value))
        elif expr.literal_type == 'texto':
            # Strings são complexas - simplificado
            return Constant(TypePtr, 0)
        elif expr.literal_type == 'booleano':
            return Constant(TypeI8, 1 if expr.value else 0)
        return Constant(TypeI32, 0)
    
    def convert_binary(self, expr) -> Value:
        """Converte expressão binária"""
        left = self.convert_expression(expr.left)
        right = self.convert_expression(expr.right)
        
        if expr.operator == '+':
            return self.builder.add(left, right)
        elif expr.operator == '-':
            return self.builder.sub(left, right)
        elif expr.operator == '*':
            return self.builder.mul(left, right)
        elif expr.operator == '/':
            return self.builder.sdiv(left, right)
        elif expr.operator == '%':
            # Simplificado - não temos srem no IR básico
            return self.builder.sdiv(left, right)
        elif expr.operator == '==':
            return self.builder.icmp(ICmpPredicate.EQ, left, right)
        elif expr.operator == '!=':
            return self.builder.icmp(ICmpPredicate.NE, left, right)
        elif expr.operator == '<':
            return self.builder.icmp(ICmpPredicate.SLT, left, right)
        elif expr.operator == '>':
            return self.builder.icmp(ICmpPredicate.SGT, left, right)
        elif expr.operator == '<=':
            return self.builder.icmp(ICmpPredicate.SLE, left, right)
        elif expr.operator == '>=':
            return self.builder.icmp(ICmpPredicate.SGE, left, right)
        
        return left
    
    def convert_call(self, expr) -> Optional[Value]:
        """Converte chamada de função"""
        func = self.function_table.get(expr.callee)
        if not func:
            raise NameError(f"Undefined function: {expr.callee}")
        
        args = [self.convert_expression(arg) for arg in expr.arguments]
        return self.builder.call(func, args)
    
    def string_to_type(self, type_str: str) -> Type:
        """Converte string de tipo para Type"""
        type_map = {
            'inteiro': TypeI32,
            'real': TypeF64,
            'texto': TypePtr,
            'booleano': TypeI8,
            'void': TypeVoid,
            'i8': TypeI8,
            'i16': TypeI16,
            'i32': TypeI32,
            'i64': TypeI64,
            'f32': TypeF32,
            'f64': TypeF64,
        }
        return type_map.get(type_str, TypeI32)


class ULXCompiler:
    """Compilador ULX completo"""
    
    def __init__(self):
        self.type_checker = TypeChecker()
        self.ast_to_ir = ASTtoIR()
    
    def compile(self, source: str, output_file: str = None, emit_ir: bool = False) -> str:
        """
        Compila código fonte ULX
        
        Args:
            source: Código fonte ULX
            output_file: Arquivo de saída (opcional)
            emit_ir: Se True, retorna IR em vez de binário
        
        Returns:
            Caminho do arquivo gerado ou IR como string
        """
        # 1. Parsing
        print("[1/4] Parsing...")
        ast = parse_source(source)
        
        # 2. Type checking
        print("[2/4] Type checking...")
        self.type_checker.check_program(ast)
        
        # 3. IR generation
        print("[3/4] Generating IR...")
        ir_module = self.ast_to_ir.convert(ast)
        
        if emit_ir:
            return str(ir_module)
        
        # 4. Code generation (via GCC por enquanto)
        print("[4/4] Generating code...")
        return self.generate_code(ir_module, output_file)
    
    def generate_code(self, ir_module: Module, output_file: str = None) -> str:
        """Gera código usando GCC como backend temporário"""
        # Gerar C como intermediário
        c_code = self.ir_to_c(ir_module)
        
        # Escrever arquivo C temporário
        with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
            f.write(c_code)
            c_file = f.name
        
        # Compilar com GCC
        if output_file is None:
            output_file = 'a.out'
        
        try:
            result = subprocess.run(
                ['gcc', '-O2', '-o', output_file, c_file, '-static'],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(f"GCC error: {result.stderr}")
                return None
        finally:
            os.unlink(c_file)
        
        return output_file
    
    def ir_to_c(self, ir_module: Module) -> str:
        """Converte IR para C (backend temporário)"""
        lines = [
            '#include <stdio.h>',
            '#include <stdlib.h>',
            '#include <stdint.h>',
            '#include <string.h>',
            '',
        ]
        
        for func in ir_module.functions:
            lines.extend(self.function_to_c(func))
            lines.append('')
        
        return '\n'.join(lines)
    
    def function_to_c(self, func: Function) -> List[str]:
        """Converte função IR para C"""
        lines = []
        
        # Assinatura
        ret_type = self.type_to_c(func.return_type)
        params = ', '.join(f'{self.type_to_c(p.type)} {p.name[1:]}' for p in func.params)
        lines.append(f'{ret_type} {func.name}({params}) {{')
        
        # Corpo
        for block in func.blocks:
            if block.name != 'entry':
                lines.append(f'{block.name}:')
            for inst in block.instructions:
                line = self.instruction_to_c(inst)
                if line:
                    lines.append(f'    {line}')
        
        lines.append('}')
        return lines
    
    def instruction_to_c(self, inst: Instruction) -> str:
        """Converte instrução IR para C"""
        if inst.opcode == Opcode.ALLOCA:
            return None  # Alocação implícita em C
        
        elif inst.opcode == Opcode.LOAD:
            ptr = inst.operands[0]
            return f'{inst.result.type} {inst.result.name[1:]} = {ptr.name[1:]};'
        
        elif inst.opcode == Opcode.STORE:
            value = inst.operands[0]
            ptr = inst.operands[1]
            return f'{ptr.name[1:]} = {value.name};'
        
        elif inst.opcode == Opcode.ADD:
            lhs = inst.operands[0]
            rhs = inst.operands[1]
            return f'{inst.result.type} {inst.result.name[1:]} = {lhs.name} + {rhs.name};'
        
        elif inst.opcode == Opcode.SUB:
            lhs = inst.operands[0]
            rhs = inst.operands[1]
            return f'{inst.result.type} {inst.result.name[1:]} = {lhs.name} - {rhs.name};'
        
        elif inst.opcode == Opcode.MUL:
            lhs = inst.operands[0]
            rhs = inst.operands[1]
            return f'{inst.result.type} {inst.result.name[1:]} = {lhs.name} * {rhs.name};'
        
        elif inst.opcode == Opcode.SDIV:
            lhs = inst.operands[0]
            rhs = inst.operands[1]
            return f'{inst.result.type} {inst.result.name[1:]} = {lhs.name} / {rhs.name};'
        
        elif inst.opcode == Opcode.ICMP:
            lhs = inst.operands[0]
            rhs = inst.operands[1]
            pred = inst.predicate
            op_map = {
                ICmpPredicate.EQ: '==',
                ICmpPredicate.NE: '!=',
                ICmpPredicate.SLT: '<',
                ICmpPredicate.SGT: '>',
                ICmpPredicate.SLE: '<=',
                ICmpPredicate.SGE: '>=',
            }
            op = op_map.get(pred, '==')
            return f'int {inst.result.name[1:]} = {lhs.name} {op} {rhs.name};'
        
        elif inst.opcode == Opcode.BR:
            target = inst.operands[0]
            return f'goto {target.name};'
        
        elif inst.opcode == Opcode.COND_BR:
            cond = inst.operands[0]
            true_block = inst.operands[1]
            false_block = inst.operands[2]
            return f'if ({cond.name}) goto {true_block.name}; else goto {false_block.name};'
        
        elif inst.opcode == Opcode.RET:
            if inst.operands:
                return f'return {inst.operands[0].name};'
            return 'return;'
        
        elif inst.opcode == Opcode.CALL:
            func = inst.operands[0]
            args = ', '.join(op.name for op in inst.operands[1:])
            if inst.result:
                return f'{inst.result.type} {inst.result.name[1:]} = {func.name}({args});'
            return f'{func.name}({args});'
        
        return f'// TODO: {inst.opcode}'
    
    def type_to_c(self, type: Type) -> str:
        """Converte tipo IR para C"""
        type_map = {
            TypeKind.VOID: 'void',
            TypeKind.I8: 'int8_t',
            TypeKind.I16: 'int16_t',
            TypeKind.I32: 'int32_t',
            TypeKind.I64: 'int64_t',
            TypeKind.F32: 'float',
            TypeKind.F64: 'double',
            TypeKind.PTR: 'void*',
        }
        return type_map.get(type.kind, 'int32_t')


def main():
    parser = argparse.ArgumentParser(description='ULX Compiler')
    parser.add_argument('input', help='Input ULX file')
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('--emit-ir', action='store_true', help='Emit IR only')
    parser.add_argument('--run', action='store_true', help='Run after compile')
    
    args = parser.parse_args()
    
    # Ler arquivo de entrada
    with open(args.input, 'r') as f:
        source = f.read()
    
    # Compilar
    compiler = ULXCompiler()
    
    try:
        result = compiler.compile(source, args.output, args.emit_ir)
        
        if args.emit_ir:
            print(result)
        else:
            print(f"Compiled: {result}")
            
            if args.run and result:
                print("\n--- Running ---")
                subprocess.run([f'./{result}'])
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
