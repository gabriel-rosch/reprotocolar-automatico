# 📖 Instruções de Instalação - Migrador PEP

## 🚀 Para Usuários Não Técnicos

### Passo 1: Instalar Python (se ainda não tiver)

#### macOS:
1. Abra o Terminal (procure por "Terminal" no Spotlight)
2. Execute:
   ```bash
   brew install python3
   ```
   Ou baixe em: https://www.python.org/downloads/

#### Windows:
1. Baixe Python em: https://www.python.org/downloads/
2. Durante a instalação, **marque a opção "Add Python to PATH"**
3. Clique em "Install Now"

#### Linux:
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

### Passo 2: Instalar o Migrador PEP

1. Abra o Terminal (macOS/Linux) ou Prompt de Comando (Windows)
2. Navegue até a pasta do projeto:
   ```bash
   cd /caminho/para/reprotocolar-automatico
   ```
3. Execute o instalador:

   **macOS/Linux:**
   ```bash
   chmod +x instalar.sh
   ./instalar.sh
   ```

   **Windows:**
   ```bash
   instalar.bat
   ```

### Passo 3: Usar o Migrador

#### Opção 1: Interface Web (Recomendado - Mais Fácil)

1. Execute:
   ```bash
   python3 gui_migrador_web.py
   ```

2. Abra seu navegador e acesse:
   ```
   http://localhost:5000
   ```

3. Use a interface gráfica no navegador!

#### Opção 2: Linha de Comando

```bash
python3 migrador_pep.py 664276 /caminho/para/pasta
```

---

## 🔧 Solução de Problemas

### Erro: "python3: command not found"
- **Solução:** Instale Python 3 primeiro (veja Passo 1)

### Erro: "pip: command not found"
- **Solução:** Execute:
  ```bash
  python3 -m ensurepip --upgrade
  ```

### Erro ao instalar Playwright
- **Solução:** Execute manualmente:
  ```bash
  python3 -m playwright install chromium
  ```

### Erro: "Permission denied"
- **Solução macOS/Linux:** Execute:
  ```bash
  chmod +x instalar.sh
  ```

### Interface não abre
- Verifique se a porta 5000 está livre
- Tente fechar outros programas que usam a porta

---

## 📞 Precisa de Ajuda?

Se encontrar problemas:
1. Verifique se Python 3 está instalado: `python3 --version`
2. Verifique se pip está instalado: `pip3 --version`
3. Tente reinstalar: `./instalar.sh` (macOS/Linux) ou `instalar.bat` (Windows)

---

## ✅ Verificação Rápida

Execute estes comandos para verificar se está tudo OK:

```bash
# Verificar Python
python3 --version

# Verificar pip
pip3 --version

# Verificar Playwright
python3 -c "import playwright; print('OK')"
```

Se todos retornarem sem erro, está tudo instalado corretamente! ✅

