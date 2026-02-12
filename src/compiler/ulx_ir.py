#!/usr/bin/env python3
"""
ULX-IR - Representação Intermediária da linguagem ULX
Baseado em LLVM IR mas simplificado para o ecossistema ULX
"""

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union, Any
from abc import ABC, abstractmethod


class TypeKind(Enum):
    """Tipos primitivos suportados"""
    VOID = auto()
    I8 = auto()
    I16 = auto()
    I32 = auto()
    I64 = auto()
    F32 = auto()
    F64 = auto()
    PTR = auto()
    ARRAY = auto()
    FUNCTION = auto()
    STRUCT = auto()


@dataclass
class Type:
    """Representa um tipo na ULX-IR"""
    kind: TypeKind
    element_type: Optional['Type'] = None  # Para arrays e pointers
    size: int = 0  # Para arrays
    params: List['Type'] = field(default_factory=list)  # Para funções
    ret_type: Optional['Type'] = None  # Para funções
    
    def __str__(self):
        if self.kind == TypeKind.PTR:
            return f"ptr"
        elif self.kind == TypeKind.ARRAY:
            return f"[{self.size} x {self.element_type}]"
        elif self.kind == TypeKind.FUNCTION:
            params = ", ".join(str(p) for p in self.params)
            return f"{self.ret_type} ({params})"
        return self.kind.name.lower()
    
    def __eq__(self, other):
        if not isinstance(other, Type):
            return False
        return (self.kind == other.kind and 
                self.element_type == other.element_type and
                self.size == other.size)


# Tipos pré-definidos
TypeVoid = Type(TypeKind.VOID)
TypeI8 = Type(TypeKind.I8)
TypeI16 = Type(TypeKind.I16)
TypeI32 = Type(TypeKind.I32)
TypeI64 = Type(TypeKind.I64)
TypeF32 = Type(TypeKind.F32)
TypeF64 = Type(TypeKind.F64)
TypePtr = Type(TypeKind.PTR)


def ArrayType(element_type: Type, size: int) -> Type:
    """Cria um tipo array"""
    return Type(TypeKind.ARRAY, element_type=element_type, size=size)


def FunctionType(ret_type: Type, params: List[Type]) -> Type:
    """Cria um tipo função"""
    return Type(TypeKind.FUNCTION, ret_type=ret_type, params=params)


class Opcode(Enum):
    """Operações da ULX-IR"""
    # Memory
    ALLOCA = "alloca"
    LOAD = "load"
    STORE = "store"
    GEP = "getelementptr"  # Get element pointer
    
    # Arithmetic
    ADD = "add"
    SUB = "sub"
    MUL = "mul"
    SDIV = "sdiv"  # Signed division
    UDIV = "udiv"  # Unsigned division
    SREM = "srem"  # Signed remainder
    UREM = "urem"  # Unsigned remainder
    
    # Floating point
    FADD = "fadd"
    FSUB = "fsub"
    FMUL = "fmul"
    FDIV = "fdiv"
    FREM = "frem"
    
    # Bitwise
    AND = "and"
    OR = "or"
    XOR = "xor"
    SHL = "shl"
    LSHR = "lshr"  # Logical shift right
    ASHR = "ashr"  # Arithmetic shift right
    
    # Comparison
    ICMP = "icmp"  # Integer compare
    FCMP = "fcmp"  # Float compare
    
    # Control flow
    BR = "br"      # Branch
    COND_BR = "cond_br"  # Conditional branch
    RET = "ret"
    CALL = "call"
    PHI = "phi"    # SSA phi node
    
    # Conversions
    TRUNC = "trunc"
    ZEXT = "zext"  # Zero extend
    SEXT = "sext"  # Sign extend
    FPTRUNC = "fptrunc"
    FPEXT = "fpext"
    FPTOUI = "fptoui"
    FPTOSI = "fptosi"
    UITOFP = "uitofp"
    SITOFP = "sitofp"
    PTRTOINT = "ptrtoint"
    INTTOPTR = "inttoptr"
    BITCAST = "bitcast"


class ICmpPredicate(Enum):
    """Predicados de comparação inteira"""
    EQ = "eq"
    NE = "ne"
    UGT = "ugt"
    UGE = "uge"
    ULT = "ult"
    ULE = "ule"
    SGT = "sgt"
    SGE = "sge"
    SLT = "slt"
    SLE = "sle"


class FCmpPredicate(Enum):
    """Predicados de comparação de ponto flutuante"""
    FALSE = "false"
    OEQ = "oeq"
    OGT = "ogt"
    OGE = "oge"
    OLT = "olt"
    OLE = "ole"
    ONE = "one"
    ORD = "ord"
    UEQ = "ueq"
    UGT = "ugt"
    UGE = "uge"
    ULT = "ult"
    ULE = "ule"
    UNE = "une"
    UNO = "uno"
    TRUE = "true"


