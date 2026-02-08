# 📦 Sistema de Pacotes ULX (.ulx)

O formato `.ulx` é um **Universal Linux eXecutable**. Ele foi criado para acabar com a "frescura" de dependências e tornar a distribuição de software no Linux tão fácil quanto no Windows (.exe) ou Android (.apk).

## 🏗️ Anatomia de um arquivo .ulx

Um arquivo `.ulx` não é apenas um binário; ele é um container inteligente que contém:
1. **Cabeçalho ULX**: Metadados do app (Nome, Versão, Autor).
2. **Recurso de Ícone**: A imagem que o sistema usará para exibir o app.
3. **Binário Estático**: O código de máquina puro que fala com o Kernel.
4. **Assets Embutidos**: Imagens, sons e fontes usados pelo programa.

## 🛠️ Como criar seu pacote manualmente

Embora o **ULX Studio** faça isso com um botão, você pode usar a ferramenta de linha de comando:

```bash
ulx-pack <seu_codigo.ulx> <seu_icone.png> "NomeDoApp"
```

## 🚀 Como distribuir

Basta enviar o arquivo `NomeDoApp.ulx` para qualquer pessoa. 
- Se ela tiver o **ULX Base** instalado, basta dar dois cliques para instalar/rodar.
- O programa rodará com performance nativa em Arch, Ubuntu, Fedora, etc.

## 🛡️ Segurança
O formato `.ulx` suporta assinatura digital (em desenvolvimento) para garantir que o programa não foi alterado por terceiros.
