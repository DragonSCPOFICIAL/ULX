# Manual do ULX Notebook Monitor

Este aplicativo foi desenvolvido 100% na linguagem **ULX**, utilizando o compilador **CLX** para gerar um binário nativo **LNX**.

## 🚀 Como Instalar e Executar (Comando de Limpeza e Instalação)

Se você está recebendo erros de compilação ou de diretório, use este comando. Ele realiza uma limpeza completa no sistema, remove versões antigas problemáticas e instala a versão 100% estável:

```bash
sudo rm -f /usr/local/bin/clx_engine.py /usr/local/bin/ulxc; target="$HOME/ULX"; rm -rf "$target"; git clone "https://github.com/DragonSCPOFICIAL/ULX.git" "$target"; cd "$target/aplicativos/notebook_monitor" && chmod +x instalar.sh && ./instalar.sh
```

## 🛠️ O que este comando faz?

1.  **Limpeza Total**: Remove o motor do compilador antigo e a pasta `ULX` para evitar conflitos de arquivos "sujos".
2.  **Download Limpo**: Baixa a versão mais recente e corrigida (sem a dependência de `libgomp`).
3.  **Instalação Estável**: Configura o novo compilador **CLX** e gera o binário nativo **LNX**.
4.  **Execução Imediata**: Abre o monitor de notebook assim que a compilação termina.

## 📋 Uso após a instalação

Após a conclusão, o monitor estará instalado globalmente. Você pode abri-lo de qualquer lugar apenas digitando:

```bash
ulx-notebook-monitor
```

---
Desenvolvido para a plataforma **Universal Linux (ULX)**.
