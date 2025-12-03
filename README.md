# Migrador Automático de Formulários PEP CELESC

Projeto para migração automática de dados entre formulários web do sistema PEP CELESC.

## 📥 Como Baixar o Projeto

### Para Pessoas Não Técnicas:

1. **Acesse:** https://github.com/gabriel-rosch/reprotocolar-automatico
2. **Clique no botão verde "Code"** → **"Download ZIP"**
3. **Extraia o arquivo ZIP** na pasta desejada
4. **Leia o arquivo `LEIA-ME.txt`** para instruções rápidas
5. **Execute `instalar.sh`** (macOS/Linux) ou `instalar.bat` (Windows)

📖 **Guia completo:** Veja `COMO_BAIXAR.md` para instruções detalhadas.

## 🌐 Executar na Rede Local

Para permitir que outras pessoas na mesma rede acessem o sistema:

**macOS/Linux:**
```bash
./executar_web_rede.sh
```

**Windows:**
```bash
executar_web_rede.bat
```

📖 **Guia completo:** Veja `ACESSO_REDE.md` para instruções detalhadas sobre acesso na rede.

## 🚀 Tecnologias

- **Python 3.8+**
- **Playwright** - Automação de navegador
- **BeautifulSoup4** - Parsing HTML (opcional)
- **python-dotenv** - Gerenciamento de variáveis de ambiente

## 📦 Instalação

1. Clone o repositório ou navegue até a pasta do projeto

2. Instale as dependências:
```bash
python3 -m pip install -r requirements.txt
```

3. Instale os navegadores do Playwright:
```bash
python3 -m playwright install chromium
```

4. Configure as variáveis de ambiente:
```bash
cp env.example .env
```

Edite o arquivo `.env` se necessário (as credenciais já estão configuradas):
```
URL_LOGIN=https://pep.celesc.com.br/PEP/externo/login.xhtml
URL_BASE_FORMULARIO=https://pep.celesc.com.br/PEP/externo/ot/compartilhamentoPoste.xhtml
USUARIO=00793831903
SENHA=b$dEj@6L5#
DELAY_PREENCHIMENTO=500
HEADLESS=false
```

## 🎯 Como Usar

Execute o script do PEP passando o protocolo como parâmetro:
```bash
python3 migrador_pep.py <protocolo>
```

**Exemplo:**
```bash
python3 migrador_pep.py 876686
```

O script irá:
1. 🔐 Fazer login automaticamente no sistema PEP
2. 📥 Acessar o formulário antigo com o protocolo informado e extrair todos os dados
3. 🆕 Abrir uma nova aba com o formulário novo (sem protocolo)
4. 📝 Preencher automaticamente o novo formulário com os dados extraídos
5. 🔍 Manter ambas as abas abertas para você revisar e comparar antes de submeter

**⚠️ IMPORTANTE:** O script NÃO submete os formulários automaticamente. Você deve revisar manualmente e submeter quando estiver satisfeito.

## ⚙️ Configurações

- `URL_LOGIN`: URL da página de login do PEP
- `URL_BASE_FORMULARIO`: URL base do formulário (sem parâmetros)
- `USUARIO`: Usuário para login
- `SENHA`: Senha para login
- `DELAY_PREENCHIMENTO`: Delay em milissegundos entre cada campo (padrão: 500)
- `HEADLESS`: Se `true`, executa sem abrir o navegador (padrão: `false`)

## 📋 Parâmetros

O script `migrador_pep.py` recebe o protocolo como parâmetro:
- **Protocolo**: Número do protocolo (ex: 876686) que será usado para acessar o formulário antigo

## 🔧 Personalização

O script tenta mapear automaticamente os campos por:
1. Atributo `name`
2. Atributo `id`

Se os nomes dos campos forem diferentes entre os formulários, você pode editar o arquivo `migrador.py` para adicionar um mapeamento customizado.

## 📝 Exemplo de Mapeamento Customizado

Se precisar mapear campos com nomes diferentes, adicione um dicionário de mapeamento:

```python
MAPEAMENTO_CAMPOS = {
    'nome_antigo': 'nome_novo',
    'email_antigo': 'email_novo',
    # ... outros campos
}
```

## ⚠️ Notas Importantes

- O script não submete o formulário automaticamente - você precisa revisar e submeter manualmente
- Alguns sites podem ter proteção contra bots - pode ser necessário ajustar delays ou adicionar autenticação
- Campos com validação JavaScript podem precisar de tratamento especial

## 🐛 Troubleshooting

**Erro ao instalar Playwright:**
```bash
python3 -m playwright install --with-deps chromium
```

**No Windows, se tiver erro de Visual C++ Build Tools:**
- Execute: `instalar_windows_automatico.bat` (resolve automaticamente)
- Ou veja: `INSTALACAO_WINDOWS.md` para soluções detalhadas

**No macOS/Fish shell, use sempre `python3` ao invés de `python`:**

**No Windows, se tiver erro de Visual C++ Build Tools:**
- Execute: `instalar_windows_automatico.bat` (resolve automaticamente)
- Ou veja: `INSTALACAO_WINDOWS.md` para soluções detalhadas
```bash
# Instalar dependências
python3 -m pip install -r requirements.txt

# Instalar navegador
python3 -m playwright install chromium

# Executar script PEP
python3 migrador_pep.py 876686
```

**Campos não estão sendo preenchidos:**
- Verifique se os nomes/ids dos campos estão corretos
- Aumente o `DELAY_PREENCHIMENTO` se o site for lento
- Verifique se há JavaScript bloqueando o preenchimento

**Problemas com login:**
- O script tenta encontrar automaticamente os campos de login
- Se houver problemas, screenshots serão salvos em `debug_login.png` e `debug_pos_login.png`
- Verifique os screenshots para identificar os seletores corretos

**Campos não estão sendo encontrados:**
- O script tenta mapear campos por `name` e `id`
- Se os campos tiverem nomes diferentes, você pode editar `migrador_pep.py` para adicionar mapeamento customizado
- Screenshots de debug são salvos automaticamente quando há problemas

**Formulário não carrega:**
- Aumente o `DELAY_PREENCHIMENTO` no arquivo `.env`
- Verifique se o protocolo está correto
- Certifique-se de que está logado corretamente

