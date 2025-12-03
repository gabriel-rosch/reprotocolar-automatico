# 📥 Como Baixar e Usar o Projeto

## Para Pessoas Não Técnicas

### 🌐 Opção 1: Baixar como ZIP (MAIS FÁCIL)

1. **Acesse o projeto no GitHub:**
   - Vá para: https://github.com/gabriel-rosch/reprotocolar-automatico
   - Ou procure por: `gabriel-rosch/reprotocolar-automatico`

2. **Baixe o projeto:**
   - Clique no botão verde **"Code"** (no topo da página)
   - Clique em **"Download ZIP"**
   - O arquivo será baixado para sua pasta de Downloads

3. **Extraia o arquivo:**
   - **macOS:** Duplo clique no arquivo ZIP
   - **Windows:** Clique com botão direito → "Extrair tudo"
   - **Linux:** Clique com botão direito → "Extrair aqui"

4. **Pronto!** Agora siga as instruções de instalação abaixo.

---

### 💻 Opção 2: Usar Git (Para Pessoas Técnicas)

Se você tem Git instalado:

```bash
git clone https://github.com/gabriel-rosch/reprotocolar-automatico.git
cd reprotocolar-automatico
```

---

## 📋 O Que Você Precisa Ter

### ✅ Requisitos Mínimos:

1. **Python 3.8 ou superior**
   - **macOS:** Geralmente já vem instalado
   - **Windows:** Baixe em: https://www.python.org/downloads/
   - **Linux:** `sudo apt-get install python3`

2. **Conexão com Internet**
   - Para baixar o projeto
   - Para instalar dependências
   - Para usar o sistema

3. **Navegador Web** (Chrome, Firefox, Safari, Edge)
   - Para usar a interface web

---

## 🚀 Passos Após Baixar

### 1️⃣ Instalação (Faça apenas uma vez)

**macOS/Linux:**
```bash
cd reprotocolar-automatico
chmod +x instalar.sh
./instalar.sh
```

**Windows:**
```bash
cd reprotocolar-automatico
instalar_windows_automatico.bat
```
(ou duplo clique em `instalar_windows_automatico.bat`)

💡 **Se tiver erro de Visual C++ Build Tools:**
   - Veja o guia: `INSTALACAO_WINDOWS.md`
   - Ou use: `instalar_windows_automatico.bat` (resolve automaticamente)

### 2️⃣ Usar o Sistema

**macOS/Linux:**
```bash
./executar_web.sh
```

**Windows:**
```bash
executar_web.bat
```
(ou duplo clique em `executar_web.bat`)

### 3️⃣ Acessar a Interface

1. Abra seu navegador
2. Acesse: **http://localhost:5000**
3. Use a interface gráfica!

---

## 📖 Arquivos Importantes

Após baixar, você encontrará:

- **LEIA-ME.txt** → Instruções rápidas (LEIA PRIMEIRO!)
- **INSTRUCOES_INSTALACAO.md** → Guia detalhado de instalação
- **instalar.sh / instalar.bat** → Script de instalação
- **executar_web.sh / executar_web.bat** → Para iniciar o sistema

---

## ❓ Dúvidas Frequentes

### "Não consigo baixar do GitHub"
- Use a **Opção 1 (ZIP)** - é mais fácil
- Ou peça para alguém enviar o ZIP por email/pendrive

### "Não tenho Python instalado"
- **Windows:** Baixe em https://www.python.org/downloads/
- **macOS:** Já vem instalado (ou instale via Homebrew)
- **Linux:** `sudo apt-get install python3`

### "O instalador não funciona"
- Verifique se Python está instalado: `python3 --version`
- Tente executar manualmente os comandos do `instalar.sh`

### "A interface não abre"
- Verifique se executou `executar_web.sh` (ou `executar_web.bat`)
- Verifique se a porta 5000 está livre
- Tente reiniciar o computador

---

## 🔗 Links Úteis

- **Projeto no GitHub:** https://github.com/gabriel-rosch/reprotocolar-automatico
- **Download Python:** https://www.python.org/downloads/
- **Documentação Python:** https://docs.python.org/

---

## 💡 Dica

**Sempre comece lendo o arquivo `LEIA-ME.txt`!** Ele tem todas as instruções básicas em português simples.

---

## 📞 Precisa de Ajuda?

Se tiver problemas:
1. Leia o arquivo `INSTRUCOES_INSTALACAO.md`
2. Verifique se Python está instalado: `python3 --version`
3. Tente executar a instalação novamente


