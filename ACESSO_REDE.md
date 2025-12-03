# 🌐 Como Executar na Rede Local

Este guia explica como executar o sistema na rede local para que outras pessoas possam acessar e testar.

---

## 🚀 Modo Rápido

### macOS/Linux:
```bash
chmod +x executar_web_rede.sh
./executar_web_rede.sh
```

### Windows:
Duplo clique em: `executar_web_rede.bat`

---

## 📋 Passo a Passo

### 1️⃣ Execute o Sistema em Modo Rede

**macOS/Linux:**
```bash
python3 gui_migrador_web.py --rede
```

**Windows:**
```bash
python gui_migrador_web.py --rede
```

**Especificar porta customizada:**
```bash
python3 gui_migrador_web.py --rede --port 5001
```

### 2️⃣ Anote o IP e Porta que Aparecem

Quando você executar, verá algo assim:
```
🌐 Iniciando interface web na rede local...
📱 Acesse localmente: http://localhost:5000
🌍 Acesse pela rede: http://192.168.1.100:5000

💡 Outras pessoas na mesma rede podem acessar:
   http://192.168.1.100:5000
```

**Se a porta 5000 estiver em uso, verá:**
```
⚠️  Porta 5000 está em uso. Usando porta 5001.
💡 No macOS, isso geralmente acontece por causa do AirPlay Receiver.
   Para desabilitar: Preferências do Sistema → Compartilhamento → AirPlay Receiver
🌐 Iniciando interface web na rede local...
📱 Acesse localmente: http://localhost:5001
🌍 Acesse pela rede: http://192.168.1.100:5001
```

**Anote o IP e a PORTA que aparecem** (exemplo: `192.168.1.100:5001`)

### 3️⃣ Compartilhe o IP e Porta com Outras Pessoas

A pessoa que vai testar precisa:
1. Estar na **mesma rede Wi-Fi/Ethernet** que você
2. Abrir o navegador
3. Acessar: `http://[SEU_IP]:[PORTA]`
   - Exemplo: `http://192.168.1.100:5000` ou `http://192.168.1.100:5001`

---

## 🔒 Configurar Firewall

### macOS:

1. **Abra:** Preferências do Sistema → Segurança e Privacidade → Firewall
2. **Clique em:** "Opções do Firewall..."
3. **Adicione:** Python ou permita conexões de entrada na porta 5000

**Ou via Terminal:**
```bash
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/local/bin/python3
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblockapp /usr/local/bin/python3
```

### Windows:

1. **Abra:** Painel de Controle → Firewall do Windows
2. **Clique em:** "Permitir um aplicativo pelo Firewall"
3. **Adicione:** Python ou crie uma regra para a porta 5000

**Ou via PowerShell (como Administrador):**
```powershell
New-NetFirewallRule -DisplayName "Migrador PEP" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

### Linux:

```bash
# Ubuntu/Debian
sudo ufw allow 5000/tcp

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
```

---

## ✅ Verificar se Está Funcionando

### No Seu Computador:
1. Abra o navegador
2. Acesse: `http://localhost:5000`
3. Deve abrir a interface normalmente

### No Computador da Outra Pessoa:
1. Abra o navegador
2. Acesse: `http://[SEU_IP]:5000`
3. Deve abrir a mesma interface

**Se não abrir:**
- Verifique se ambos estão na mesma rede
- Verifique se o firewall está configurado
- Verifique se o IP está correto

---

## 🔍 Descobrir Seu IP Manualmente

### macOS/Linux:
```bash
# Método 1
ifconfig | grep "inet " | grep -v 127.0.0.1

# Método 2
ip addr show | grep "inet " | grep -v 127.0.0.1

# Método 3 (mais simples)
hostname -I
```

### Windows:
```bash
ipconfig
```
Procure por "Endereço IPv4" na seção da sua conexão Wi-Fi/Ethernet.

---

## ⚠️ Importante

### Segurança:
- ⚠️ **NÃO use em redes públicas** (cafés, aeroportos, etc.)
- ✅ Use apenas em **redes confiáveis** (casa, escritório)
- 🔒 O sistema roda em modo debug - **não use em produção**

### Limitações:
- Apenas pessoas na **mesma rede** podem acessar
- O sistema **para** quando você fechar a janela
- Não funciona pela internet (apenas rede local)

---

## 🐛 Problemas Comuns

### "Não consigo acessar de outro computador"

**Soluções:**
1. Verifique se ambos estão na mesma rede Wi-Fi
2. Verifique se o firewall está permitindo conexões
3. Tente desabilitar temporariamente o firewall para testar
4. Verifique se o IP está correto

### "O IP mudou"

**Solução:**
- O IP pode mudar se você desconectar/reconectar na rede
- Execute novamente e anote o novo IP

### "Porta 5000 já está em uso"

**Solução Automática:**
- O sistema agora tenta automaticamente outras portas (5001, 5002, etc.)
- A porta usada será mostrada na tela quando iniciar

**Solução Manual - macOS (AirPlay Receiver):**
1. Abra: **Preferências do Sistema** → **Compartilhamento**
2. Desmarque: **AirPlay Receiver**
3. Ou especifique outra porta:
   ```bash
   python3 gui_migrador_web.py --rede --port 5001
   ```

**Solução Manual - Windows/Linux:**
- Especifique outra porta:
  ```bash
  python gui_migrador_web.py --rede --port 5001
  ```
- Ou feche o programa que está usando a porta 5000

---

## 💡 Dicas

1. **Use um IP fixo** (configurar no roteador) para não precisar descobrir o IP toda vez
2. **Crie um atalho** no desktop para `executar_web_rede.sh` (ou `.bat`)
3. **Compartilhe este arquivo** com quem vai testar

---

## 📞 Precisa de Ajuda?

Se tiver problemas:
1. Verifique se Python está rodando: `python3 --version`
2. Verifique se a porta 5000 está livre
3. Tente acessar `http://localhost:5000` primeiro (deve funcionar)
4. Verifique as configurações do firewall

