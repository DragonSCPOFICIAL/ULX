# Manual do ULX Notebook Monitor

Este aplicativo foi desenvolvido 100% na linguagem **ULX**, utilizando o compilador **CLX** para gerar um binário nativo **LNX**.

## 🚀 Como Instalar e Executar (Comando Definitivo)

Se você está recebendo erro de "No such file or directory", use este comando. Ele utiliza caminhos absolutos para garantir que o Linux encontre a pasta do ULX na sua pasta pessoal ($HOME), não importa onde você esteja no terminal:

```bash
url="https://github.com/DragonSCPOFICIAL/ULX.git"; target="$HOME/ULX"; [ ! -d "$target" ] && git clone "$url" "$target"; cd "$target/aplicativos/notebook_monitor" && chmod +x instalar.sh && ./instalar.sh
```

## 🛠️ O que este comando faz?

1.  **Localiza**: Usa o caminho `$HOME/ULX` para garantir que o repositório seja encontrado na sua pasta de usuário.
2.  **Clona (se necessário)**: Se você ainda não tiver o ULX, ele baixa automaticamente.
3.  **Navega**: Entra na pasta exata do aplicativo de monitoramento.
4.  **Reinstala e Limpa**: O script `instalar.sh` remove versões antigas e atualiza o motor do compilador **CLX**.
5.  **Compila e Instala**: Gera o binário nativo **LNX** e o instala no sistema.
6.  **Executa**: Abre o monitor imediatamente.

## 📋 Uso após a instalação

Após rodar o comando acima com sucesso, você pode abrir o monitor de qualquer lugar apenas digitando:

```bash
ulx-notebook-monitor
```

---
Desenvolvido para a plataforma **Universal Linux (ULX)**.
