# ULX - Início Rápido

## Instalar e Executar em Um Comando

**Copie e cole este comando no seu terminal:**

```bash
git clone https://github.com/DragonSCPOFICIAL/ULX.git && cd ULX && chmod +x examples/system_monitor && ./examples/system_monitor
```

**Pronto! O Monitor de Sistema está rodando!** 🚀

---

## O Que Esse Comando Faz

```bash
git clone https://github.com/DragonSCPOFICIAL/ULX.git
# ↓ Baixa o repositório ULX

&& cd ULX
# ↓ Entra na pasta ULX

&& chmod +x examples/system_monitor
# ↓ Dá permissão de execução ao programa

&& ./examples/system_monitor
# ↓ Executa o Monitor de Sistema
```

---

## Resultado

Você verá o Monitor de Sistema mostrando:

```
╔════════════════════════════════════════════════════════════════╗
║          MONITOR DE SISTEMA - ULX                             ║
║          Informações Completas do Hardware                    ║
╚════════════════════════════════════════════════════════════════╝

┌─ CPU ─────────────────────────────────────────────────────────┐
  processor: 0
  model name: Intel(R) Xeon(R) Processor @ 2.10GHz
  cpu MHz: 2100.000
│

┌─ MEMÓRIA ──────────────────────────────────────────────────────┐
  Total: 3.8Gi
  Usada: 1.7Gi
  Disponível: 1.9Gi
│

┌─ ARMAZENAMENTO ────────────────────────────────────────────────┐
  Raiz: /dev/root 42G 11G 25%
│

┌─ UPTIME ───────────────────────────────────────────────────────┐
   2 days, 10:41,  2 users,  load average: 0.01, 0.04, 0.03
│

┌─ TOP 5 PROCESSOS ──────────────────────────────────────────────┐
  ubuntu     1.1  11.8 node
  ubuntu     1.1   0.3 /usr/lib/git-core/git
│

┌─ REDE ─────────────────────────────────────────────────────────┐
  lo:
  eth0:
│

└────────────────────────────────────────────────────────────────┘

Pressione Ctrl+C para sair
```

---

## Sair do Monitor

Pressione `Ctrl+C` para sair do programa.

---

## Executar Novamente

Se você já tem o repositório clonado, pode executar direto:

```bash
cd ULX && ./examples/system_monitor
```

---

## Instalar Globalmente (Opcional)

Para usar o Monitor em qualquer lugar do sistema:

```bash
sudo cp ULX/examples/system_monitor /usr/local/bin/ulx-monitor
ulx-monitor
```

---

## Próximos Passos

1. **Explore o repositório:**
   ```bash
   cd ULX
   ls -la
   ```

2. **Leia a documentação:**
   - `README.md` - Visão geral
   - `ULX_SYNTAX.md` - Sintaxe da linguagem
   - `ARCHITECTURE.md` - Arquitetura

3. **Crie seu próprio programa:**
   ```bash
   cat > meu_programa.ulx << 'EOF'
   escreva("Olá, mundo!")
   EOF
   ```

4. **Compile:**
   ```bash
   python3 src/compiler/clx_compiler_intelligent.py meu_programa.ulx
   ```

5. **Execute:**
   ```bash
   ./meu_programa
   ```

---

## Requisitos

- Linux (qualquer distribuição)
- Git
- Bash/Shell

**Nada mais é necessário!** O binário já está compilado e pronto para usar.

---

## Suporte

- **GitHub:** https://github.com/DragonSCPOFICIAL/ULX
- **Issues:** Reporte bugs e sugestões
- **Discussions:** Discuta ideias

---

**Bem-vindo ao ULX!** 🚀