@dataclass
class Value:
    """Valor em SSA form"""
    name: str
    type: Type
    
    def __str__(self):
        return f"{self.type} {self.name}"


@dataclass
class Constant(Value):
    """Constante"""
    value: Union[int, float, str, None]
    
    def __init__(self, type: Type, value: Union[int, float, str, None]):
        super().__init__("", type)
        self.value = value
    
    def __str__(self):
        if self.value is None:
            return "null"
        if isinstance(self.value, str):
            return f'c"{self.value}"'
        return str(self.value)


@dataclass
class Instruction:
    """Instrução ULX-IR"""
    opcode: Opcode
    result: Optional[Value] = None
    operands: List[Value] = field(default_factory=list)
    predicate: Optional[Union[ICmpPredicate, FCmpPredicate]] = None
    
    def __str__(self):
        if self.result:
            result_str = f"{self.result.name} = "
        else:
            result_str = ""
        
        ops = ", ".join(str(op) for op in self.operands)
        
        if self.predicate:
            return f"  {result_str}{self.opcode.value} {self.predicate.value} {ops}"
        return f"  {result_str}{self.opcode.value} {ops}"


@dataclass
class BasicBlock:
    """Bloco básico - sequência de instruções"""
    name: str
    instructions: List[Instruction] = field(default_factory=list)
    predecessors: List['BasicBlock'] = field(default_factory=list)
    successors: List['BasicBlock'] = field(default_factory=list)
    
    def add_instruction(self, inst: Instruction):
        self.instructions.append(inst)
    
    def __str__(self):
        lines = [f"{self.name}:"]
        for inst in self.instructions:
            lines.append(str(inst))
        return "\n".join(lines)


@dataclass
class Function:
    """Função ULX-IR"""
    name: str
    return_type: Type
    params: List[Value]
    blocks: List[BasicBlock] = field(default_factory=list)
    is_external: bool = False
    
    def __post_init__(self):
        if not self.blocks and not self.is_external:
            entry = BasicBlock("entry")
            self.blocks.append(entry)
    
    def add_block(self, name: str) -> BasicBlock:
        block = BasicBlock(name)
        self.blocks.append(block)
        return block
    
    def entry_block(self) -> BasicBlock:
        return self.blocks[0] if self.blocks else None
    
    def __str__(self):
        if self.is_external:
            params = ", ".join(f"{p.type} {p.name}" for p in self.params)
            return f"declare {self.return_type} @{self.name}({params})"
        
        params = ", ".join(f"{p.type} {p.name}" for p in self.params)
        lines = [f"define {self.return_type} @{self.name}({params}) {{"]
        for block in self.blocks:
            lines.append(str(block))
        lines.append("}")
        return "\n".join(lines)


@dataclass
class GlobalVariable:
    """Variável global"""
    name: str
    type: Type
    initializer: Optional[Constant] = None
    is_constant: bool = False
    
    def __str__(self):
        const_str = "constant" if self.is_constant else "global"
        if self.initializer:
            return f"@{self.name} = {const_str} {self.type} {self.initializer}"
        return f"@{self.name} = {const_str} {self.type} zeroinitializer"


@dataclass
class Module:
    """Módulo ULX-IR - contém funções e variáveis globais"""
    name: str
    functions: List[Function] = field(default_factory=list)
    globals: List[GlobalVariable] = field(default_factory=list)
    
    def add_function(self, func: Function):
        self.functions.append(func)
    
    def add_global(self, global_var: GlobalVariable):
        self.globals.append(global_var)
    
    def get_function(self, name: str) -> Optional[Function]:
        for f in self.functions:
            if f.name == name:
                return f
        return None
    
    def __str__(self):
        lines = [f"; Module: {self.name}", ""]
        
        # Globals
        for g in self.globals:
            lines.append(str(g))
        if self.globals:
            lines.append("")
        
        # Functions
        for f in self.functions:
            lines.append(str(f))
            lines.append("")
        
        return "\n".join(lines)


