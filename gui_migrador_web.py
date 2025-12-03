"""
Interface web para migração de formulários PEP
Alternativa para quando tkinter não funciona
"""
from flask import Flask, render_template_string, request, jsonify
import threading
import os
import json
from datetime import datetime
import asyncio
import concurrent.futures
from migrador_pep import MigradorPEP

app = Flask(__name__)

# Estado global
itens_migracao = {}
configuracao = {
    'diretorio_base': '/Users/gabrielrosch/git/'
}

# Template HTML
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Migrador PEP - Sistema de Migração</title>
    <meta charset="utf-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 30px;
        }
        h1 {
            color: #333;
            margin-bottom: 30px;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }
        .section {
            margin-bottom: 30px;
            padding: 20px;
            background: #fafafa;
            border-radius: 6px;
            border: 1px solid #e0e0e0;
        }
        .section h2 {
            color: #555;
            margin-bottom: 15px;
            font-size: 18px;
        }
        input[type="text"], textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
            font-family: monospace;
        }
        textarea {
            min-height: 150px;
            resize: vertical;
        }
        button {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            margin-right: 10px;
            margin-top: 10px;
        }
        button:hover {
            background: #45a049;
        }
        button.secondary {
            background: #2196F3;
        }
        button.secondary:hover {
            background: #0b7dda;
        }
        button.danger {
            background: #f44336;
        }
        button.danger:hover {
            background: #da190b;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
            background: white;
            color: #333;
        }
        th {
            background: #2c3e50;
            color: white;
            font-weight: 600;
        }
        tr:nth-child(even) {
            background: #f8f9fa;
        }
        tr:hover {
            background: #e3f2fd;
        }
        td {
            color: #212529;
        }
        .status-pendente { color: #999; }
        .status-executando { color: #2196F3; font-weight: bold; }
        .status-concluido { color: #4CAF50; font-weight: bold; }
        .status-erro { color: #f44336; font-weight: bold; }
        .progress-bar {
            width: 100%;
            height: 20px;
            background: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background: #4CAF50;
            transition: width 0.3s;
        }
        .message {
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
        }
        .message.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .message.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔄 Migrador PEP - Sistema de Migração</h1>
        
        <div class="section">
            <h2>⚙️ Configurações</h2>
            <label>Diretório Base:</label>
            <input type="text" id="diretorio_base" value="{{ diretorio_base }}" style="margin-top: 5px;">
        </div>
        
        <div class="section">
            <h2>📋 Lista de Protocolos e Pastas</h2>
            <p style="margin-bottom: 10px; color: #666;">
                Formato: PROTOCOLO [TAB] NOME_PASTA (um por linha)<br>
                Exemplo: 701524	ATPS-23-LGS-051
            </p>
            <textarea id="lista_protocolos" placeholder="Cole aqui a lista de protocolos e pastas..."></textarea>
            <div>
                <button onclick="validarLista()">✓ Validar</button>
                <button onclick="limparLista()" class="secondary">🗑️ Limpar</button>
                <button onclick="iniciarMigracao()" style="background: #FF9800;">🚀 Iniciar Migração</button>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 Progresso das Migrações</h2>
            <div id="tabela_progresso">
                <p style="color: #999;">Nenhuma migração iniciada ainda.</p>
            </div>
        </div>
    </div>
    
    <script>
        let intervaloAtualizacao = null;
        
        function validarLista() {
            const texto = document.getElementById('lista_protocolos').value.trim();
            if (!texto) {
                alert('A lista está vazia!');
                return;
            }
            
            const linhas = texto.split('\\n');
            let validos = 0;
            let invalidos = [];
            
            linhas.forEach((linha, idx) => {
                linha = linha.trim();
                if (!linha) return;
                
                // Aceita TAB, dois espaços ou múltiplos espaços
                let partes;
                if (linha.includes('\\t')) {
                    partes = linha.split('\\t');
                } else if (linha.includes('  ')) {
                    partes = linha.split('  ');
                } else {
                    // Tenta separar por espaços múltiplos usando regex
                    partes = linha.split(/\\s{2,}/);
                }
                if (partes.length >= 2 && partes[0].trim() && partes[1].trim()) {
                    validos++;
                } else {
                    invalidos.push(`Linha ${idx + 1}: ${linha}`);
                }
            });
            
            let mensagem = `Validação concluída!\\n\\n✓ Válidos: ${validos}`;
            if (invalidos.length > 0) {
                mensagem += `\\n✗ Inválidos: ${invalidos.length}`;
                if (invalidos.length <= 10) {
                    mensagem += '\\n\\n' + invalidos.join('\\n');
                } else {
                    mensagem += `\\n\\n${invalidos.slice(0, 10).join('\\n')}\\n... e mais ${invalidos.length - 10}`;
                }
            }
            alert(mensagem);
        }
        
        function limparLista() {
            document.getElementById('lista_protocolos').value = '';
        }
        
        function iniciarMigracao() {
            const diretorio = document.getElementById('diretorio_base').value;
            const lista = document.getElementById('lista_protocolos').value;
            
            fetch('/iniciar', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({diretorio_base: diretorio, lista: lista})
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    alert(`Migração iniciada para ${data.count} item(ns)!`);
                    atualizarProgresso();
                    if (!intervaloAtualizacao) {
                        intervaloAtualizacao = setInterval(atualizarProgresso, 2000);
                    }
                } else {
                    alert('Erro: ' + data.error);
                }
            });
        }
        
        function atualizarProgresso() {
            fetch('/status')
            .then(r => r.json())
            .then(data => {
                const div = document.getElementById('tabela_progresso');
                if (data.itens && data.itens.length > 0) {
                    let html = '<table><thead><tr><th>Protocolo</th><th>Pasta</th><th>Status</th><th>Progresso</th><th>Login</th><th>Extração</th><th>Preenchimento</th><th>Anexos</th><th>Mensagem</th></tr></thead><tbody>';
                    data.itens.forEach(item => {
                        const statusClass = `status-${item.status.toLowerCase().replace(' ', '-')}`;
                        html += `<tr>
                            <td>${item.protocolo}</td>
                            <td>${item.nome_pasta}</td>
                            <td class="${statusClass}">${item.status}</td>
                            <td>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: ${item.progresso}%"></div>
                                </div>
                                ${item.progresso}%
                            </td>
                            <td>${item.steps.Login || '⏳'}</td>
                            <td>${item.steps.Extração || '⏳'}</td>
                            <td>${item.steps.Preenchimento || '⏳'}</td>
                            <td>${item.steps.Anexos || '⏳'}</td>
                            <td>${item.mensagem || ''}</td>
                        </tr>`;
                    });
                    html += '</tbody></table>';
                    div.innerHTML = html;
                } else {
                    div.innerHTML = '<p style="color: #999;">Nenhuma migração iniciada ainda.</p>';
                }
            });
        }
        
        // Atualiza a cada 2 segundos se houver migrações
        setInterval(() => {
            if (intervaloAtualizacao) {
                atualizarProgresso();
            }
        }, 2000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, diretorio_base=configuracao['diretorio_base'])

@app.route('/iniciar', methods=['POST'])
def iniciar():
    try:
        data = request.json
        diretorio_base = data.get('diretorio_base', '/Users/gabrielrosch/git/')
        lista_texto = data.get('lista', '')
        
        # Parseia lista
        linhas = lista_texto.strip().split('\n')
        itens = []
        for linha in linhas:
            linha = linha.strip()
            if not linha:
                continue
            # Aceita TAB, dois espaços ou múltiplos espaços
            if '\t' in linha:
                partes = linha.split('\t')
            elif '  ' in linha:  # Dois ou mais espaços
                partes = linha.split('  ')
            else:
                # Tenta separar por espaços múltiplos
                import re
                partes = re.split(r'\s{2,}', linha)
            
            if len(partes) >= 2:
                protocolo = partes[0].strip()
                nome_pasta = partes[1].strip()
                if protocolo and nome_pasta:
                    caminho_pasta = os.path.join(diretorio_base, nome_pasta)
                    
                    # Valida se a pasta existe
                    if not os.path.exists(caminho_pasta):
                        return jsonify({
                            'success': False, 
                            'error': f'Pasta não encontrada: {caminho_pasta}\nProtocolo: {protocolo}'
                        })
                    
                    itens.append({
                        'protocolo': protocolo,
                        'nome_pasta': nome_pasta,
                        'caminho_pasta': caminho_pasta,
                        'status': 'Pendente',
                        'progresso': 0,
                        'mensagem': '',
                        'steps': {
                            'Login': '⏳',
                            'Extração': '⏳',
                            'Preenchimento': '⏳',
                            'Anexos': '⏳'
                        }
                    })
        
        if not itens:
            return jsonify({'success': False, 'error': 'Nenhum item válido encontrado'})
        
        # Salva configuração
        configuracao['diretorio_base'] = diretorio_base
        
        # Limpa itens anteriores
        itens_migracao.clear()
        
        # Adiciona novos itens
        for item in itens:
            itens_migracao[item['protocolo']] = item
        
        # Inicia migrações em thread
        threading.Thread(target=executar_migracoes, daemon=True).start()
        
        return jsonify({'success': True, 'count': len(itens)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/status')
def status():
    return jsonify({
        'itens': list(itens_migracao.values())
    })

def executar_migracao_item(protocolo, item):
    """Executa uma migração individual"""
    if item['status'] != 'Pendente':
        return
    
    item['status'] = 'Executando'
    
    def callback_progresso(step, status, mensagem=""):
        if step in item['steps']:
            item['steps'][step] = status
        item['mensagem'] = mensagem
        if step == "Login":
            item['progresso'] = 20
        elif step == "Extração":
            item['progresso'] = 40
        elif step == "Preenchimento":
            item['progresso'] = 70
        elif step == "Anexos":
            item['progresso'] = 90
    
    try:
        migrador = MigradorPEP(
            item['protocolo'],
            item['caminho_pasta'],
            callback_progresso=callback_progresso,
            manter_navegador_aberto=True  # Mantém navegador aberto para verificação manual
        )
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(migrador.executar_migracao())
            item['status'] = 'Concluído'
            item['progresso'] = 100
            item['mensagem'] = 'Migração concluída! Navegador aberto para verificação manual.'
        except Exception as e:
            item['status'] = 'Erro'
            item['mensagem'] = f'Erro: {str(e)}'
        finally:
            loop.close()
    except Exception as e:
        item['status'] = 'Erro'
        item['mensagem'] = f'Erro crítico: {str(e)}'

def executar_migracoes():
    """Executa as migrações em paralelo"""
    
    # Filtra apenas itens pendentes
    itens_pendentes = [
        (protocolo, item) 
        for protocolo, item in itens_migracao.items() 
        if item['status'] == 'Pendente'
    ]
    
    if not itens_pendentes:
        return
    
    # Executa até 20 migrações em paralelo (aumentado para processar grandes lotes rapidamente)
    # Limite alto para permitir processar muitos itens ao mesmo tempo
    max_workers = min(20, len(itens_pendentes))
    
    print(f"🚀 Iniciando {len(itens_pendentes)} migração(ões) com até {max_workers} em paralelo...")
    
    # Usa ThreadPoolExecutor para executar em paralelo
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submete todas as migrações
        futures = {
            executor.submit(executar_migracao_item, protocolo, item): (protocolo, item)
            for protocolo, item in itens_pendentes
        }
        
        # Aguarda todas completarem
        for future in concurrent.futures.as_completed(futures):
            protocolo, item = futures[future]
            try:
                future.result()  # Verifica se houve exceção
            except Exception as e:
                item['status'] = 'Erro'
                item['mensagem'] = f'Erro na execução: {str(e)}'

def obter_ip_local():
    """Obtém o IP local da máquina"""
    import socket
    try:
        # Conecta a um servidor externo para descobrir o IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"

def encontrar_porta_disponivel(porta_inicial=5000, max_tentativas=10):
    """Encontra uma porta disponível começando da porta inicial"""
    import socket
    for i in range(max_tentativas):
        porta = porta_inicial + i
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', porta))
                return porta
        except OSError:
            continue
    return None

def obter_porta_dos_argumentos():
    """Extrai a porta dos argumentos da linha de comando"""
    import sys
    for i, arg in enumerate(sys.argv):
        if arg in ['--port', '-p'] and i + 1 < len(sys.argv):
            try:
                return int(sys.argv[i + 1])
            except ValueError:
                return None
        elif arg.startswith('--port='):
            try:
                return int(arg.split('=')[1])
            except ValueError:
                return None
    return None

if __name__ == '__main__':
    import sys
    
    # Verifica se deve rodar na rede local
    rodar_rede = '--rede' in sys.argv or '--network' in sys.argv
    
    # Tenta obter porta dos argumentos
    porta_customizada = obter_porta_dos_argumentos()
    porta_inicial = porta_customizada if porta_customizada else 5000
    
    # Encontra porta disponível
    porta = encontrar_porta_disponivel(porta_inicial)
    if not porta:
        print("❌ Erro: Não foi possível encontrar uma porta disponível!")
        print("💡 Tente fechar outros programas ou especificar uma porta:")
        print("   python3 gui_migrador_web.py --port 5001")
        sys.exit(1)
    
    if porta != porta_inicial:
        print(f"⚠️  Porta {porta_inicial} está em uso. Usando porta {porta}.")
        if porta_inicial == 5000:
            print("💡 No macOS, isso geralmente acontece por causa do AirPlay Receiver.")
            print("   Para desabilitar: Preferências do Sistema → Compartilhamento → AirPlay Receiver")
    
    if rodar_rede:
        ip_local = obter_ip_local()
        print("🌐 Iniciando interface web na rede local...")
        print(f"📱 Acesse localmente: http://localhost:{porta}")
        print(f"🌍 Acesse pela rede: http://{ip_local}:{porta}")
        print(f"\n💡 Outras pessoas na mesma rede podem acessar:")
        print(f"   http://{ip_local}:{porta}")
        print(f"\n⚠️  Certifique-se de que o firewall permite conexões na porta {porta}")
        try:
            app.run(debug=True, host='0.0.0.0', port=porta)
        except OSError as e:
            if "Address already in use" in str(e):
                print(f"\n❌ Erro: Porta {porta} ainda está em uso!")
                print("💡 Tente especificar outra porta:")
                print(f"   python3 gui_migrador_web.py --rede --port {porta + 1}")
            else:
                raise
    else:
        print("🌐 Iniciando interface web (apenas local)...")
        print(f"📱 Acesse: http://localhost:{porta}")
        print("💡 Para permitir acesso na rede, execute com: --rede")
        try:
            app.run(debug=True, port=porta)
        except OSError as e:
            if "Address already in use" in str(e):
                print(f"\n❌ Erro: Porta {porta} ainda está em uso!")
                print("💡 Tente especificar outra porta:")
                print(f"   python3 gui_migrador_web.py --port {porta + 1}")
            else:
                raise

