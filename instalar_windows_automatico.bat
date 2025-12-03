@echo off
REM Script de instalação AUTOMÁTICA do Migrador PEP para Windows
REM Detecta e resolve problemas de compilação automaticamente

echo ==========================================
echo 🔧 Instalador Automático - Migrador PEP
echo ==========================================
echo.

REM Verifica se Python 3 está instalado
echo 📋 Verificando Python 3...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 3 não encontrado!
    echo.
    echo 💡 INSTALAÇÃO DO PYTHON:
    echo    1. Baixe em: https://www.python.org/downloads/
    echo    2. Durante a instalação, MARQUE "Add Python to PATH"
    echo    3. Clique em "Install Now"
    echo    4. Execute este script novamente após instalar
    echo.
    pause
    exit /b 1
)

python --version
echo ✅ Python encontrado

REM Verifica versão do Python
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo 🔍 Versão detectada: %PYTHON_VERSION%
echo.

REM Avisa se a versão é muito nova (pode não ter wheels)
echo %PYTHON_VERSION% | findstr /R "^3\.1[4-9]\." >nul
if not errorlevel 1 (
    echo ⚠️  AVISO: Python %PYTHON_VERSION% é muito recente!
    echo    Algumas dependências podem não ter wheels pré-compilados.
    echo    Recomendado: Use Python 3.11 ou 3.12 para melhor compatibilidade.
    echo.
)

REM Verifica se pip está instalado
echo 📦 Verificando pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip não encontrado!
    echo 💡 Instalando pip...
    python -m ensurepip --upgrade
    if errorlevel 1 (
        echo ❌ Erro ao instalar pip
        pause
        exit /b 1
    )
)

echo ✅ pip encontrado
echo.

REM Atualiza pip primeiro
echo 🔄 Atualizando pip...
python -m pip install --upgrade pip --quiet
echo.

REM Tenta instalar dependências com estratégias diferentes
echo 📥 Instalando dependências...
echo    (Isso pode levar alguns minutos...)
echo.

REM Estratégia 1: Atualiza ferramentas de build primeiro
echo 🔍 Preparando ambiente...
python -m pip install --upgrade pip setuptools wheel --quiet
echo.

REM Estratégia 2: Tenta instalar greenlet com múltiplas abordagens
echo 🔍 Tentativa 1: Instalando greenlet (dependência crítica)...
echo    Tentando versão mais recente com wheels...
python -m pip install --only-binary :all: greenlet --quiet 2>nul
if not errorlevel 1 (
    echo    ✅ Greenlet instalado com sucesso!
    goto :greenlet_ok
)

echo    ⚠️  Tentando versão específica do greenlet...
python -m pip install --only-binary :all: "greenlet>=3.0.0,<4.0.0" --quiet 2>nul
if not errorlevel 1 (
    echo    ✅ Greenlet instalado com sucesso!
    goto :greenlet_ok
)

echo    ⚠️  Tentando greenlet sem restrições de binary...
python -m pip install greenlet --no-build-isolation --quiet 2>nul
if not errorlevel 1 (
    echo    ✅ Greenlet instalado com sucesso!
    goto :greenlet_ok
)

echo    ⚠️  Tentando versão específica do greenlet (3.0.3)...
python -m pip install --only-binary :all: greenlet==3.0.3 --quiet 2>nul
if not errorlevel 1 (
    echo    ✅ Greenlet instalado com sucesso!
    goto :greenlet_ok
)

REM Se chegou aqui, greenlet falhou
echo    ❌ Não foi possível instalar greenlet automaticamente
echo.
echo    💡 SOLUÇÃO PARA PYTHON %PYTHON_VERSION%:
echo.
echo    Opção A - USAR PYTHON 3.11 ou 3.12 (RECOMENDADO):
echo       1. Desinstale Python %PYTHON_VERSION%
echo       2. Baixe Python 3.11 ou 3.12 de: https://www.python.org/downloads/
echo       3. Durante instalação, marque "Add Python to PATH"
echo       4. Execute este script novamente
echo.
echo    Opção B - INSTALAR VISUAL C++ BUILD TOOLS:
echo       1. Baixe: https://visualstudio.microsoft.com/visual-cpp-build-tools/
echo       2. Instale "C++ build tools"
echo       3. Reinicie o computador
echo       4. Execute este script novamente
echo.
echo    Opção C - INSTALAÇÃO MANUAL DO GREENLET:
echo       python -m pip install --upgrade pip setuptools wheel
echo       python -m pip install --only-binary :all: greenlet
echo       Se falhar, tente: python -m pip install greenlet
echo.
pause
exit /b 1

:greenlet_ok

REM Estratégia 3: Tenta instalar normalmente (com wheels pré-compilados)
echo 🔍 Tentativa 2: Instalando outras dependências com wheels pré-compilados...
python -m pip install --only-binary :all: -r requirements.txt --quiet 2>nul
if not errorlevel 1 (
    echo ✅ Dependências instaladas com sucesso!
    goto :instalar_playwright
)

