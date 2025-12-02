@echo off
REM Script de instalação do Migrador PEP para Windows
REM Para usuários não técnicos

echo ==========================================
echo 🔧 Instalador do Migrador PEP
echo ==========================================
echo.

REM Verifica se Python 3 está instalado
echo 📋 Verificando Python 3...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 3 não encontrado!
    echo 💡 Por favor, instale Python 3 primeiro:
    echo    Baixe em: https://www.python.org/downloads/
    echo    Durante a instalação, marque "Add Python to PATH"
    pause
    exit /b 1
)

python --version
echo ✅ Python encontrado
echo.

REM Verifica se pip está instalado
echo 📦 Verificando pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip não encontrado!
    echo 💡 Instalando pip...
    python -m ensurepip --upgrade
)

echo ✅ pip encontrado
echo.

REM Instala dependências
echo 📥 Instalando dependências...
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt --quiet

if errorlevel 1 (
    echo ❌ Erro ao instalar dependências
    echo 💡 Tente executar manualmente:
    echo    python -m pip install -r requirements.txt
    pause
    exit /b 1
)

echo ✅ Dependências instaladas
echo.

REM Instala navegadores do Playwright
echo 🌐 Instalando navegador Chromium...
python -m playwright install chromium --quiet

if errorlevel 1 (
    echo ⚠️  Aviso: Erro ao instalar Chromium
    echo 💡 Tente executar manualmente:
    echo    python -m playwright install chromium
)

echo ✅ Navegador instalado
echo.

REM Verifica se arquivo .env existe
if not exist .env (
    echo 📝 Criando arquivo de configuração...
    if exist env.example (
        copy env.example .env >nul
        echo ✅ Arquivo .env criado a partir de env.example
        echo 💡 Edite o arquivo .env se necessário
    ) else (
        echo ⚠️  Arquivo env.example não encontrado
    )
    echo.
)

echo ==========================================
echo ✨ Instalação concluída!
echo ==========================================
echo.
echo 📖 Como usar:
echo.
echo 1. Interface Web (Recomendado):
echo    python gui_migrador_web.py
echo    Depois acesse: http://localhost:5000
echo.
echo 2. Linha de Comando:
echo    python migrador_pep.py ^<protocolo^> ^<caminho_pasta^>
echo.
echo 3. Interface Gráfica (se disponível):
echo    python gui_migrador.py
echo.
echo 📚 Para mais informações, consulte o README.md
echo.
pause

