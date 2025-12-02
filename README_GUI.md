# 🖥️ Interface Gráfica - Migrador PEP

Interface gráfica moderna para gerenciar múltiplas migrações de formulários PEP de forma simultânea.

## 🚀 Como Usar

### 1. Iniciar a Interface

```bash
python3 gui_migrador.py
```

### 2. Configurar Diretório Base

1. No campo **"Diretório Base"**, informe o caminho onde estão as pastas com os arquivos
   - Exemplo: `/Users/gabrielrosch/git/`
   - Ou clique em **"📁 Buscar"** para selecionar o diretório

### 3. Adicionar Lista de Protocolos

Na área de texto **"Lista de Protocolos e Pastas"**, cole ou digite a lista no formato:

```
701524	ATPS-23-LGS-051
701528	ATPS-23-LGS-052
701532	ATPS-23-LGS-054
```

**Formato:**
- `PROTOCOLO [TAB] NOME_PASTA` (um por linha)
- Ou `PROTOCOLO  NOME_PASTA` (com espaços múltiplos)

**Dicas:**
- Você pode copiar e colar diretamente do Excel/Google Sheets
- Use o botão **"✓ Validar"** para verificar se o formato está correto
- Use **"🗑️ Limpar"** para limpar a lista

### 4. Iniciar Migração

1. Clique em **"🚀 Iniciar Migração"**
2. Confirme a quantidade de itens
3. Cada item abrirá 2 abas no navegador:
   - **Aba 1:** Formulário antigo (somente leitura)
   - **Aba 2:** Formulário novo (preenchido automaticamente)

### 5. Acompanhar Progresso

A tabela mostra o progresso de cada migração:

| Coluna | Descrição |
|--------|-----------|
| **Protocolo** | Número do protocolo |
| **Pasta** | Nome da pasta |
| **Status** | Estado atual (Pendente, Executando, Concluído, Erro) |
| **Progresso** | Porcentagem de conclusão |
| **Login** | Status do login (⏳, 🔄, ✅, ❌) |
| **Extração** | Status da extração de dados |
| **Preenchimento** | Status do preenchimento |
| **Anexos** | Status do upload de anexos |
| **Mensagem** | Mensagens de status/erro |

### 6. Menu de Contexto

Clique com o botão direito em um item da lista para:

- **🔄 Reimportar:** Executa novamente um item que teve erro
- **📂 Abrir Pasta:** Abre a pasta do item no Finder
- **❌ Remover:** Remove o item da lista

## 📋 Funcionalidades

### ✅ Validação de Lista
- Valida o formato antes de iniciar
- Mostra quantos itens são válidos/inválidos
- Lista linhas com problemas

### 📊 Acompanhamento em Tempo Real
- Atualização automática do progresso
- Status de cada etapa (Login, Extração, Preenchimento, Anexos)
- Mensagens de erro detalhadas

### 🔄 Reimportação
- Reimporta apenas itens com erro
- Mantém histórico na lista
- Não precisa reiniciar tudo

### 💾 Configurações Salvas
- Salva o diretório base automaticamente
- Restaura na próxima execução

## ⚠️ Importante

1. **Navegador:** Cada migração abre 2 abas no navegador. Não feche manualmente!
2. **Revisão:** Sempre revise os formulários antes de submeter
3. **Erros:** Itens com erro podem ser reimportados individualmente
4. **Performance:** As migrações são executadas sequencialmente para evitar sobrecarga

## 🐛 Solução de Problemas

### Interface não abre
```bash
# Verifique se tkinter está instalado
python3 -c "import tkinter; print('OK')"
```

### Erro ao executar migração
- Verifique se o diretório base está correto
- Verifique se as pastas existem
- Veja a mensagem de erro na coluna "Mensagem"

### Navegador não abre
- Verifique se o Playwright está instalado: `playwright install chromium`
- Verifique as credenciais no arquivo `.env`

## 📝 Exemplo de Uso

1. Abra a interface: `python3 gui_migrador.py`
2. Configure diretório: `/Users/gabrielrosch/git/`
3. Cole a lista:
   ```
   701524	ATPS-23-LGS-051
   701528	ATPS-23-LGS-052
   ```
4. Clique em "🚀 Iniciar Migração"
5. Acompanhe o progresso na tabela
6. Revise os formulários nas abas do navegador

## 🎯 Próximos Passos

Após a migração:
1. Revise cada formulário nas abas abertas
2. Verifique se todos os dados foram preenchidos corretamente
3. Verifique se os anexos foram anexados
4. Submeta manualmente quando estiver tudo OK