REM Estratégia 4: Tenta instalar sem restrições (permite compilação)
echo 🔍 Tentativa 3: Instalando dependências (pode precisar compilar)...
python -m pip install -r requirements.txt --quiet 2>nul
if not errorlevel 1 (
    echo ✅ Dependências instaladas com sucesso!
    goto :instalar_playwright
)

REM Se chegou aqui, houve erro
echo.
echo ⚠️  Erro ao instalar algumas dependências
echo.
echo 🔧 TENTANDO SOLUÇÃO AUTOMÁTICA...
echo.

REM Estratégia 5: Instala cada dependência individualmente (greenlet já foi instalado)
echo 🔍 Tentativa 4: Instalando dependências uma por uma...
python -m pip install playwright==1.40.0 --quiet
python -m pip install beautifulsoup4==4.12.2 --quiet
python -m pip install requests==2.31.0 --quiet
python -m pip install python-dotenv==1.0.0 --quiet
python -m pip install flask==3.0.0 --quiet

REM Verifica se pelo menos as principais foram instaladas
python -c "import playwright; import flask; print('OK')" >nul 2>&1
if not errorlevel 1 (
    echo ✅ Dependências principais instaladas!
    goto :instalar_playwright
)

REM Se ainda falhou, mostra instruções detalhadas
echo.
echo ==========================================
echo ❌ ERRO: Falha na instalação
echo ==========================================
echo.
echo O problema é que algumas dependências precisam ser COMPILADAS
echo e isso requer o Microsoft Visual C++ Build Tools.
echo.
echo 💡 SOLUÇÃO AUTOMÁTICA:
echo.
echo Opção 1 - INSTALAR VISUAL C++ BUILD TOOLS (Recomendado):
echo    1. Abra este link no navegador:
echo       https://visualstudio.microsoft.com/visual-cpp-build-tools/
echo    2. Baixe e instale "Microsoft C++ Build Tools"
echo    3. Execute este script novamente
echo.
echo Opção 2 - USAR PYTHON 3.11 ou 3.12 (RECOMENDADO para evitar problemas):
echo    Python %PYTHON_VERSION% é muito recente e pode não ter wheels para todas as dependências.
echo    1. Desinstale Python %PYTHON_VERSION%
echo    2. Baixe Python 3.11 ou 3.12 de:
echo       https://www.python.org/downloads/
echo    3. Durante a instalação, marque TODAS as opções:
echo       - Add Python to PATH
echo       - Install for all users (se possível)
echo    4. Execute este script novamente
echo    (Python 3.11 e 3.12 têm melhor suporte para wheels pré-compilados)
echo.
echo Opção 3 - INSTALAÇÃO MANUAL COM GREENLET (Avançado):
echo    python -m pip install --upgrade pip setuptools wheel
echo    python -m pip install --only-binary :all: greenlet
echo    python -m pip install playwright beautifulsoup4 requests python-dotenv flask
echo.
echo Opção 4 - INSTALAR VISUAL C++ BUILD TOOLS (Mais confiável):
echo    1. Baixe: https://visualstudio.microsoft.com/visual-cpp-build-tools/
echo    2. Instale "C++ build tools"
echo    3. Reinicie o computador
echo    4. Execute este script novamente
echo.
echo ==========================================
echo.
echo Pressione qualquer tecla para tentar continuar mesmo assim...
pause >nul

REM Tenta instalar Playwright mesmo assim
:instalar_playwright
echo.
echo 🌐 Instalando navegador Chromium...
python -m playwright install chromium --quiet

if errorlevel 1 (
    echo ⚠️  Aviso: Erro ao instalar Chromium
    echo 💡 Tente executar manualmente depois:
    echo    python -m playwright install chromium
) else (
    echo ✅ Navegador instalado
)

echo.

REM Verifica se arquivo .env existe
if not exist .env (
    echo 📝 Criando arquivo de configuração...
    if exist env.example (
        copy env.example .env >nul
        echo ✅ Arquivo .env criado
    )
    echo.
)

REM Verificação final
echo 🔍 Verificando instalação...
python -c "import playwright; import flask; print('✅ Tudo OK!')" 2>nul
if errorlevel 1 (
    echo ⚠️  Algumas dependências podem não estar instaladas corretamente
    echo 💡 Tente executar manualmente:
    echo    python -m pip install -r requirements.txt
    echo.
) else (
    echo.
    echo ==========================================
    echo ✨ Instalação concluída!
    echo ==========================================
    echo.
)

echo 📖 Como usar:
echo.
echo 1. Interface Web (Recomendado):
echo    Duplo clique em: executar_web.bat
echo    Ou execute: python gui_migrador_web.py
echo    Depois acesse: http://localhost:5000
echo.
echo 2. Linha de Comando:
echo    python migrador_pep.py ^<protocolo^> ^<caminho_pasta^>
echo.
echo.
pause

