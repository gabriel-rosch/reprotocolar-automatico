# 📦 Como Distribuir o Migrador PEP

## Para Distribuir para Pessoas Não Técnicas

### 1. Preparar o Pacote

Inclua estes arquivos na pasta que será distribuída:

**Arquivos Essenciais:**
- ✅ `instalar.sh` (macOS/Linux) ou `instalar.bat` (Windows)
- ✅ `executar_web.sh` (macOS/Linux) ou `executar_web.bat` (Windows)
- ✅ `LEIA-ME.txt` (instruções rápidas)
- ✅ `INSTRUCOES_INSTALACAO.md` (instruções detalhadas)
- ✅ `gui_migrador_web.py` (interface web)
- ✅ `migrador_pep.py` (script principal)
- ✅ `config.py` (configurações)
- ✅ `requirements.txt` (dependências)
- ✅ `env.example` (exemplo de configuração)

**Arquivos Opcionais:**
- `gui_migrador.py` (GUI tkinter - pode não funcionar em todos os sistemas)
- `README.md` (documentação completa)
- `README_GUI.md` (guia da interface)

### 2. Instruções para o Usuário Final

**Envie estas instruções:**

```
═══════════════════════════════════════════════════════════════
    MIGRADOR PEP - Instruções de Instalação
═══════════════════════════════════════════════════════════════

📋 ANTES DE COMEÇAR:
───────────────────────────────────────────────────────────────
1. Certifique-se de ter Python 3 instalado
   • macOS: Já vem instalado ou instale via Homebrew
   • Windows: Baixe em https://www.python.org/downloads/
   • Durante a instalação no Windows, marque "Add Python to PATH"

📦 INSTALAÇÃO (Faça apenas uma vez):
───────────────────────────────────────────────────────────────

   macOS/Linux:
   1. Abra o Terminal
   2. Navegue até a pasta do projeto
   3. Execute: chmod +x instalar.sh && ./instalar.sh

   Windows:
   1. Abra o Prompt de Comando
   2. Navegue até a pasta do projeto
   3. Duplo clique em: instalar.bat
      OU execute: instalar.bat

🚀 USAR O SISTEMA:
───────────────────────────────────────────────────────────────

   macOS/Linux:
   • Duplo clique em: executar_web.sh
   • OU execute: ./executar_web.sh

   Windows:
   • Duplo clique em: executar_web.bat

   Depois:
   • Abra seu navegador
   • Acesse: http://localhost:5000
   • Use a interface gráfica!

📖 Para mais detalhes, leia: LEIA-ME.txt
═══════════════════════════════════════════════════════════════
```

### 3. Formato de Distribuição

**Opção A: ZIP/TAR**
```bash
# Criar arquivo ZIP
zip -r migrador-pep.zip . -x "*.pyc" "__pycache__/*" ".git/*" "*.log"
```

**Opção B: GitHub Release**
- Crie um release no GitHub
- Anexe o ZIP com todos os arquivos

**Opção C: Pendrive/HD Externo**
- Copie toda a pasta do projeto
- Inclua o `LEIA-ME.txt` na raiz

### 4. Checklist de Distribuição

Antes de distribuir, verifique:

- [ ] Todos os scripts têm permissão de execução (chmod +x)
- [ ] Arquivo `LEIA-ME.txt` está na raiz
- [ ] Arquivo `.env` NÃO está incluído (use `env.example`)
- [ ] Arquivos de log/temporários foram removidos
- [ ] Testou a instalação em um sistema limpo
- [ ] Instruções estão claras e em português

### 5. Suporte

Se o usuário tiver problemas:

1. Verifique se Python 3 está instalado: `python3 --version`
2. Verifique se pip está instalado: `pip3 --version`
3. Execute a instalação novamente: `./instalar.sh`
4. Verifique os logs de erro no terminal

### 6. Atualizações Futuras

Para atualizar o sistema:

1. Envie apenas os arquivos Python modificados
2. Ou envie um novo ZIP completo
3. O usuário pode simplesmente substituir os arquivos antigos

---

## 📝 Notas Importantes

- **NÃO inclua** o arquivo `.env` na distribuição (contém credenciais)
- **NÃO inclua** arquivos `.pyc` ou `__pycache__`
- **SEMPRE inclua** o `LEIA-ME.txt` com instruções claras
- **TESTE** a instalação em um sistema limpo antes de distribuir

