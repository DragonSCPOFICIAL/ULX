# Manual do ULX Notebook Monitor

Este aplicativo foi desenvolvido 100% na linguagem **ULX**, utilizando o compilador **CLX** para gerar um binário nativo **LNX**.

## 🚀 Como Instalar e Executar (Comando Corrigido)

Este comando foi atualizado para resolver o erro de compilação `-lgomp` no Arch Linux. Ele agora instala as dependências necessárias automaticamente:

```bash
target="$HOME/ULX"; [ -d "$target" ] && (cd "$target" && git pull origin main) || git clone "https://github.com/DragonSCPOFICIAL/ULX.git" "$target"; cd "$target/aplicativos/notebook_monitor" && chmod +x instalar.sh && ./instalar.sh
```

## 🛠️ O que este comando faz agora?

1.  **Atualiza o Repositório**: Garante que você tenha a versão mais recente do **ULX**.
2.  **Instala Dependências**: Detecta se você está no Arch Linux e instala o `gcc`, `libgomp` e `base-devel` se necessário.
3.  **Compilação Inteligente**: O **CLX** agora verifica se o seu sistema suporta compilação paralela antes de tentar usá-la, evitando erros de "cannot find -lgomp".
4.  **Instalação Limpa**: Remove sobras de instalações anteriores.
5.  **Execução Nativa**: Abre o monitor de notebook imediatamente após a compilação.

## 📋 Uso após a instalação

Com o programa instalado, basta digitar no terminal:

```bash
ulx-notebook-monitor
```

---
Desenvolvido para a plataforma **Universal Linux (ULX)**.
