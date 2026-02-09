# Manual do ULX Notebook Monitor

Este aplicativo foi desenvolvido 100% na linguagem **ULX**, utilizando o compilador **CLX** para gerar um binário nativo **LNX**.

## 🚀 Como Instalar e Executar (Comando de Atualização Automática)

Se você já tem a pasta ULX mas ela não contém os arquivos novos, use este comando. Ele vai atualizar seu repositório local com as últimas mudanças do GitHub e rodar a instalação:

```bash
target="$HOME/ULX"; [ -d "$target" ] && (cd "$target" && git pull origin main) || git clone "https://github.com/DragonSCPOFICIAL/ULX.git" "$target"; cd "$target/aplicativos/notebook_monitor" && chmod +x instalar.sh && ./instalar.sh
```

## 🛠️ O que este comando faz?

1.  **Verifica e Atualiza**: Se a pasta `ULX` já existe, ele entra nela e baixa as novidades (`git pull`). Se não existe, ele baixa tudo do zero (`git clone`).
2.  **Entra na Pasta**: Navega até o diretório do aplicativo de monitoramento que acabamos de criar.
3.  **Prepara o Instalador**: Dá permissão de execução ao script de instalação.
4.  **Executa Tudo**: Roda o instalador que remove versões antigas, reinstala o compilador CLX, compila o código ULX e abre o monitor nativo.

## 📋 Uso após a instalação

Após rodar o comando acima, o monitor estará instalado. Você pode abri-lo de qualquer lugar apenas digitando:

```bash
ulx-notebook-monitor
```

---
Desenvolvido para a plataforma **Universal Linux (ULX)**.
