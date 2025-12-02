#!/bin/bash
# Script de instalação do Migrador PEP
# Para usuários não técnicos

echo "=========================================="
echo "🔧 Instalador do Migrador PEP"
echo "=========================================="
echo ""

# Verifica se Python 3 está instalado
echo "📋 Verificando Python 3..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    echo "💡 Por favor, instale Python 3 primeiro:"
    echo "   macOS: brew install python3"
    echo "   Ou baixe em: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ $PYTHON_VERSION encontrado"
echo ""

# Verifica se pip está instalado
echo "📦 Verificando pip..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não encontrado!"
    echo "💡 Instalando pip..."
    python3 -m ensurepip --upgrade
fi

echo "✅ pip encontrado"
echo ""

# Instala dependências
echo "📥 Instalando dependências..."
python3 -m pip install --upgrade pip --quiet
python3 -m pip install -r requirements.txt --quiet

if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências"
    echo "💡 Tente executar manualmente:"
    echo "   python3 -m pip install -r requirements.txt"
    exit 1
fi

echo "✅ Dependências instaladas"
echo ""

# Instala navegadores do Playwright
echo "🌐 Instalando navegador Chromium..."
python3 -m playwright install chromium --quiet

if [ $? -ne 0 ]; then
    echo "⚠️  Aviso: Erro ao instalar Chromium"
    echo "💡 Tente executar manualmente:"
    echo "   python3 -m playwright install chromium"
fi

echo "✅ Navegador instalado"
echo ""

# Verifica se arquivo .env existe
if [ ! -f .env ]; then
    echo "📝 Criando arquivo de configuração..."
    if [ -f env.example ]; then
        cp env.example .env
        echo "✅ Arquivo .env criado a partir de env.example"
        echo "💡 Edite o arquivo .env se necessário"
    else
        echo "⚠️  Arquivo env.example não encontrado"
    fi
    echo ""
fi

echo "=========================================="
echo "✨ Instalação concluída!"
echo "=========================================="
echo ""
echo "📖 Como usar:"
echo ""
echo "1. Interface Web (Recomendado):"
echo "   python3 gui_migrador_web.py"
echo "   Depois acesse: http://localhost:5000"
echo ""
echo "2. Linha de Comando:"
echo "   python3 migrador_pep.py <protocolo> <caminho_pasta>"
echo ""
echo "3. Interface Gráfica (se disponível):"
echo "   python3 gui_migrador.py"
echo ""
echo "📚 Para mais informações, consulte o README.md"
echo ""

