# 🪟 Guia de Instalação para Windows

Este guia resolve os problemas comuns de instalação no Windows, especialmente o erro do **Microsoft Visual C++ Build Tools**.

---

## 🚀 Instalação Rápida (Recomendado)

### Passo 1: Instalar Python

1. **Baixe Python:**
   - Acesse: https://www.python.org/downloads/
   - Baixe a versão mais recente (3.11 ou 3.12)

2. **Durante a instalação:**
   - ✅ **MARQUE:** "Add Python to PATH" (MUITO IMPORTANTE!)
   - ✅ **MARQUE:** "Install for all users" (se possível)
   - Clique em "Install Now"

3. **Verifique se funcionou:**
   - Abra o Prompt de Comando
   - Digite: `python --version`
   - Deve mostrar algo como: `Python 3.11.x`

### Passo 2: Instalar o Migrador PEP

**Opção A - Script Automático (RECOMENDADO):**
1. Duplo clique em: `instalar_windows_automatico.bat`
2. Aguarde a instalação (pode levar alguns minutos)
3. Pronto! ✅

**Opção B - Script Normal:**
1. Duplo clique em: `instalar.bat`
2. Se der erro, veja as soluções abaixo

---

## ❌ Erro: "Microsoft Visual C++ 14.0 or greater is required" (Greenlet)

Este é o erro mais comum no Windows, geralmente relacionado ao `greenlet`. 

**📖 Guia específico:** Veja `SOLUCAO_GREENLET.md` para soluções detalhadas sem precisar instalar Visual C++.

Aqui estão as soluções rápidas:

### 🔧 Solução 1: Usar Script Automático (MAIS FÁCIL)

O script `instalar_windows_automatico.bat` tenta automaticamente instalar versões pré-compiladas do greenlet, evitando a necessidade de compilar.

**Se ainda der erro de greenlet:**
- Veja o guia específico: `SOLUCAO_GREENLET.md`
- Ou continue com a Solução 2 abaixo

### 🔧 Solução 2: Instalar Visual C++ Build Tools (Se necessário)

1. **Acesse:**
   - https://visualstudio.microsoft.com/visual-cpp-build-tools/

2. **Baixe e instale:**
   - Clique em "Baixar Build Tools"
   - Execute o instalador
   - Marque: **"C++ build tools"** (Desktop development with C++)
   - Clique em "Instalar"
   - Aguarde a instalação (pode levar 10-20 minutos)

3. **Reinicie o computador**

4. **Execute novamente:**
   - `instalar.bat` ou `instalar_windows_automatico.bat`

### 🔧 Solução 3: Usar Python Mais Recente

Versões mais recentes do Python (3.11+) geralmente têm menos problemas:

1. **Desinstale o Python atual** (se tiver)
2. **Baixe Python 3.12:**
   - https://www.python.org/downloads/
3. **Instale com:**
   - ✅ "Add Python to PATH"
   - ✅ "Install for all users"
4. **Execute novamente:** `instalar.bat`

### 🔧 Solução 4: Instalação Manual (Avançado)

Abra o Prompt de Comando como **Administrador** e execute:

```cmd
python -m pip install --upgrade pip
python -m pip install playwright==1.40.0
python -m pip install beautifulsoup4==4.12.2
python -m pip install requests==2.31.0
python -m pip install python-dotenv==1.0.0
python -m pip install flask==3.0.0
python -m playwright install chromium
```

---

## ✅ Verificar se Está Tudo OK

Execute estes comandos no Prompt de Comando:

```cmd
REM Verificar Python
python --version

REM Verificar pip
python -m pip --version

REM Verificar se as dependências estão instaladas
python -c "import playwright; import flask; print('✅ Tudo OK!')"
```

Se todos funcionarem sem erro, está tudo instalado! ✅

---

## 🐛 Outros Problemas Comuns

### "python não é reconhecido como comando"

**Solução:**
- Python não está no PATH
- Reinstale o Python e **marque "Add Python to PATH"**
- Ou adicione manualmente ao PATH (avançado)

### "pip não é reconhecido"

**Solução:**
```cmd
python -m ensurepip --upgrade
```

### "Erro ao instalar Playwright"

**Solução:**
```cmd
python -m playwright install chromium
```

### "Porta 5000 já está em uso"

**Solução:**
- Feche outros programas
- Ou o sistema tentará usar outra porta automaticamente

---

## 📞 Precisa de Ajuda?

Se nada funcionar:

1. **Use o script automático:**
   - `instalar_windows_automatico.bat`
   - Ele tenta várias estratégias automaticamente

2. **Verifique os requisitos:**
   - Python 3.8+ instalado
   - "Add Python to PATH" marcado
   - Conexão com internet

3. **Tente instalar manualmente:**
   - Veja "Solução 3" acima

---

## 💡 Dicas

- **Sempre marque "Add Python to PATH"** durante a instalação do Python
- **Use Python 3.11 ou 3.12** para menos problemas
- **Execute como Administrador** se tiver problemas de permissão
- **O script automático** (`instalar_windows_automatico.bat`) resolve a maioria dos problemas

---

## 🎯 Após Instalar

1. **Execute o sistema:**
   - Duplo clique em: `executar_web.bat`
   - Ou: `python gui_migrador_web.py`

2. **Acesse no navegador:**
   - http://localhost:5000

3. **Pronto para usar!** 🎉

