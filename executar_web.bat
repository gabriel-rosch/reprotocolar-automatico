@echo off
REM Script para executar a interface web no Windows
REM Duplo clique neste arquivo para iniciar

echo ==========================================
echo 🚀 Iniciando Migrador PEP - Interface Web
echo ==========================================
echo.
echo 📱 A interface será aberta em: http://localhost:5000
echo.
echo ⚠️  Mantenha esta janela aberta enquanto usar o sistema
echo.
echo Para fechar, pressione Ctrl+C ou feche esta janela
echo.

python gui_migrador_web.py

if errorlevel 1 (
    echo.
    echo ❌ Erro ao iniciar!
    echo 💡 Verifique se a instalação foi concluída:
    echo    Execute: instalar.bat
    echo.
    pause
)

