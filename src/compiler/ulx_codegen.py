#!/usr/bin/env python3
"""
ULX CodeGen - Geração de código x86-64 assembly
Gera código assembly diretamente a partir do ULX-IR
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, field
from .ulx_ir import *


class RegisterAllocator:
    """Alocador de registradores simples (linear scan)"""
    
    REGISTERS = ['rax', 'rbx', 'rcx', 'rdx', 'rsi', 'rdi', 
                 'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14', 'r15']
    CALLER_SAVED = ['rax', 'rcx', 'rdx', 'rsi', 'rdi', 'r8', 'r9', 'r10', 'r11']
    CALLEE_SAVED = ['rbx', 'r12', 'r13', 'r14', 'r15']
    ARG_REGISTERS = ['rdi', 'rsi', 'rdx', 'rcx', 'r8', 'r9']
    
    def __init__(self):
        self.used: Dict[str, bool] = {reg: False for reg in self.REGISTERS}
        self.allocations: Dict[str, str] = {}  # value_name -> register
        self.spill_slots: Dict[str, int] = {}  # value_name -> stack_offset
        self.stack_offset = 0
    
    def allocate(self, value_name: str) -> str:
        """Aloca um registrador para um valor"""
        if value_name in self.allocations:
            return self.allocations[value_name]
        
        # Procurar registrador livre
        for reg in self.REGISTERS:
            if not self.used[reg]:
                self.used[reg] = True
                self.allocations[value_name] = reg
                return reg
        
        # Spill - usar stack
        self.stack_offset += 8
        self.spill_slots[value_name] = self.stack_offset
        return None
    
    def free(self, value_name: str):
        """Libera um registrador"""
        if value_name in self.allocations:
            reg = self.allocations[value_name]
            self.used[reg] = False
            del self.allocations[value_name]
    
    def get_stack_size(self) -> int:
        """Retorna tamanho total da stack necessária"""
        return self.stack_offset


@dataclass
class AssemblyFunction:
    """Função em assembly"""
    name: str
    instructions: List[str] = field(default_factory=list)
    
    def emit(self, instr: str):
        self.instructions.append(instr)
    
    def __str__(self) -> str:
        lines = [f".globl {self.name}", f".type {self.name}, @function", f"{self.name}:"]
        lines.extend(f"  {instr}" for instr in self.instructions)
        return "\n".join(lines)


class X86_64CodeGen:
    """Gerador de código x86-64"""
    
    def __init__(self):
        self.functions: List[AssemblyFunction] = []
        self.data_section: List[str] = []
        self.current_function: Optional[AssemblyFunction] = None
        self.reg_alloc: Optional[RegisterAllocator] = None
        self.label_counter = 0
    
    def new_label(self, prefix: str = "L") -> str:
        """Gera um novo label único"""
        label = f".{prefix}{self.label_counter}"
        self.label_counter += 1
        return label
    
    def emit(self, instr: str):
        """Emite instrução na função atual"""
        if self.current_function:
            self.current_function.emit(instr)
    
    def generate(self, module: Module) -> str:
        """Gera código assembly completo"""
        output = []
        
        # Header
        output.append("# ULX Generated Assembly")
        output.append(".text")
        output.append("")
        
        # Gerar cada função
        for func in module.functions:
            self.generate_function(func)
        
        # Adicionar funções
        for func in self.functions:
            output.append(str(func))
            output.append("")
        
        # Data section
        if self.data_section:
            output.append(".data")
            for line in self.data_section:
                output.append(line)
        
        return "\n".join(output)
    
    def generate_function(self, func: Function):
        """Gera código para uma função"""
        self.current_function = AssemblyFunction(func.name)
        self.reg_alloc = RegisterAllocator()
        self.functions.append(self.current_function)
        
        # Prologue
        self.emit("pushq %rbp")
        self.emit("movq %rsp, %rbp")
        
        # Alocar espaço para variáveis locais
        locals_size = self.calculate_locals_size(func)
        if locals_size > 0:
            self.emit(f"subq ${locals_size}, %rsp")
        
        # Salvar registradores callee-saved
        for reg in RegisterAllocator.CALLEE_SAVED:
            self.emit(f"pushq %{reg}")
        
        # Mover argumentos dos registradores para stack/locais
        for i, param in enumerate(func.params):
            if i < 6:
                arg_reg = RegisterAllocator.ARG_REGISTERS[i]
                self.emit(f"movq %{arg_reg}, -{8*(i+1)}(%rbp)")
        
        # Gerar código para cada bloco
        for block in func.blocks:
            self.generate_block(block)
        
        # Epilogue (fallback)
        epilogue_label = self.new_label("epilogue")
        self.emit(f"{epilogue_label}:")
        
        # Restaurar registradores
        for reg in reversed(RegisterAllocator.CALLEE_SAVED):
            self.emit(f"popq %{reg}")
        
        self.emit("leave")
        self.emit("ret")
    
    def calculate_locals_size(self, func: Function) -> int:
        """Calcula espaço necessário para variáveis locais"""
        # Contar alocações no entry block
        count = len(func.params)
        for block in func.blocks:
            for inst in block.instructions:
                if inst.opcode == Opcode.ALLOCA:
                    count += 1
        return count * 8
    
    def generate_block(self, block: BasicBlock):
        """Gera código para um bloco básico"""
        if block.name != "entry":
            self.emit(f"{block.name}:")
        
        for inst in block.instructions:
            self.generate_instruction(inst)
    
    def generate_instruction(self, inst: Instruction):
        """Gera código para uma instrução"""
        opcode_handlers = {
            Opcode.ALLOCA: self.gen_alloca,
            Opcode.LOAD: self.gen_load,
            Opcode.STORE: self.gen_store,
            Opcode.ADD: self.gen_add,
            Opcode.SUB: self.gen_sub,
            Opcode.MUL: self.gen_mul,
            Opcode.SDIV: self.gen_sdiv,
            Opcode.ICMP: self.gen_icmp,
            Opcode.BR: self.gen_br,
            Opcode.COND_BR: self.gen_cond_br,
            Opcode.CALL: self.gen_call,
            Opcode.RET: self.gen_ret,
            Opcode.PHI: self.gen_phi,
        }
        
        handler = opcode_handlers.get(inst.opcode)
        if handler:
            handler(inst)
        else:
            self.emit(f"# TODO: {inst.opcode}")
    
    def gen_alloca(self, inst: Instruction):
        """Gera código para alloca"""
        # Alocação já feita no prologue
        pass
    
    def gen_load(self, inst: Instruction):
        """Gera código para load"""
        ptr = inst.operands[0]
        result = inst.result
        
        reg = self.reg_alloc.allocate(result.name)
        if reg:
            self.emit(f"movq {ptr.name}, %{reg}")
        else:
            # Spill
            offset = self.reg_alloc.spill_slots[result.name]
            self.emit(f"movq {ptr.name}, %rax")
            self.emit(f"movq %rax, -{offset}(%rbp)")
    
    def gen_store(self, inst: Instruction):
        """Gera código para store"""
        value = inst.operands[0]
        ptr = inst.operands[1]
        
        self.emit(f"movq {value.name}, %rax")
        self.emit(f"movq %rax, {ptr.name}")
    
    def gen_add(self, inst: Instruction):
        """Gera código para add"""
        lhs = inst.operands[0]
        rhs = inst.operands[1]
        result = inst.result
        
        self.emit(f"movq {lhs.name}, %rax")
        self.emit(f"addq {rhs.name}, %rax")
        
        reg = self.reg_alloc.allocate(result.name)
        if reg and reg != 'rax':
            self.emit(f"movq %rax, %{reg}")
    
    def gen_sub(self, inst: Instruction):
        """Gera código para sub"""
        lhs = inst.operands[0]
        rhs = inst.operands[1]
        result = inst.result
        
        self.emit(f"movq {lhs.name}, %rax")
        self.emit(f"subq {rhs.name}, %rax")
        
        reg = self.reg_alloc.allocate(result.name)
        if reg and reg != 'rax':
            self.emit(f"movq %rax, %{reg}")
    
    def gen_mul(self, inst: Instruction):
        """Gera código para mul"""
        lhs = inst.operands[0]
        rhs = inst.operands[1]
        result = inst.result
        
        self.emit(f"movq {lhs.name}, %rax")
        self.emit(f"imulq {rhs.name}, %rax")
        
        reg = self.reg_alloc.allocate(result.name)
        if reg and reg != 'rax':
            self.emit(f"movq %rax, %{reg}")
    
    def gen_sdiv(self, inst: Instruction):
        """Gera código para divisão com sinal"""
        lhs = inst.operands[0]
        rhs = inst.operands[1]
        result = inst.result
        
        self.emit(f"movq {lhs.name}, %rax")
        self.emit("cqto")  # Sign extend rax to rdx:rax
        self.emit(f"idivq {rhs.name}")
        
        reg = self.reg_alloc.allocate(result.name)
        if reg and reg != 'rax':
            self.emit(f"movq %rax, %{reg}")
    
    def gen_icmp(self, inst: Instruction):
        """Gera código para comparação inteira"""
        lhs = inst.operands[0]
        rhs = inst.operands[1]
        result = inst.result
        pred = inst.predicate
        
        self.emit(f"movq {lhs.name}, %rax")
        self.emit(f"cmpq {rhs.name}, %rax")
        
        # Set flag baseado no predicado
        setcc = {
            ICmpPredicate.EQ: "sete",
            ICmpPredicate.NE: "setne",
            ICmpPredicate.SGT: "setg",
            ICmpPredicate.SGE: "setge",
            ICmpPredicate.SLT: "setl",
            ICmpPredicate.SLE: "setle",
            ICmpPredicate.UGT: "seta",
            ICmpPredicate.UGE: "setae",
            ICmpPredicate.ULT: "setb",
            ICmpPredicate.ULE: "setbe",
        }
        
        instr = setcc.get(pred, "sete")
        self.emit(f"{instr} %al")
        self.emit("movzbq %al, %rax")  # Zero extend
        
        reg = self.reg_alloc.allocate(result.name)
        if reg and reg != 'rax':
            self.emit(f"movq %rax, %{reg}")
    
    def gen_br(self, inst: Instruction):
        """Gera código para branch incondicional"""
        target = inst.operands[0]
        self.emit(f"jmp {target.name}")
    
    def gen_cond_br(self, inst: Instruction):
        """Gera código para branch condicional"""
        cond = inst.operands[0]
        true_block = inst.operands[1]
        false_block = inst.operands[2]
        
        self.emit(f"movq {cond.name}, %rax")
        self.emit("testq %rax, %rax")
        self.emit(f"jnz {true_block.name}")
        self.emit(f"jmp {false_block.name}")
    
    def gen_call(self, inst: Instruction):
        """Gera código para chamada de função"""
        func = inst.operands[0]
        args = inst.operands[1:]
        result = inst.result
        
        # Salvar registradores caller-saved
        for reg in RegisterAllocator.CALLER_SAVED:
            self.emit(f"pushq %{reg}")
        
        # Passar argumentos
        for i, arg in enumerate(args[:6]):
            arg_reg = RegisterAllocator.ARG_REGISTERS[i]
            self.emit(f"movq {arg.name}, %{arg_reg}")
        
        # Chamar função
        self.emit(f"call {func.name}")
        
        # Restaurar registradores
        for reg in reversed(RegisterAllocator.CALLER_SAVED):
            self.emit(f"popq %{reg}")
        
        # Mover resultado se necessário
        if result:
            reg = self.reg_alloc.allocate(result.name)
            if reg and reg != 'rax':
                self.emit(f"movq %rax, %{reg}")
    
    def gen_ret(self, inst: Instruction):
        """Gera código para retorno"""
        if inst.operands:
            value = inst.operands[0]
            self.emit(f"movq {value.name}, %rax")
        
        # Jump para epilogue
        self.emit("jmp .Lepilogue0")
    
    def gen_phi(self, inst: Instruction):
        """Gera código para nó phi (simplificado)"""
        # Phi nodes são resolvidos no momento da geração de código
        # Aqui apenas movemos o primeiro valor
        if inst.operands:
            value = inst.operands[0]
            result = inst.result
            reg = self.reg_alloc.allocate(result.name)
            if reg:
                self.emit(f"movq {value.name}, %{reg}")


if __name__ == "__main__":
    # Teste
    from ulx_ir import *
    
    module = Module("test")
    
    # Função main
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
    
    # Gerar assembly
    codegen = X86_64CodeGen()
    assembly = codegen.generate(module)
    print(assembly)
