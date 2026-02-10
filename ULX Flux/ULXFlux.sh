#!/bin/bash

# ULX Flux - Script de Inicialização
# Gerencia o ambiente de tradução e otimizações de performance

LOG_FILE="$HOME/.ulx_flux.log"
echo "ULX Flux Iniciado em $(date)" > "$LOG_FILE"
exec 2>>"$LOG_FILE"

BASE_DIR="/opt/ulxflux"
[ ! -d "$BASE_DIR" ] && BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$BASE_DIR" || exit 1

# Otimizações de Performance (Modo Prime)
# Forçar performance máxima para a camada de tradução
export MESA_GL_VERSION_OVERRIDE=4.6
export MESA_GLSL_VERSION_OVERRIDE=460
export vblank_mode=0
export __GL_THREADED_OPTIMIZATIONS=1

# Iniciar o tradutor
echo "Lançando motor ULX Flux..." | tee -a "$LOG_FILE"
python3 "$BASE_DIR/src/main.py" "$@" 2>>"$LOG_FILE"

if [ $? -ne 0 ]; then
    echo "O ULX Flux fechou com erro. Verifique $LOG_FILE para detalhes."
fi
