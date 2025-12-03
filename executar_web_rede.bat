@echo off
REM Script para executar a interface web na rede local (Windows)
REM Permite que outras pessoas na mesma rede acessem o sistema

echo ==========================================
echo 🌐 Iniciando Migrador PEP - Modo Rede
echo ==========================================
echo.
echo 📱 A interface será acessível na rede local
echo.
echo ⚠️  IMPORTANTE:
echo    - Se a porta 5000 estiver em uso, será usada outra porta automaticamente
echo    - Certifique-se de que o firewall permite conexões na porta usada
echo    - Outras pessoas precisam estar na mesma rede Wi-Fi/Ethernet
echo    - Mantenha esta janela aberta enquanto usar o sistema
echo.
echo Para fechar, pressione Ctrl+C ou feche esta janela
echo.

python gui_migrador_web.py --rede

if errorlevel 1 (
    echo.
    echo ❌ Erro ao iniciar!
    echo 💡 Verifique se a instalação foi concluída:
    echo    Execute: instalar.bat
    echo.
    pause
)

