"""
Interface gráfica para migração de formulários PEP
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import json
from datetime import datetime
import asyncio
from migrador_pep import MigradorPEP


class MigracaoItem:
    """Representa um item de migração"""
    def __init__(self, protocolo, nome_pasta, diretorio_base):
        self.protocolo = protocolo
        self.nome_pasta = nome_pasta
        self.diretorio_base = diretorio_base
        self.caminho_pasta = os.path.join(diretorio_base, nome_pasta) if nome_pasta else None
        self.status = "Pendente"
        self.progresso = 0
        self.mensagem = ""
        self.erro = None
        self.thread = None
        self.browser_aberto = False
        self.steps = {
            "Login": "⏳",
            "Extração": "⏳",
            "Preenchimento": "⏳",
            "Anexos": "⏳",
            "Concluído": "⏳"
        }
        self.data_inicio = None
        self.data_fim = None


class GUIMigrador:
    def __init__(self, root):
        self.root = root
        self.root.title("Migrador PEP - Sistema de Migração Automática")
        self.root.geometry("1200x800")
        
        # Variáveis
        self.diretorio_base = tk.StringVar(value="/Users/gabrielrosch/git/")
        self.itens_migracao = []
        self.threads_ativas = {}
        
        # Configurar estilo
        self.setup_style()
        
        # Criar interface
        self.criar_interface()
        
        # Carregar configurações salvas
        self.carregar_configuracao()
    
    def setup_style(self):
        """Configura o estilo da interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Cores personalizadas
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Success.TLabel', foreground='green')
        style.configure('Error.TLabel', foreground='red')
        style.configure('Warning.TLabel', foreground='orange')
    
    def criar_interface(self):
        """Cria a interface gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = ttk.Label(main_frame, text="🔄 Migrador PEP - Sistema de Migração", style='Title.TLabel')
        title.pack(pady=(0, 20))
        
        # Frame de configuração
        config_frame = ttk.LabelFrame(main_frame, text="⚙️ Configurações", padding="10")
        config_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Diretório base
        dir_frame = ttk.Frame(config_frame)
        dir_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(dir_frame, text="Diretório Base:").pack(side=tk.LEFT, padx=(0, 10))
        dir_entry = ttk.Entry(dir_frame, textvariable=self.diretorio_base, width=60)
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        btn_buscar = ttk.Button(dir_frame, text="📁 Buscar", command=self.selecionar_diretorio)
        btn_buscar.pack(side=tk.LEFT)
        
        # Frame de lista de protocolos
        lista_frame = ttk.LabelFrame(main_frame, text="📋 Lista de Protocolos e Pastas", padding="10")
        lista_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Instruções
        instrucoes = ttk.Label(
            lista_frame, 
            text="Formato: PROTOCOLO [TAB] NOME_PASTA (um por linha)\nExemplo: 701524\tATPS-23-LGS-051",
            font=('Arial', 9)
        )
        instrucoes.pack(anchor=tk.W, pady=(0, 5))
        
        # Área de texto para colar lista
        self.texto_lista = scrolledtext.ScrolledText(lista_frame, height=8, wrap=tk.WORD)
        self.texto_lista.pack(fill=tk.BOTH, expand=True)
        
        # Botões de ação
        btn_frame = ttk.Frame(lista_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        btn_limpar = ttk.Button(btn_frame, text="🗑️ Limpar", command=self.limpar_lista)
        btn_limpar.pack(side=tk.LEFT, padx=(0, 10))
        
        btn_validar = ttk.Button(btn_frame, text="✓ Validar", command=self.validar_lista)
        btn_validar.pack(side=tk.LEFT, padx=(0, 10))
        
        btn_importar = ttk.Button(btn_frame, text="🚀 Iniciar Migração", command=self.iniciar_migracao)
        btn_importar.pack(side=tk.LEFT)
        
        # Frame de progresso (estilo uTorrent)
        progresso_frame = ttk.LabelFrame(main_frame, text="📊 Progresso das Migrações", padding="10")
        progresso_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview para lista de migrações
        self.criar_treeview(progresso_frame)
        
        # Barra de status
        self.status_bar = ttk.Label(main_frame, text="Pronto", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def criar_treeview(self, parent):
        """Cria a treeview estilo uTorrent"""
        # Frame para treeview e scrollbar
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Treeview
        columns = ('Protocolo', 'Pasta', 'Status', 'Progresso', 'Login', 'Extração', 'Preenchimento', 'Anexos', 'Mensagem')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Configurar colunas
        self.tree.heading('Protocolo', text='Protocolo')
        self.tree.heading('Pasta', text='Pasta')
        self.tree.heading('Status', text='Status')
        self.tree.heading('Progresso', text='Progresso')
        self.tree.heading('Login', text='Login')
        self.tree.heading('Extração', text='Extração')
        self.tree.heading('Preenchimento', text='Preenchimento')
        self.tree.heading('Anexos', text='Anexos')
        self.tree.heading('Mensagem', text='Mensagem')
        
        # Larguras das colunas
        self.tree.column('Protocolo', width=100)
        self.tree.column('Pasta', width=150)
        self.tree.column('Status', width=120)
        self.tree.column('Progresso', width=100)
        self.tree.column('Login', width=80)
        self.tree.column('Extração', width=80)
        self.tree.column('Preenchimento', width=120)
        self.tree.column('Anexos', width=80)
        self.tree.column('Mensagem', width=300)
        
        # Scrollbars
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        self.tree.config(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Menu de contexto
        self.criar_menu_contexto()
    
    def criar_menu_contexto(self):
        """Cria menu de contexto para itens da lista"""
        self.menu_contexto = tk.Menu(self.root, tearoff=0)
        self.menu_contexto.add_command(label="🔄 Reimportar", command=self.reimportar_selecionado)
        self.menu_contexto.add_command(label="📂 Abrir Pasta", command=self.abrir_pasta_selecionada)
        self.menu_contexto.add_separator()
        self.menu_contexto.add_command(label="❌ Remover", command=self.remover_selecionado)
        
        self.tree.bind("<Button-3>", self.mostrar_menu_contexto)
    
    def mostrar_menu_contexto(self, event):
        """Mostra menu de contexto"""
        item = self.tree.selection()[0] if self.tree.selection() else None
        if item:
            self.menu_contexto.post(event.x_root, event.y_root)
    
    def selecionar_diretorio(self):
        """Abre diálogo para selecionar diretório"""
        diretorio = filedialog.askdirectory(initialdir=self.diretorio_base.get())
        if diretorio:
            self.diretorio_base.set(diretorio)
            self.salvar_configuracao()
    
    def limpar_lista(self):
        """Limpa a área de texto"""
        self.texto_lista.delete(1.0, tk.END)
    
    def validar_lista(self):
        """Valida a lista de protocolos"""
        texto = self.texto_lista.get(1.0, tk.END).strip()
        if not texto:
            messagebox.showwarning("Aviso", "A lista está vazia!")
            return
        
        linhas = texto.split('\n')
        validos = []
        invalidos = []
        
        for idx, linha in enumerate(linhas, 1):
            linha = linha.strip()
            if not linha:
                continue
            
            # Tenta separar por TAB ou espaços múltiplos
            partes = linha.split('\t') if '\t' in linha else linha.split('  ')
            if len(partes) >= 2:
                protocolo = partes[0].strip()
                nome_pasta = partes[1].strip()
                if protocolo and nome_pasta:
                    validos.append((protocolo, nome_pasta))
                else:
                    invalidos.append(f"Linha {idx}: {linha}")
            else:
                invalidos.append(f"Linha {idx}: {linha}")
        
        mensagem = f"Validação concluída!\n\n"
        mensagem += f"✓ Válidos: {len(validos)}\n"
        if invalidos:
            mensagem += f"✗ Inválidos: {len(invalidos)}\n\n"
            mensagem += "Linhas inválidas:\n" + "\n".join(invalidos[:10])
            if len(invalidos) > 10:
                mensagem += f"\n... e mais {len(invalidos) - 10}"
        
        messagebox.showinfo("Validação", mensagem)
    
    def parsear_lista(self):
        """Parseia a lista de protocolos"""
        texto = self.texto_lista.get(1.0, tk.END).strip()
        if not texto:
            return []
        
        linhas = texto.split('\n')
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
                # Tenta separar por espaços múltiplos usando regex
                import re
                partes = re.split(r'\s{2,}', linha)
            
            if len(partes) >= 2:
                protocolo = partes[0].strip()
                nome_pasta = partes[1].strip()
                if protocolo and nome_pasta:
                    itens.append((protocolo, nome_pasta))
        
        return itens
    
    def iniciar_migracao(self):
        """Inicia o processo de migração"""
        # Valida diretório
        if not os.path.exists(self.diretorio_base.get()):
            messagebox.showerror("Erro", "Diretório base não encontrado!")
            return
        
        # Parseia lista
        itens = self.parsear_lista()
        if not itens:
            messagebox.showwarning("Aviso", "Nenhum item válido encontrado na lista!")
            return
        
        # Confirmação
        resposta = messagebox.askyesno(
            "Confirmar", 
            f"Deseja iniciar a migração de {len(itens)} item(ns)?\n\n"
            f"Cada item abrirá 2 abas no navegador (antigo e novo)."
        )
        if not resposta:
            return
        
        # Limpa treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Cria itens de migração e valida pastas
        self.itens_migracao = []
        pastas_nao_encontradas = []
        
        for protocolo, nome_pasta in itens:
            caminho_pasta = os.path.join(self.diretorio_base.get(), nome_pasta)
            
            # Valida se a pasta existe
            if not os.path.exists(caminho_pasta):
                pastas_nao_encontradas.append(f"Protocolo {protocolo}: {caminho_pasta}")
                continue
            
            item = MigracaoItem(protocolo, nome_pasta, self.diretorio_base.get())
            self.itens_migracao.append(item)
        
        # Se houver pastas não encontradas, mostra erro
        if pastas_nao_encontradas:
            mensagem = f"❌ {len(pastas_nao_encontradas)} pasta(s) não encontrada(s):\n\n"
            mensagem += "\n".join(pastas_nao_encontradas[:10])
            if len(pastas_nao_encontradas) > 10:
                mensagem += f"\n... e mais {len(pastas_nao_encontradas) - 10}"
            messagebox.showerror("Erro", mensagem)
            return
        
        if not self.itens_migracao:
            messagebox.showerror("Erro", "Nenhum item válido após validação de pastas!")
            return
            
            # Adiciona na treeview
            item_id = self.tree.insert('', tk.END, values=(
                protocolo,
                nome_pasta,
                item.status,
                f"{item.progresso}%",
                item.steps["Login"],
                item.steps["Extração"],
                item.steps["Preenchimento"],
                item.steps["Anexos"],
                item.mensagem
            ))
            item.tree_id = item_id
        
        # Salva configuração
        self.salvar_configuracao()
        
        # Inicia migração em thread separada
        self.status_bar.config(text=f"Iniciando migração de {len(itens)} item(ns)...")
        threading.Thread(target=self.executar_migracoes, daemon=True).start()
    
    def executar_migracoes(self):
        """Executa as migrações em sequência"""
        for item in self.itens_migracao:
            if item.status == "Cancelado":
                continue
            
            # Executa migração em thread separada
            thread = threading.Thread(target=self.executar_migracao_item, args=(item,), daemon=True)
            thread.start()
            item.thread = thread
            self.threads_ativas[item.protocolo] = thread
            
            # Aguarda um pouco antes do próximo
            threading.Event().wait(2)
    
    def executar_migracao_item(self, item):
        """Executa migração de um item"""
        try:
            item.status = "Executando"
            item.data_inicio = datetime.now()
            self.atualizar_item_tree(item)
            
            # Atualiza step Login
            item.steps["Login"] = "🔄"
            item.progresso = 10
            self.atualizar_item_tree(item)
            
            # Cria migrador com callback e mantém navegador aberto para verificação manual
            migrador = MigradorPEP(
                item.protocolo, 
                item.caminho_pasta,
                callback_progresso=callback_progresso,
                manter_navegador_aberto=True  # Mantém navegador aberto após anexos
            )
            
            # Executa migração (em loop de eventos assíncrono)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                # Executa a migração
                loop.run_until_complete(migrador.executar_migracao())
                
                # Atualiza steps
                item.steps["Login"] = "✅"
                item.steps["Extração"] = "✅"
                item.steps["Preenchimento"] = "✅"
                item.steps["Anexos"] = "✅"
                item.steps["Concluído"] = "✅"
                item.status = "Concluído"
                item.progresso = 100
                item.mensagem = "Migração concluída com sucesso!"
                item.data_fim = datetime.now()
                item.browser_aberto = True
                
            except Exception as e:
                item.status = "Erro"
                item.erro = str(e)
                item.mensagem = f"Erro: {str(e)}"
                item.progresso = 0
                
            finally:
                loop.close()
            
        except Exception as e:
            item.status = "Erro"
            item.erro = str(e)
            item.mensagem = f"Erro crítico: {str(e)}"
        
        finally:
            self.atualizar_item_tree(item)
            self.status_bar.config(text=f"Migração {item.protocolo} finalizada: {item.status}")
    
    def atualizar_item_tree(self, item):
        """Atualiza item na treeview"""
        if hasattr(item, 'tree_id'):
            self.tree.item(item.tree_id, values=(
                item.protocolo,
                item.nome_pasta,
                item.status,
                f"{item.progresso}%",
                item.steps["Login"],
                item.steps["Extração"],
                item.steps["Preenchimento"],
                item.steps["Anexos"],
                item.mensagem[:50] + "..." if len(item.mensagem) > 50 else item.mensagem
            ))
    
    def reimportar_selecionado(self):
        """Reimporta item selecionado"""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para reimportar!")
            return
        
        item_id = selecionado[0]
        # Encontra item correspondente
        for item in self.itens_migracao:
            if hasattr(item, 'tree_id') and item.tree_id == item_id:
                # Reseta status
                item.status = "Pendente"
                item.progresso = 0
                item.erro = None
                item.mensagem = ""
                item.steps = {k: "⏳" for k in item.steps}
                item.data_inicio = None
                item.data_fim = None
                
                self.atualizar_item_tree(item)
                
                # Executa novamente
                thread = threading.Thread(target=self.executar_migracao_item, args=(item,), daemon=True)
                thread.start()
                item.thread = thread
                break
    
    def abrir_pasta_selecionada(self):
        """Abre pasta do item selecionado"""
        selecionado = self.tree.selection()
        if not selecionado:
            return
        
        item_id = selecionado[0]
        for item in self.itens_migracao:
            if hasattr(item, 'tree_id') and item.tree_id == item_id:
                if item.caminho_pasta and os.path.exists(item.caminho_pasta):
                    os.system(f'open "{item.caminho_pasta}"')
                break
    
    def remover_selecionado(self):
        """Remove item selecionado"""
        selecionado = self.tree.selection()
        if not selecionado:
            return
        
        item_id = selecionado[0]
        self.tree.delete(item_id)
        
        # Remove da lista
        for item in self.itens_migracao[:]:
            if hasattr(item, 'tree_id') and item.tree_id == item_id:
                self.itens_migracao.remove(item)
                break
    
    def salvar_configuracao(self):
        """Salva configuração em arquivo"""
        config = {
            'diretorio_base': self.diretorio_base.get()
        }
        try:
            with open('config_gui.json', 'w') as f:
                json.dump(config, f)
        except:
            pass
    
    def carregar_configuracao(self):
        """Carrega configuração do arquivo"""
        try:
            if os.path.exists('config_gui.json'):
                with open('config_gui.json', 'r') as f:
                    config = json.load(f)
                    if 'diretorio_base' in config:
                        self.diretorio_base.set(config['diretorio_base'])
        except:
            pass


def main():
    """Função principal"""
    try:
        root = tk.Tk()
        # Configurações para evitar problemas de compatibilidade
        root.withdraw()  # Esconde temporariamente para evitar problemas de inicialização
        root.update()
        root.deiconify()  # Mostra novamente
        
        app = GUIMigrador(root)
        root.mainloop()
    except Exception as e:
        print(f"Erro ao iniciar interface gráfica: {e}")
        import traceback
        traceback.print_exc()
        print("\n💡 Tentando modo alternativo...")
        # Tenta modo simplificado
        try:
            root = tk.Tk()
            root.title("Migrador PEP")
            label = tk.Label(root, text="Interface carregando...")
            label.pack(padx=20, pady=20)
            root.update()
            root.deiconify()
            app = GUIMigrador(root)
            root.mainloop()
        except Exception as e2:
            print(f"Erro no modo alternativo: {e2}")
            print("\n❌ Não foi possível iniciar a interface gráfica.")
            print("💡 Tente usar o script de linha de comando:")
            print("   python3 migrador_pep.py <protocolo> <caminho_pasta>")


if __name__ == "__main__":
    main()

