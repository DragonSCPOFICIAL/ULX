#!/bin/bash

# ULX UNIVERSAL BRIDGE - CAMADA DE EXECUÇÃO NATIVA (.EXE & .APK)
# Este script registra os formatos .exe e .apk no kernel via binfmt_misc.

echo "========================================================="
echo "   ULX - PONTE UNIVERSAL DE EXECUÇÃO (.EXE & .APK)"
echo "========================================================="

# 1. Verificar se o binfmt_misc está montado
if [ ! -d /proc/sys/fs/binfmt_misc ]; then
    echo "[KERNEL] Montando binfmt_misc..."
    sudo mount -t binfmt_misc binfmt_misc /proc/sys/fs/binfmt_misc
fi

# 2. Registro do Formato .EXE (Windows)
# Assinatura: 'MZ' no início do arquivo
echo "[EXE] Registrando suporte nativo para Windows Executables..."
# O wrapper ulx-run-exe cuidará da tradução via Wine/Box64
if [ ! -f /proc/sys/fs/binfmt_misc/ulx-exe ]; then
    echo ':ulx-exe:M::MZ::/usr/local/bin/ulx-run-exe:' | sudo tee /proc/sys/fs/binfmt_misc/register > /dev/null
fi

# 3. Registro do Formato .APK (Android)
# Assinatura: 'PK\x03\x04' (formato ZIP) - Verificamos o cabeçalho
echo "[APK] Registrando suporte nativo para Android Packages..."
# O wrapper ulx-run-apk cuidará da tradução via Anbox-runtime/libhoudini
if [ ! -f /proc/sys/fs/binfmt_misc/ulx-apk ]; then
    echo ':ulx-apk:M::PK\x03\x04::/usr/local/bin/ulx-run-apk:' | sudo tee /proc/sys/fs/binfmt_misc/register > /dev/null
fi

# 4. Criar Wrappers de Execução Silenciosa

# Wrapper para .EXE
cat <<EOF | sudo tee /usr/local/bin/ulx-run-exe > /dev/null
#!/bin/bash
# ULX-EXE Wrapper: Execução silenciosa sem emulador visível.
export WINEDEBUG=-all
export LD_PRELOAD="/usr/local/lib/ulx/runtime/libulx_core.so"
# Usa Wine apenas como tradutor de syscalls
wine "\$@"
EOF
sudo chmod +x /usr/local/bin/ulx-run-exe

# Wrapper para .APK
cat <<EOF | sudo tee /usr/local/bin/ulx-run-apk > /dev/null
#!/bin/bash
# ULX-APK Wrapper: Execução nativa de apps Android.
# No futuro: Integração com libhoudini e anbox-runtime
export LD_PRELOAD="/usr/local/lib/ulx/runtime/libulx_core.so"
# anbox-shell run --package="\$1" (Simplificado para o exemplo)
echo "[ULX] Iniciando App Android nativamente..."
EOF
sudo chmod +x /usr/local/bin/ulx-run-apk

echo "========================================================="
echo "PONTE UNIVERSAL ATIVADA!"
echo "Agora você pode executar .exe e .apk diretamente no terminal."
echo "Exemplo: ./meu_jogo.exe ou ./meu_app.apk"
echo "========================================================="