class IRBuilder:
    """Builder para criar IR de forma conveniente"""
    
    def __init__(self, module: Module):
        self.module = module
        self.current_function: Optional[Function] = None
        self.current_block: Optional[BasicBlock] = None
        self.temp_counter = 0
        self.block_counter = 0
    
    def set_function(self, func: Function):
        self.current_function = func
        self.current_block = func.entry_block()
    
    def create_block(self, name: str = None) -> BasicBlock:
        if name is None:
            name = f"bb{self.block_counter}"
            self.block_counter += 1
        return self.current_function.add_block(name)
    
    def set_block(self, block: BasicBlock):
        self.current_block = block
    
    def _new_temp(self, type: Type) -> Value:
        name = f"%{self.temp_counter}"
        self.temp_counter += 1
        return Value(name, type)
    
    def alloca(self, type: Type, name: str = None) -> Value:
        """Cria uma alocação na stack"""
        result = Value(name or self._new_temp(TypePtr).name, TypePtr)
        inst = Instruction(Opcode.ALLOCA, result, [type])
        self.current_block.add_instruction(inst)
        return result
    
    def load(self, ptr: Value, name: str = None) -> Value:
        """Carrega valor de um ponteiro"""
        result = Value(name or self._new_temp(ptr.type).name, ptr.type)
        inst = Instruction(Opcode.LOAD, result, [ptr])
        self.current_block.add_instruction(inst)
        return result
    
    def store(self, value: Value, ptr: Value) -> None:
        """Armazena valor em um ponteiro"""
        inst = Instruction(Opcode.STORE, None, [value, ptr])
        self.current_block.add_instruction(inst)
    
    def add(self, lhs: Value, rhs: Value, name: str = None) -> Value:
        """Adição inteira"""
        result = Value(name or self._new_temp(lhs.type).name, lhs.type)
        inst = Instruction(Opcode.ADD, result, [lhs, rhs])
        self.current_block.add_instruction(inst)
        return result
    
    def sub(self, lhs: Value, rhs: Value, name: str = None) -> Value:
        """Subtração inteira"""
        result = Value(name or self._new_temp(lhs.type).name, lhs.type)
        inst = Instruction(Opcode.SUB, result, [lhs, rhs])
        self.current_block.add_instruction(inst)
        return result
    
    def mul(self, lhs: Value, rhs: Value, name: str = None) -> Value:
        """Multiplicação inteira"""
        result = Value(name or self._new_temp(lhs.type).name, lhs.type)
        inst = Instruction(Opcode.MUL, result, [lhs, rhs])
        self.current_block.add_instruction(inst)
        return result
    
    def sdiv(self, lhs: Value, rhs: Value, name: str = None) -> Value:
        """Divisão inteira com sinal"""
        result = Value(name or self._new_temp(lhs.type).name, lhs.type)
        inst = Instruction(Opcode.SDIV, result, [lhs, rhs])
        self.current_block.add_instruction(inst)
        return result
    
    def icmp(self, pred: ICmpPredicate, lhs: Value, rhs: Value, name: str = None) -> Value:
        """Comparação inteira"""
        result = Value(name or self._new_temp(TypeI1).name, TypeI1)
        inst = Instruction(Opcode.ICMP, result, [lhs, rhs], predicate=pred)
        self.current_block.add_instruction(inst)
        return result
    
    def br(self, target: BasicBlock) -> None:
        """Branch incondicional"""
        inst = Instruction(Opcode.BR, None, [target])
        self.current_block.add_instruction(inst)
        self.current_block.successors.append(target)
        target.predecessors.append(self.current_block)
    
    def cond_br(self, cond: Value, true_block: BasicBlock, false_block: BasicBlock) -> None:
        """Branch condicional"""
        inst = Instruction(Opcode.COND_BR, None, [cond, true_block, false_block])
        self.current_block.add_instruction(inst)
        self.current_block.successors.extend([true_block, false_block])
        true_block.predecessors.append(self.current_block)
        false_block.predecessors.append(self.current_block)
    
    def call(self, func: Function, args: List[Value], name: str = None) -> Optional[Value]:
        """Chamada de função"""
        result = None
        if func.return_type != TypeVoid:
            result = Value(name or self._new_temp(func.return_type).name, func.return_type)
        inst = Instruction(Opcode.CALL, result, [func] + args)
        self.current_block.add_instruction(inst)
        return result
    
    def ret(self, value: Optional[Value] = None) -> None:
        """Retorno de função"""
        if value:
            inst = Instruction(Opcode.RET, None, [value])
        else:
            inst = Instruction(Opcode.RET, None, [])
        self.current_block.add_instruction(inst)
    
    def phi(self, type: Type, incoming: List[tuple], name: str = None) -> Value:
        """Nó phi para SSA"""
        result = Value(name or self._new_temp(type).name, type)
        operands = []
        for val, block in incoming:
            operands.extend([val, block])
        inst = Instruction(Opcode.PHI, result, operands)
        self.current_block.add_instruction(inst)
        return result


# Tipo i1 para comparações
TypeI1 = Type(TypeKind.I8)  # Usamos i8 para booleanos


if __name__ == "__main__":
    # Exemplo de uso
    module = Module("test")
    
    # Criar função main
    main_func = Function("main", TypeI32, [])
    module.add_function(main_func)
    
    # Builder
    builder = IRBuilder(module)
    builder.set_function(main_func)
    
    # Criar variável local
    x = builder.alloca(TypeI32, "%x")
    
    # Armazenar valor
    builder.store(Constant(TypeI32, 42), x)
    
    # Carregar e adicionar
    val = builder.load(x)
    ten = Constant(TypeI32, 10)
    result = builder.add(val, ten)
    
    # Retornar
    builder.ret(result)
    
    print(module)
