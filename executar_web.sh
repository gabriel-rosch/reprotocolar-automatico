#!/bin/bash
# Script para executar a interface web no macOS/Linux
# Duplo clique ou execute: ./executar_web.sh

echo "=========================================="
echo "🚀 Iniciando Migrador PEP - Interface Web"
echo "=========================================="
echo ""
echo "📱 A interface será aberta em: http://localhost:5000"
echo ""
echo "⚠️  Mantenha esta janela aberta enquanto usar o sistema"
echo ""
echo "Para fechar, pressione Ctrl+C ou feche esta janela"
echo ""

python3 gui_migrador_web.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Erro ao iniciar!"
    echo "💡 Verifique se a instalação foi concluída:"
    echo "   Execute: ./instalar.sh"
    echo ""
    read -p "Pressione Enter para sair..."
fi

