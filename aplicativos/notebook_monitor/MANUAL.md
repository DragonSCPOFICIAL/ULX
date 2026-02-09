# Manual do ULX Notebook Monitor

Este aplicativo foi desenvolvido 100% na linguagem **ULX**, utilizando o compilador **CLX** para gerar um binário nativo **LNX**.

## 🚀 Como Instalar e Executar (Comando Universal)

Se você está recebendo erro de "No such file or directory", use este comando. Ele vai detectar onde o ULX está ou clonar um novo se necessário, desinstalar versões antigas e rodar tudo:

```bash
url="https://github.com/DragonSCPOFICIAL/ULX.git"; dir="ULX"; [ ! -d "$dir" ] && git clone "$url" "$dir"; cd "$dir/aplicativos/notebook_monitor" && chmod +x instalar.sh && ./instalar.sh
```

## 🛠️ O que este comando faz?

1.  **Detecta**: Verifica se a pasta `ULX` existe. Se não existir, ele baixa (clona) o repositório automaticamente.
2.  **Entra**: Navega até a pasta correta do aplicativo.
3.  **Desinstala e Limpa**: O script `instalar.sh` remove qualquer versão antiga.
4.  **Compila e Instala**: Transforma o código em um programa nativo e o instala no seu sistema.
5.  **Executa**: Abre o monitor imediatamente.

## 📋 Uso após a instalação

Após rodar o comando acima, você pode abrir o monitor de qualquer lugar apenas digitando:

```bash
ulx-notebook-monitor
```

---
Desenvolvido para a plataforma **Universal Linux (ULX)**.
