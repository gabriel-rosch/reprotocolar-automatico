# 📋 Formatos de Entrada - Migrador PEP

## 🔤 Formato 1: Linha de Comando (CLI)

### Sintaxe:
```bash
python3 migrador_pep.py <protocolo> <caminho_completo_pasta>
```

### Exemplo:
```bash
python3 migrador_pep.py 664276 /Users/gabrielrosch/git/ATPS-23-LGS-012
```

### Onde:
- **664276** = Protocolo (número)
- **/Users/gabrielrosch/git/ATPS-23-LGS-012** = Caminho completo da pasta (incluindo diretório base)

### Vantagens:
- ✅ Execução direta e rápida
- ✅ Ideal para automação/scripts
- ✅ Um protocolo por vez

---

## 📝 Formato 2: Lista na GUI (Interface Gráfica)

### Sintaxe:
```
PROTOCOLO [TAB] NOME_PASTA
```

### Exemplo:
```
701524	ATPS-23-LGS-051
701528	ATPS-23-LGS-052
701532	ATPS-23-LGS-054
```

### Onde:
- **701524** = Protocolo (número)
- **ATPS-23-LGS-051** = Nome da pasta (sem caminho completo)
- O diretório base é configurado separadamente na interface

### Vantagens:
- ✅ Múltiplos protocolos de uma vez
- ✅ Interface visual
- ✅ Acompanhamento de progresso
- ✅ Reimportação individual

---

## 🔄 Como Converter Entre Formatos

### De Lista GUI → Linha de Comando:

**Lista GUI:**
```
701524	ATPS-23-LGS-051
```

**Comando equivalente:**
```bash
python3 migrador_pep.py 701524 /Users/gabrielrosch/git/ATPS-23-LGS-051
```

**Fórmula:**
```bash
python3 migrador_pep.py <PROTOCOLO> <DIRETORIO_BASE>/<NOME_PASTA>
```

### De Linha de Comando → Lista GUI:

**Comando:**
```bash
python3 migrador_pep.py 664276 /Users/gabrielrosch/git/ATPS-23-LGS-012
```

**Lista GUI equivalente:**
```
664276	ATPS-23-LGS-012
```

**E configure o diretório base na GUI como:** `/Users/gabrielrosch/git/`

---

## 📊 Comparação

| Aspecto | Linha de Comando | Interface GUI |
|---------|------------------|--------------|
| **Formato** | `protocolo caminho_completo` | `protocolo [TAB] nome_pasta` |
| **Quantidade** | 1 por vez | Múltiplos |
| **Diretório Base** | Incluído no caminho | Configurado separadamente |
| **Exemplo** | `664276 /Users/gabrielrosch/git/ATPS-23-LGS-012` | `664276	ATPS-23-LGS-012` |
| **Uso** | Scripts, automação | Migração em lote |

---

## 💡 Exemplos Práticos

### Exemplo 1: Linha de Comando
```bash
# Protocolo 664276, pasta ATPS-23-LGS-012
python3 migrador_pep.py 664276 /Users/gabrielrosch/git/ATPS-23-LGS-012
```

### Exemplo 2: Lista GUI
```
# Configure diretório base: /Users/gabrielrosch/git/
# Cole a lista:
664276	ATPS-23-LGS-012
701524	ATPS-23-LGS-051
701528	ATPS-23-LGS-052
```

### Exemplo 3: Converter Lista para Script Bash

Se você tem uma lista no formato GUI e quer executar via linha de comando:

```bash
# Lista original (formato GUI):
# 701524	ATPS-23-LGS-051
# 701528	ATPS-23-LGS-052

# Script bash equivalente:
DIR_BASE="/Users/gabrielrosch/git/"
python3 migrador_pep.py 701524 "${DIR_BASE}ATPS-23-LGS-051"
python3 migrador_pep.py 701528 "${DIR_BASE}ATPS-23-LGS-052"
```

---

## ⚠️ Importante

1. **Linha de Comando:** Sempre use o caminho completo da pasta
2. **GUI:** Use apenas o nome da pasta (o diretório base é configurado separadamente)
3. **TAB vs Espaços:** Na GUI, pode usar TAB ou espaços múltiplos para separar
4. **Caminhos:** Use caminhos absolutos ou relativos completos na linha de comando

