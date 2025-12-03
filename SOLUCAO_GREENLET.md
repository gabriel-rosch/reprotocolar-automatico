# 🔧 Solução para Erro do Greenlet no Windows

Se você está vendo este erro:
```
error: Microsoft Visual C++ 14.0 or greater is required
ERROR: Failed building wheel for greenlet
```

Este guia resolve o problema **sem precisar instalar Visual C++ Build Tools**.

---

## 🚀 Solução Rápida (Recomendada)

### Opção 1: Usar Script Automático

Execute:
```cmd
instalar_windows_automatico.bat
```

O script tenta automaticamente instalar versões pré-compiladas do greenlet.

---

## 🔧 Soluções Manuais

### Solução 1: Instalar Greenlet Pré-Compilado

Abra o Prompt de Comando e execute:

```cmd
python -m pip install --upgrade pip setuptools wheel
python -m pip install --only-binary :all: greenlet
python -m pip install -r requirements.txt
```

### Solução 2: Instalar Versão Específica do Greenlet

```cmd
python -m pip install greenlet==3.0.3
python -m pip install -r requirements.txt
```

### Solução 3: Instalar Sem Isolamento de Build

```cmd
python -m pip install --upgrade pip setuptools wheel
python -m pip install greenlet --no-build-isolation
python -m pip install -r requirements.txt
```

### Solução 4: Instalar Dependências Uma por Uma

```cmd
python -m pip install --upgrade pip setuptools wheel
python -m pip install playwright==1.40.0
python -m pip install beautifulsoup4==4.12.2
python -m pip install requests==2.31.0
python -m pip install python-dotenv==1.0.0
python -m pip install --only-binary :all: greenlet
python -m pip install flask==3.0.0
python -m playwright install chromium
```

---

## 🎯 Por Que Isso Acontece?

O `greenlet` é uma dependência do Flask/SQLAlchemy que precisa ser **compilada** em C. No Windows, isso requer o Microsoft Visual C++ Build Tools.

**Mas** existem versões **pré-compiladas** (wheels) que não precisam compilar!

---

## ✅ Verificar se Funcionou

Execute:

```cmd
python -c "import greenlet; import flask; print('✅ Tudo OK!')"
```

Se não der erro, está funcionando! ✅

---

## 🐛 Se Nada Funcionar

### Última Opção: Instalar Visual C++ Build Tools

1. **Baixe:**
   - https://visualstudio.microsoft.com/visual-cpp-build-tools/

2. **Instale:**
   - Execute o instalador
   - Marque: **"C++ build tools"** (Desktop development with C++)
   - Clique em "Instalar"
   - Aguarde (10-20 minutos)

3. **Reinicie o computador**

4. **Execute novamente:**
   ```cmd
   instalar_windows_automatico.bat
   ```

---

## 💡 Dicas

- **Use Python 3.11 ou 3.12** - Versões mais recentes têm mais wheels pré-compilados
- **Sempre atualize pip primeiro:** `python -m pip install --upgrade pip`
- **O script automático** (`instalar_windows_automatico.bat`) tenta todas essas soluções automaticamente

---

## 📞 Ainda com Problemas?

Se nenhuma solução funcionar:

1. Verifique a versão do Python: `python --version`
2. Tente Python 3.11 ou 3.12
3. Verifique se pip está atualizado: `python -m pip install --upgrade pip`
4. Tente instalar em um ambiente virtual (avançado)

