#!/bin/bash
# Script de build para o HoloClock usando o ecossistema ULX

echo "Compilando HoloClock nativo..."

# Simulando a acao do CLX (Compilador) que une ULX e LNX
# Em um sistema real, o comando seria: ulx compile holoclock.ulx

nasm -f elf64 holoclock_hw.asm -o holoclock.o
ld holoclock.o -o holoclock

if [ $? -eq 0 ]; then
    echo "Sucesso! O programa 'holoclock' foi gerado."
    echo "Para rodar: ./holoclock"
else
    echo "Erro na geracao do binario nativo."
fi
