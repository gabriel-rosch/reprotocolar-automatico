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

REM Atualiza pip primeiro
echo 🔄 Atualizando pip...
python -m pip install --upgrade pip --quiet
echo.

REM Instala dependências com múltiplas estratégias
echo 📥 Instalando dependências...
echo    (Isso pode levar alguns minutos...)
echo.

REM Tenta primeiro com wheels pré-compilados (mais rápido)
python -m pip install --only-binary :all: -r requirements.txt --quiet 2>nul
if not errorlevel 1 (
    echo ✅ Dependências instaladas com sucesso!
    goto :deps_ok
)

REM Se falhou, tenta instalação normal
python -m pip install -r requirements.txt --quiet
if not errorlevel 1 (
    echo ✅ Dependências instaladas com sucesso!
    goto :deps_ok
)

REM Se ainda falhou, tenta instalar uma por uma
echo ⚠️  Tentando instalar dependências individualmente...
python -m pip install playwright==1.40.0 --quiet
python -m pip install beautifulsoup4==4.12.2 --quiet
python -m pip install requests==2.31.0 --quiet
python -m pip install python-dotenv==1.0.0 --quiet
python -m pip install flask==3.0.0 --quiet

REM Verifica se pelo menos as principais funcionam
python -c "import playwright; import flask; print('OK')" >nul 2>&1
if not errorlevel 1 (
    echo ✅ Dependências principais instaladas!
    goto :deps_ok
)

REM Se chegou aqui, houve erro crítico
echo.
echo ==========================================
echo ❌ ERRO: Falha na instalação de dependências
echo ==========================================
echo.
echo 💡 PROBLEMA COMUM NO WINDOWS:
echo    Algumas dependências precisam ser COMPILADAS
echo    e isso requer o Microsoft Visual C++ Build Tools.
echo.
echo 🔧 SOLUÇÕES:
echo.
echo Opção 1 - INSTALAR VISUAL C++ BUILD TOOLS:
echo    1. Abra: https://visualstudio.microsoft.com/visual-cpp-build-tools/
echo    2. Baixe e instale "Microsoft C++ Build Tools"
echo    3. Execute este script novamente
echo.
echo Opção 2 - USAR SCRIPT AUTOMÁTICO:
echo    Execute: instalar_windows_automatico.bat
echo    (Ele tenta resolver automaticamente)
echo.
echo Opção 3 - INSTALAÇÃO MANUAL:
echo    python -m pip install --upgrade pip
echo    python -m pip install playwright beautifulsoup4 requests python-dotenv flask
echo.
echo ==========================================
echo.
pause
exit /b 1

:deps_ok

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

