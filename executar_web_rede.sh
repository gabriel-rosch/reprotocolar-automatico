#!/bin/bash
# Script para executar a interface web na rede local (macOS/Linux)
# Permite que outras pessoas na mesma rede acessem o sistema

echo "=========================================="
echo "🌐 Iniciando Migrador PEP - Modo Rede"
echo "=========================================="
echo ""
echo "📱 A interface será acessível na rede local"
echo ""
echo "⚠️  IMPORTANTE:"
echo "   - Se a porta 5000 estiver em uso, será usada outra porta automaticamente"
echo "   - Certifique-se de que o firewall permite conexões na porta usada"
echo "   - Outras pessoas precisam estar na mesma rede Wi-Fi/Ethernet"
echo "   - Mantenha esta janela aberta enquanto usar o sistema"
echo ""
echo "💡 Se a porta 5000 estiver em uso (AirPlay no macOS):"
echo "   - O sistema tentará usar outra porta automaticamente"
echo "   - Ou desabilite AirPlay: Preferências → Compartilhamento → AirPlay Receiver"
echo ""
echo "Para fechar, pressione Ctrl+C ou feche esta janela"
echo ""

python3 gui_migrador_web.py --rede

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Erro ao iniciar!"
    echo "💡 Verifique se a instalação foi concluída:"
    echo "   Execute: ./instalar.sh"
    echo ""
    read -p "Pressione Enter para sair..."
fi

