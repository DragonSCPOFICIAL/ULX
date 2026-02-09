# Manual do ULX Notebook Monitor

Este aplicativo foi desenvolvido 100% na linguagem **ULX**, utilizando o compilador **CLX** para gerar um binário nativo **LNX**.

## 🚀 Como Instalar e Executar

Este comando realiza a limpeza completa, instala a versão estável e cria um **atalho no seu menu de aplicativos**:

```bash
sudo rm -f /usr/local/bin/clx_engine.py /usr/local/bin/ulxc; target="$HOME/ULX"; rm -rf "$target"; git clone "https://github.com/DragonSCPOFICIAL/ULX.git" "$target"; cd "$target/aplicativos/notebook_monitor" && chmod +x instalar.sh && ./instalar.sh
```

## 🛠️ O que este comando faz?

1.  **Limpeza e Atualização**: Garante que você tenha o código mais recente e sem erros.
2.  **Compilação Nativa**: Gera o binário de alta performance através do **CLX**.
3.  **Integração com o Sistema**: Cria um atalho chamado **"ULX Notebook Monitor"** no menu do seu Arch Linux.
4.  **Execução Independente**: Agora você pode abrir o monitor sem precisar digitar comandos no terminal.

## 📋 Como usar

Existem duas formas de abrir o monitor após a instalação:

1.  **Pelo Menu**: Procure por "ULX Notebook Monitor" na sua lista de aplicativos.
2.  **Pelo Terminal**: Digite `ulx-notebook-monitor`.

---
Desenvolvido para a plataforma **Universal Linux (ULX)**.
