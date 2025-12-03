"""
Script para migração automática de formulários do PEP CELESC
"""
import asyncio
import sys
import os
from playwright.async_api import async_playwright
import config


class MigradorPEP:
    def __init__(self, protocolo, caminho_pasta_anexos=None, callback_progresso=None, manter_navegador_aberto=False):
        self.protocolo = protocolo
        self.caminho_pasta_anexos = caminho_pasta_anexos
        self.url_login = config.URL_LOGIN
        self.url_base = config.URL_BASE_FORMULARIO
        self.usuario = config.USUARIO
        self.senha = config.SENHA
        self.delay = config.DELAY_PREENCHIMENTO
        self.headless = config.HEADLESS
        self.callback_progresso = callback_progresso
        self.manter_navegador_aberto = manter_navegador_aberto
        
        # URLs completas
        self.url_antiga = f"{self.url_base}?idSO={protocolo}"
        self.url_nova = self.url_base
    
    def atualizar_progresso(self, step, status, mensagem=""):
        """Atualiza progresso via callback"""
        if self.callback_progresso:
            self.callback_progresso(step, status, mensagem)

    async def fazer_login(self, page):
        """
        Realiza login no sistema PEP
        """
        print(f"🔐 Fazendo login no sistema...")
        print(f"🌐 Acessando: {self.url_login}")
        
        await page.goto(self.url_login, wait_until='networkidle')
        await page.wait_for_timeout(2000)
        
        # Procura pelos campos de login
        # Tenta diferentes seletores comuns para campos de login
        selectors_usuario = [
            'input[name="j_idt*:usuario"]',
            'input[id*="usuario"]',
            'input[type="text"]',
            'input[name*="user"]',
            'input[id*="user"]'
        ]
        
        selectors_senha = [
            'input[name="j_idt*:senha"]',
            'input[id*="senha"]',
            'input[type="password"]',
            'input[name*="pass"]',
            'input[id*="pass"]'
        ]
        
        # Encontra campo de usuário
        campo_usuario = None
        for selector in selectors_usuario:
            campo_usuario = await page.query_selector(selector)
            if campo_usuario:
                print(f"  ✓ Campo de usuário encontrado: {selector}")
                break
        
        # Encontra campo de senha
        campo_senha = None
        for selector in selectors_senha:
            campo_senha = await page.query_selector(selector)
            if campo_senha:
                print(f"  ✓ Campo de senha encontrado: {selector}")
                break
        
        if not campo_usuario or not campo_senha:
            # Tenta encontrar por labels ou textos próximos
            print("  ⚠ Tentando encontrar campos por texto...")
            await page.screenshot(path='debug_login.png')
            print("  📸 Screenshot salvo em debug_login.png para análise")
            
            # Lista todos os inputs para debug
            inputs = await page.query_selector_all('input')
            print(f"  📋 Encontrados {len(inputs)} campos input na página")
            for i, inp in enumerate(inputs):
                name = await inp.get_attribute('name')
                id_attr = await inp.get_attribute('id')
                input_type = await inp.get_attribute('type')
                print(f"    Input {i+1}: name={name}, id={id_attr}, type={input_type}")
        
        # Preenche usuário
        if campo_usuario:
            await campo_usuario.fill(self.usuario)
            await page.wait_for_timeout(500)
            print(f"  ✓ Usuário preenchido")
        else:
            raise Exception("Campo de usuário não encontrado")
        
        # Preenche senha
        if campo_senha:
            await campo_senha.fill(self.senha)
            await page.wait_for_timeout(500)
            print(f"  ✓ Senha preenchida")
        else:
            raise Exception("Campo de senha não encontrado")
        
        # Procura e clica no botão de login
        selectors_botao = [
            'button[type="submit"]',
            'input[type="submit"]',
            'button:has-text("Entrar")',
            'button:has-text("Login")',
            'a:has-text("Entrar")',
            'a:has-text("Login")',
            'button',
            'a.button'
        ]
        
        botao_login = None
        for selector in selectors_botao:
            botao_login = await page.query_selector(selector)
            if botao_login:
                texto = await botao_login.inner_text()
                if any(palavra in texto.lower() for palavra in ['entrar', 'login', 'acessar', 'submit']):
                    print(f"  ✓ Botão de login encontrado: {texto}")
                    break
        
        if botao_login:
            await botao_login.click()
            await page.wait_for_timeout(3000)
            print(f"  ✓ Login realizado")
        else:
            # Tenta pressionar Enter no campo de senha
            await campo_senha.press('Enter')
            await page.wait_for_timeout(3000)
            print(f"  ✓ Tentativa de login (Enter pressionado)")
        
        # Verifica se o login foi bem-sucedido (aguarda redirecionamento ou mudança na URL)
        await page.wait_for_timeout(2000)
        url_atual = page.url
        if 'login' not in url_atual.lower():
            print(f"  ✅ Login bem-sucedido! Redirecionado para: {url_atual}")
        else:
            print(f"  ⚠ Ainda na página de login. Verifique as credenciais.")
            await page.screenshot(path='debug_pos_login.png')
            print("  📸 Screenshot salvo em debug_pos_login.png")

    async def extrair_resumo_itinerario(self, page):
        """
        Extrai o resumo do itinerário de um input/textarea que contém logradouros separados por ponto e vírgula
        Retorna lista de logradouros
        """
        try:
            # Procura por input ou textarea que contenha o resumo do itinerário
            # Pode estar em um campo hidden ou visível
            selectors = [
                'input[type="hidden"][value*=";"]',
                'textarea[value*=";"]',
                'input[value*=";"]',
                'textarea'
            ]
            
            for selector in selectors:
                elementos = await page.query_selector_all(selector)
                for elemento in elementos:
                    value = await elemento.input_value() if await elemento.evaluate('el => el.tagName.toLowerCase()') == 'textarea' else await elemento.get_attribute('value')
                    
                    if value and ';' in value:
                        # Separa por ponto e vírgula e limpa os valores
                        logradouros = [log.strip() for log in value.split(';') if log.strip()]
                        if logradouros:
                            print(f"  📋 {len(logradouros)} logradouros encontrados no itinerário (separados por ;)")
                            return logradouros
            
            # Se não encontrou com ponto e vírgula, tenta extrair da tabela
            tabela = await page.query_selector('#form\\:tabs\\:tableLogradouros')
            if tabela:
                linhas = await tabela.query_selector_all('tbody tr:not(.ui-datatable-empty-message)')
                logradouros = []
                for linha in linhas:
                    celula = await linha.query_selector('td:first-child')
                    if celula:
                        texto = await celula.inner_text()
                        if texto and texto.strip():
                            logradouros.append(texto.strip())
                if logradouros:
                    print(f"  📋 {len(logradouros)} logradouros encontrados na tabela do itinerário")
                    return logradouros
            
            return []
        except Exception as e:
            print(f"  ⚠ Erro ao extrair resumo do itinerário: {str(e)}")
            return []

    async def extrair_dados_formulario_antigo(self, page):
        """
        Extrai os dados do formulário antigo (com protocolo)
        """
        print(f"\n📥 Extraindo dados do formulário antigo...")
        print(f"🌐 Acessando: {self.url_antiga}")
        
        await page.goto(self.url_antiga, wait_until='networkidle')
        await page.wait_for_timeout(3000)  # Aguarda carregamento completo
        
        dados = {}
        
        # Extrai todos os tipos de campos
        print("  🔍 Procurando campos no formulário...")
        
        # Inputs de texto, email, tel, number (NÃO inclui hidden)
        inputs = await page.query_selector_all('input[type="text"], input[type="email"], input[type="tel"], input[type="number"], input:not([type])')
        for input_elem in inputs:
            name = await input_elem.get_attribute('name')
            id_attr = await input_elem.get_attribute('id')
            input_type = await input_elem.get_attribute('type')
            
            # Ignora campos de sistema JSF e campos especiais
            if name and ('j_idt' in name or 'javax.faces.ViewState' in name or name == 'form'):
                continue
            
            value = await input_elem.input_value()
            
            # Ignora campos vazios
            if value:
                if name:
                    dados[name] = value
                elif id_attr:
                    dados[id_attr] = value
        
        # Textareas (ignora campos de sistema)
        textareas = await page.query_selector_all('textarea')
        for textarea in textareas:
            name = await textarea.get_attribute('name')
            id_attr = await textarea.get_attribute('id')
            
            # Ignora campos de sistema JSF
            if name and 'j_idt' in name:
                continue
            
            value = await textarea.input_value()
            if value:
                if name:
                    dados[name] = value
                elif id_attr:
                    dados[id_attr] = value
        
        # Selects (dropdowns)
        selects = await page.query_selector_all('select')
        for select in selects:
            name = await select.get_attribute('name')
            id_attr = await select.get_attribute('id')
            value = await select.evaluate('el => el.value')
            if value:
                if name:
                    dados[name] = value
                elif id_attr:
                    dados[id_attr] = value
        
        # Checkboxes e radios selecionados
        checkboxes = await page.query_selector_all('input[type="checkbox"]:checked, input[type="radio"]:checked')
        for checkbox in checkboxes:
            name = await checkbox.get_attribute('name')
            id_attr = await checkbox.get_attribute('id')
            value = await checkbox.get_attribute('value')
            if value:
                if name:
                    dados[name] = value
                elif id_attr:
                    dados[id_attr] = value
        
        # Extrai resumo do itinerário
        dados['_itinerario_logradouros'] = await self.extrair_resumo_itinerario(page)
        
        print(f"  ✅ {len(dados)} campos encontrados com valores")
        return dados

    def normalizar_nome_logradouro(self, nome):
        """
        Normaliza o nome do logradouro para comparação:
        - Remove artigos comuns (DA, DE, DO, DAS, DOS)
        - Remove espaços extras
        - Converte para minúsculas
        - Remove acentos (simplificado)
        """
        if not nome:
            return ""
        
        # Converte para minúsculas e remove espaços extras
        nome = nome.lower().strip()
        
        # Remove artigos comuns
        artigos = [' da ', ' de ', ' do ', ' das ', ' dos ', ' e ', ' em ', ' na ', ' no ']
        for artigo in artigos:
            nome = nome.replace(artigo, ' ')
        
        # Remove espaços múltiplos
        nome = ' '.join(nome.split())
        
        return nome
    
    def comparar_logradouros(self, nome1, nome2):
        """
        Compara dois nomes de logradouro de forma flexível
        Retorna True se forem considerados equivalentes
        """
        if not nome1 or not nome2:
            return False
        
        # Normaliza ambos
        nome1_norm = self.normalizar_nome_logradouro(nome1)
        nome2_norm = self.normalizar_nome_logradouro(nome2)
        
        # Match exato após normalização
        if nome1_norm == nome2_norm:
            return True
        
        # Extrai palavras-chave (ignora artigos e palavras muito curtas)
        palavras1 = [p for p in nome1_norm.split() if len(p) > 2]
        palavras2 = [p for p in nome2_norm.split() if len(p) > 2]
        
        if not palavras1 or not palavras2:
            return False
        
        # Verifica se todas as palavras importantes de nome1 estão em nome2
        # (permite que nome2 tenha palavras a mais, mas deve conter as principais)
        palavras_encontradas = sum(1 for p1 in palavras1 if any(p1 in p2 or p2 in p1 for p2 in palavras2))
        
        # Se pelo menos 70% das palavras foram encontradas, considera match
        if palavras_encontradas >= len(palavras1) * 0.7:
            return True
        
        # Tenta match reverso (palavras de nome2 em nome1)
        palavras_encontradas_reverso = sum(1 for p2 in palavras2 if any(p2 in p1 or p1 in p2 for p1 in palavras1))
        if palavras_encontradas_reverso >= len(palavras2) * 0.7:
            return True
        
        return False

    async def buscar_logradouro_no_select(self, page, nome_logradouro):
        """
        Busca um logradouro no select do itinerário com lógica flexível para lidar com abreviações
        Retorna True se encontrado e selecionado
        """
        try:
            select_logradouro = await page.query_selector('select[name="form:tabs:logradouroItinerario"]')
            if not select_logradouro:
                return False
            
            # Pega todas as opções do select (exceto a opção vazia)
            opcoes = await select_logradouro.query_selector_all('option[value]:not([value=""])')
            
            nome_logradouro_limpo = nome_logradouro.strip()
            
            # Primeiro tenta match exato (case insensitive)
            for opcao in opcoes:
                texto = await opcao.inner_text()
                valor = await opcao.get_attribute('value')
                
                if not texto or not valor:
                    continue
                
                texto_limpo = texto.strip()
                
                # Match exato
                if texto_limpo.lower() == nome_logradouro_limpo.lower():
                    await select_logradouro.select_option(value=valor)
                    await page.wait_for_timeout(500)
                    print(f"      ✓ Logradouro encontrado (match exato): {texto}")
                    return True
            
            # Se não encontrou match exato, tenta busca flexível
            melhor_match = None
            melhor_score = 0
            
            for opcao in opcoes:
                texto = await opcao.inner_text()
                valor = await opcao.get_attribute('value')
                
                if not texto or not valor:
                    continue
                
                # Usa a função de comparação flexível
                if self.comparar_logradouros(nome_logradouro_limpo, texto):
                    # Calcula um score baseado na similaridade
                    nome_norm = self.normalizar_nome_logradouro(nome_logradouro_limpo)
                    texto_norm = self.normalizar_nome_logradouro(texto)
                    
                    # Score baseado em quantas palavras coincidem
                    palavras1 = set(nome_norm.split())
                    palavras2 = set(texto_norm.split())
                    palavras_comuns = palavras1.intersection(palavras2)
                    score = len(palavras_comuns) / max(len(palavras1), len(palavras2), 1)
                    
                    if score > melhor_score:
                        melhor_score = score
                        melhor_match = (texto, valor)
            
            # Se encontrou um match com score razoável, seleciona
            if melhor_match and melhor_score > 0.5:
                await select_logradouro.select_option(value=melhor_match[1])
                await page.wait_for_timeout(500)
                print(f"      ✓ Logradouro encontrado (match flexível, score: {melhor_score:.2f}): {melhor_match[0]}")
                return True
            
            return False
        except Exception as e:
            print(f"    ⚠ Erro ao buscar logradouro: {str(e)}")
            return False

    async def buscar_logradouro_em_bairro(self, page, estado, municipio, bairro, nome_logradouro):
        """
        Busca um logradouro em um bairro específico
        Retorna True se encontrado e selecionado
        """
        try:
            # Preenche Estado
            if not await self.preencher_select_dependente(page, 'form:tabs:estadoItinerario', estado, 2000):
                return False
            
            # Preenche Município
            if not await self.preencher_select_dependente(page, 'form:tabs:municipioItinerario', municipio, 2000):
                return False
            
            # Preenche Bairro
            if not await self.preencher_select_dependente(page, 'form:tabs:bairroItinerario', bairro, 2000):
                return False
            
            # Busca o logradouro
            return await self.buscar_logradouro_no_select(page, nome_logradouro)
        except Exception as e:
            print(f"    ⚠ Erro ao buscar logradouro em bairro: {str(e)}")
            return False

    async def buscar_logradouro_em_todos_bairros(self, page, estado, municipio, nome_logradouro):
        """
        Busca um logradouro em todos os bairros do município
        Retorna True se encontrado
        """
        try:
            # Preenche Estado
            if not await self.preencher_select_dependente(page, 'form:tabs:estadoItinerario', estado, 2000):
                return False
            
            # Preenche Município
            if not await self.preencher_select_dependente(page, 'form:tabs:municipioItinerario', municipio, 2000):
                return False
            
            # Pega todos os bairros disponíveis
            select_bairro = await page.query_selector('select[name="form:tabs:bairroItinerario"]')
            if not select_bairro:
                return False
            
            opcoes_bairro = await select_bairro.query_selector_all('option[value]:not([value=""])')
            
            for opcao_bairro in opcoes_bairro:
                valor_bairro = await opcao_bairro.get_attribute('value')
                if not valor_bairro:
                    continue
                
                # Seleciona o bairro
                await select_bairro.select_option(value=valor_bairro)
                await page.wait_for_timeout(2000)  # Aguarda carregar logradouros
                
                # Busca o logradouro neste bairro
                if await self.buscar_logradouro_no_select(page, nome_logradouro):
                    return True
            
            return False
        except Exception as e:
            print(f"    ⚠ Erro ao buscar logradouro em todos os bairros: {str(e)}")
            return False

    async def processar_itinerario(self, page, dados):
        """
        Processa o itinerário: para cada logradouro, preenche Estado/Município/Bairro.
        Se houver exatamente 2 itinerários: usa Ponta A para o primeiro e Ponta B para o segundo.
        Caso contrário: sempre usa Ponta A.
        """
        logradouros = dados.get('_itinerario_logradouros', [])
        if not logradouros:
            print("  ℹ️ Nenhum logradouro no itinerário para processar")
            return []
        
        # Pega dados da Ponta A e Ponta B
        estado_a = dados.get('form:tabs:estadoA', '')
        municipio_a = dados.get('form:tabs:municipioA', '')
        bairro_a = dados.get('form:tabs:bairroA', '')
        
        estado_b = dados.get('form:tabs:estadoB', '')
        municipio_b = dados.get('form:tabs:municipioB', '')
        bairro_b = dados.get('form:tabs:bairroB', '')
        
        if not estado_a or not municipio_a or not bairro_a:
            print("  ⚠ Dados da Ponta A incompletos, não é possível processar itinerário")
            return []
        
        # Verifica se há exatamente 2 itinerários
        usar_ponta_b = (len(logradouros) == 2) and estado_b and municipio_b and bairro_b
        
        logradouros_nao_encontrados = []
        logradouros_encontrados = []
        
        print(f"\n  🗺️ Processando {len(logradouros)} logradouros do itinerário...")
        if usar_ponta_b:
            print(f"  📍 Estratégia: Ponta A para o 1º, Ponta B para o 2º")
        else:
            print(f"  📍 Estratégia: Sempre usando Ponta A para todos")
        
        for idx, nome_logradouro in enumerate(logradouros, 1):
            print(f"\n  [{idx}/{len(logradouros)}] Processando: {nome_logradouro}")
            
            # Decide qual ponto usar: se for exatamente 2 itinerários, usa Ponta B para o segundo
            if usar_ponta_b and idx == 2:
                estado_ref = estado_b
                municipio_ref = municipio_b
                bairro_ref = bairro_b
                ponto_ref = "Ponta B"
            else:
                estado_ref = estado_a
                municipio_ref = municipio_a
                bairro_ref = bairro_a
                ponto_ref = "Ponta A"
            
            print(f"    📍 Usando referência: {ponto_ref} ({estado_ref} / {municipio_ref} / {bairro_ref})")
            
            try:
                # Passo 1: Preenche Estado do Itinerário
                print(f"    📍 Preenchendo Estado...")
                if not await self.preencher_select_dependente(page, 'form:tabs:estadoItinerario', estado_ref, 2000):
                    print(f"    ⚠ Não foi possível preencher Estado")
                    logradouros_nao_encontrados.append(nome_logradouro)
                    continue
                
                # Passo 2: Preenche Município do Itinerário
                print(f"    📍 Preenchendo Município...")
                if not await self.preencher_select_dependente(page, 'form:tabs:municipioItinerario', municipio_ref, 2000):
                    print(f"    ⚠ Não foi possível preencher Município")
                    logradouros_nao_encontrados.append(nome_logradouro)
                    continue
                
                # Passo 3: Preenche Bairro do Itinerário
                print(f"    📍 Preenchendo Bairro...")
                if not await self.preencher_select_dependente(page, 'form:tabs:bairroItinerario', bairro_ref, 2000):
                    print(f"    ⚠ Não foi possível preencher Bairro")
                    logradouros_nao_encontrados.append(nome_logradouro)
                    continue
                
                # Passo 4: Busca o logradouro no combo (deve aparecer após preencher os 3 campos)
                print(f"    🔍 Buscando logradouro no combo...")
                encontrado = await self.buscar_logradouro_no_select(page, nome_logradouro)
                
                if encontrado:
                    print(f"    ✅ Logradouro encontrado!")
                    
                    # Passo 5: Clica no botão "Incluir Logradouro"
                    print(f"    ➕ Clicando em 'Incluir Logradouro'...")
                    try:
                        botao_incluir = await page.query_selector('button[name="form:tabs:j_idt227"]')
                        if botao_incluir:
                            await botao_incluir.click()
                            await page.wait_for_timeout(2000)  # Aguarda adicionar na tabela e limpar formulário
                            print(f"    ✓ Logradouro adicionado ao itinerário (formulário limpo automaticamente)")
                            logradouros_encontrados.append(nome_logradouro)
                        else:
                            print(f"    ⚠ Botão 'Incluir Logradouro' não encontrado")
                            logradouros_nao_encontrados.append(nome_logradouro)
                    except Exception as e:
                        print(f"    ⚠ Erro ao clicar no botão Incluir: {str(e)}")
                        logradouros_nao_encontrados.append(nome_logradouro)
                else:
                    print(f"    ❌ Logradouro NÃO encontrado no combo")
                    # Tenta buscar em outros bairros usando a mesma referência
                    print(f"    🔍 Tentando buscar em outros bairros do município...")
                    encontrado_alternativo = await self.buscar_logradouro_em_todos_bairros(
                        page, estado_ref, municipio_ref, nome_logradouro
                    )
                    
                    if encontrado_alternativo:
                        print(f"    ✅ Logradouro encontrado em outro bairro!")
                        try:
                            botao_incluir = await page.query_selector('button[name="form:tabs:j_idt227"]')
                            if botao_incluir:
                                await botao_incluir.click()
                                await page.wait_for_timeout(2000)
                                print(f"    ✓ Logradouro adicionado ao itinerário")
                                logradouros_encontrados.append(nome_logradouro)
                            else:
                                logradouros_nao_encontrados.append(nome_logradouro)
                        except Exception as e:
                            logradouros_nao_encontrados.append(nome_logradouro)
                    else:
                        logradouros_nao_encontrados.append(nome_logradouro)
                        
            except Exception as e:
                print(f"    ❌ Erro ao processar logradouro: {str(e)}")
                logradouros_nao_encontrados.append(nome_logradouro)
        
        # Adiciona mensagem no comentário se houver logradouros não encontrados
        if logradouros_nao_encontrados:
            mensagem = "\n\n⚠️ ATENÇÃO - LOGRADOUROS NÃO ENCONTRADOS (CADASTRAR MANUALMENTE):\n"
            for logradouro in logradouros_nao_encontrados:
                mensagem += f"  • {logradouro}\n"
            
            # Adiciona ao campo de comentários
            try:
                campo_comentario = await page.query_selector('textarea[name="form:tabs:j_idt238"]')
                if campo_comentario:
                    comentario_atual = await campo_comentario.input_value()
                    novo_comentario = comentario_atual + mensagem if comentario_atual else mensagem
                    await campo_comentario.fill(novo_comentario)
                    print(f"\n  📝 Mensagem adicionada no comentário sobre {len(logradouros_nao_encontrados)} logradouros não encontrados")
            except Exception as e:
                print(f"  ⚠ Erro ao adicionar mensagem no comentário: {str(e)}")
        
        print(f"\n  ✅ Itinerário processado: {len(logradouros_encontrados)} encontrados, {len(logradouros_nao_encontrados)} não encontrados")
        return logradouros_encontrados

    def listar_arquivos_locais(self, caminho_pasta):
        """
        Lista arquivos de uma pasta local
        Retorna lista de caminhos completos dos arquivos
        """
        print(f"\n  📁 Listando arquivos da pasta local: {caminho_pasta}")
        
        arquivos = []
        
        try:
            # Verifica se a pasta existe
            if not os.path.exists(caminho_pasta):
                print(f"    ❌ Pasta não encontrada: {caminho_pasta}")
                return []
            
            if not os.path.isdir(caminho_pasta):
                print(f"    ❌ Caminho não é uma pasta: {caminho_pasta}")
                return []
            
            # Lista todos os arquivos na pasta
            itens = os.listdir(caminho_pasta)
            
            for item in itens:
                caminho_completo = os.path.join(caminho_pasta, item)
                
                # Ignora pastas e arquivos ocultos
                if os.path.isfile(caminho_completo) and not item.startswith('.'):
                    arquivos.append(caminho_completo)
                    print(f"    ✓ Arquivo encontrado: {item}")
            
            if not arquivos:
                print(f"    ⚠ Nenhum arquivo encontrado na pasta")
            else:
                print(f"    ✅ {len(arquivos)} arquivo(s) encontrado(s)")
            
            return arquivos
            
        except Exception as e:
            print(f"  ❌ Erro ao listar arquivos da pasta: {str(e)}")
            import traceback
            traceback.print_exc()
            return []

    async def mudar_para_aba_anexos(self, page):
        """
        Muda para a aba Anexos
        """
        try:
            # Aguarda um pouco para garantir que a página está pronta
            await page.wait_for_timeout(1000)
            
            print("    🔍 Procurando aba 'Anexos'...")
            
            # Tenta diferentes seletores para a aba Anexos
            seletores_aba = [
                'a[href="#form:tabs:tabAnexo"]',
                'a[href*="tabAnexo"]',
                'li[data-index="2"] a',  # Terceira aba (índice 2: Serviço=0, Cliente=1, Anexos=2)
                'li:has-text("Anexos") a',
                '[role="tab"]:has-text("Anexos")',
                'a:has-text("Anexos")'
            ]
            
            aba_anexos = None
            seletor_usado = None
            for selector in seletores_aba:
                try:
                    aba_anexos = await page.query_selector(selector)
                    if aba_anexos:
                        seletor_usado = selector
                        print(f"    ✓ Aba Anexos encontrada com seletor: {selector}")
                        break
                except Exception as e:
                    continue
            
            if aba_anexos:
                # Rola até o elemento se necessário
                await aba_anexos.scroll_into_view_if_needed()
                await page.wait_for_timeout(500)
                
                # Verifica se já está ativa
                classes = await aba_anexos.evaluate('el => el.closest("li")?.className || ""')
                if 'ui-state-active' in classes or 'ui-tabs-selected' in classes:
                    print("    ✓ Aba 'Anexos' já está ativa")
                    return True
                
                # Clica na aba
                print("    👆 Clicando na aba 'Anexos'...")
                await aba_anexos.click()
                await page.wait_for_timeout(2000)  # Aguarda aba carregar
                
                # Verifica se a aba foi ativada (procura pelo painel visível)
                try:
                    # Aguarda o painel da aba Anexos ficar visível
                    await page.wait_for_selector('#form\\:tabs\\:tabAnexo:not(.ui-helper-hidden)', timeout=3000)
                    print("  ✓ Aba 'Anexos' ativada com sucesso")
                    return True
                except:
                    # Tenta verificar de outra forma
                    aba_ativa = await page.query_selector('#form\\:tabs\\:tabAnexo')
                    if aba_ativa:
                        classes = await aba_ativa.get_attribute('class')
                        if classes and 'ui-helper-hidden' not in classes:
                            print("  ✓ Aba 'Anexos' ativada")
                            return True
                    
                    # Tenta verificar pelo índice da aba
                    li_aba = await aba_anexos.evaluate_handle('el => el.closest("li")')
                    if li_aba:
                        classes_li = await li_aba.get_attribute('class')
                        if classes_li and ('ui-state-active' in classes_li or 'ui-tabs-selected' in classes_li):
                            print("  ✓ Aba 'Anexos' ativada (verificado pelo li)")
                            return True
                    
                    print("  ⚠ Aba 'Anexos' clicada, mas pode não estar totalmente visível")
                    print("  💡 Verificando manualmente...")
                    await page.wait_for_timeout(2000)
                    return True  # Assume que funcionou
            else:
                print("  ⚠ Aba 'Anexos' não encontrada automaticamente")
                print("  💡 Tentando encontrar todas as abas disponíveis...")
                
                # Lista todas as abas disponíveis
                todas_abas = await page.query_selector_all('li[role="tab"], a[href*="tab"]')
                print(f"    📋 Encontradas {len(todas_abas)} abas")
                for idx, aba in enumerate(todas_abas):
                    try:
                        texto = await aba.inner_text()
                        href = await aba.get_attribute('href')
                        print(f"      [{idx}] {texto} - {href}")
                    except:
                        pass
                
                print("  💡 Por favor, mude manualmente para a aba Anexos e pressione Enter...")
                input()
                return False
        except Exception as e:
            print(f"  ⚠ Erro ao mudar para aba Anexos: {str(e)}")
            import traceback
            traceback.print_exc()
            print("  💡 Por favor, mude manualmente para a aba Anexos e pressione Enter...")
            input()
            return False

    async def fazer_upload_anexos(self, page, arquivos):
        """
        Faz upload dos arquivos na aba Anexos
        Preenche primeiro o campo de texto com mensagem fixa
        """
        print(f"\n  📎 Processando anexos...")
        
        try:
            # Garante que está na aba "Anexos" (pode já estar se foi chamado após preencher CNPJ)
            print("  🔄 Garantindo que está na aba 'Anexos'...")
            if not await self.mudar_para_aba_anexos(page):
                print("  ⚠ Não foi possível ativar aba Anexos, tentando continuar...")
                await page.wait_for_timeout(2000)
            
            # Preenche o campo de texto com mensagem fixa
            print("  📝 Preenchendo campo de texto...")
            mensagem_fixa = "Segue o projeto para compartilhamento de poste."
            
            # O campo de texto está em um editor (iframe)
            # Procura pelo textarea do editor que está escondido
            campo_texto = await page.query_selector('textarea[name="form:tabs:editor_input"]')
            
            if campo_texto:
                try:
                    # Preenche o textarea escondido
                    await campo_texto.fill(mensagem_fixa)
                    await page.wait_for_timeout(500)
                    
                    # Dispara evento para atualizar o iframe do editor
                    await campo_texto.evaluate('el => el.dispatchEvent(new Event("input"))')
                    await page.wait_for_timeout(500)
                    
                    print(f"  ✓ Mensagem preenchida: '{mensagem_fixa}'")
                except Exception as e:
                    print(f"  ⚠ Erro ao preencher campo de texto: {str(e)}")
                    # Tenta método alternativo - clicar no iframe e digitar
                    try:
                        iframe_editor = await page.query_selector('#form\\:tabs\\:editor iframe')
                        if iframe_editor:
                            frame = await iframe_editor.content_frame()
                            if frame:
                                body = await frame.query_selector('body')
                                if body:
                                    await body.click()
                                    await body.type(mensagem_fixa)
                                    await page.wait_for_timeout(500)
                                    print(f"  ✓ Mensagem preenchida via iframe: '{mensagem_fixa}'")
                    except Exception as e2:
                        print(f"  ⚠ Erro ao preencher via iframe: {str(e2)}")
            else:
                print("  ⚠ Campo de texto não encontrado, continuando com upload...")
            
            if not arquivos:
                print("  ℹ️ Nenhum arquivo para anexar")
                print("  💡 Você pode fazer o upload manualmente na aba Anexos")
                return
            
            # Procura pelo input de upload do PrimeFaces
            print("  🔍 Procurando campo de upload...")
            
            # O PrimeFaces FileUpload geralmente tem um input file
            # Pode estar escondido ou dentro de um span com classe ui-fileupload-choose
            input_file = None
            
            # Tenta diferentes seletores
            seletores = [
                'input[type="file"][name*="j_idt358"]',
                'input[type="file"]',
                'input[type="file"][id*="j_idt358"]'
            ]
            
            for selector in seletores:
                input_file = await page.query_selector(selector)
                if input_file:
                    # Verifica se está visível ou se precisa clicar no botão primeiro
                    is_visible = await input_file.is_visible()
                    if not is_visible:
                        # Tenta clicar no botão "Selecionar Arquivos"
                        botao_selecionar = await page.query_selector('span.ui-fileupload-choose, button:has-text("Selecionar"), span:has-text("Selecionar Arquivos")')
                        if botao_selecionar:
                            await botao_selecionar.click()
                            await page.wait_for_timeout(500)
                    break
            
            if input_file:
                print("  ✓ Campo de upload encontrado")
                
                if not arquivos:
                    print("  ⚠ Nenhum arquivo para fazer upload")
                    print("  💡 Você pode fazer o upload manualmente clicando em 'Selecionar Arquivos'")
                    return
                
                # Filtra apenas arquivos que existem
                arquivos_validos = [arq for arq in arquivos if os.path.exists(arq)]
                
                if not arquivos_validos:
                    print("  ⚠ Nenhum arquivo válido encontrado")
                    return
                
                # Lista os arquivos que serão enviados
                print(f"  📋 Preparando upload de {len(arquivos_validos)} arquivo(s):")
                for idx, arquivo_path in enumerate(arquivos_validos, 1):
                    print(f"    [{idx}] {os.path.basename(arquivo_path)}")
                
                try:
                    # Envia TODOS os arquivos de uma vez
                    # Isso evita abrir múltiplos diálogos do macOS
                    print(f"\n  ⬆️ Enviando todos os arquivos de uma vez...")
                    await input_file.set_input_files(arquivos_validos)
                    await page.wait_for_timeout(3000)  # Aguarda upload processar
                    
                    print(f"  ✅ Upload de {len(arquivos_validos)} arquivo(s) concluído com sucesso!")
                    
                except Exception as e:
                    print(f"  ❌ Erro ao fazer upload dos arquivos: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    print("  💡 Você pode fazer o upload manualmente na aba Anexos")
            else:
                print("  ⚠ Campo de upload não encontrado automaticamente")
                print("  💡 Por favor, faça o upload manualmente dos arquivos na aba Anexos")
                print("  💡 Pressione Enter quando terminar...")
                input()
                
        except Exception as e:
            print(f"  ❌ Erro ao processar anexos: {str(e)}")
            import traceback
            traceback.print_exc()
            print("  💡 Você pode fazer o upload manualmente na aba Anexos")

    async def preencher_select_dependente(self, page, campo_select, valor, delay_extra=2000):
        """
        Preenche um select e aguarda o carregamento de campos dependentes (para PrimeFaces)
        """
        try:
            selector = f'select[name="{campo_select}"]'
            elemento = await page.query_selector(selector)
            
            if not elemento:
                return False
            
            # Seleciona o valor
            await elemento.select_option(value=str(valor))
            await page.wait_for_timeout(500)  # Pequeno delay para o evento disparar
            
            # Aguarda o carregamento dos campos dependentes (PrimeFaces faz AJAX)
            await page.wait_for_timeout(delay_extra)
            
            return True
        except Exception as e:
            print(f"    ⚠ Erro ao preencher select dependente {campo_select}: {str(e)}")
            return False

    async def preencher_cascata_endereco(self, page, dados, sufixo):
        """
        Preenche campos de endereço em cascata: Estado → Município → Bairro → Logradouro
        sufixo pode ser 'A', 'B', ou 'Itinerario'
        """
        campos_preenchidos = 0
        
        # Mapeamento de sufixos para nomes de campos completos
        if sufixo == 'Itinerario':
            campo_estado = 'form:tabs:estadoItinerario'
            campo_municipio = 'form:tabs:municipioItinerario'
            campo_bairro = 'form:tabs:bairroItinerario'
            campo_logradouro = 'form:tabs:logradouroItinerario'
        else:
            campo_estado = f'form:tabs:estado{sufixo}'
            campo_municipio = f'form:tabs:municipio{sufixo}'
            campo_bairro = f'form:tabs:bairro{sufixo}'
            campo_logradouro = f'form:tabs:logradouros{sufixo}'
        
        # Estado
        if campo_estado in dados and dados[campo_estado]:
            print(f"  📍 Preenchendo Estado ({sufixo})...")
            if await self.preencher_select_dependente(page, campo_estado, dados[campo_estado], 2000):
                campos_preenchidos += 1
                print(f"    ✓ Estado = {dados[campo_estado]}")
        
        # Município
        if campo_municipio in dados and dados[campo_municipio]:
            print(f"  📍 Preenchendo Município ({sufixo})...")
            if await self.preencher_select_dependente(page, campo_municipio, dados[campo_municipio], 2000):
                campos_preenchidos += 1
                print(f"    ✓ Município = {dados[campo_municipio]}")
        
        # Bairro
        if campo_bairro in dados and dados[campo_bairro]:
            print(f"  📍 Preenchendo Bairro ({sufixo})...")
            if await self.preencher_select_dependente(page, campo_bairro, dados[campo_bairro], 2000):
                campos_preenchidos += 1
                print(f"    ✓ Bairro = {dados[campo_bairro]}")
        
        # Logradouro
        if campo_logradouro in dados and dados[campo_logradouro]:
            print(f"  📍 Preenchendo Logradouro ({sufixo})...")
            if await self.preencher_select_dependente(page, campo_logradouro, dados[campo_logradouro], 1000):
                campos_preenchidos += 1
                print(f"    ✓ Logradouro = {dados[campo_logradouro]}")
        
        return campos_preenchidos

    async def preencher_formulario_novo(self, page, dados):
        """
        Preenche o novo formulário (sem protocolo) com os dados extraídos
        Foca na aba "Serviço" primeiro
        """
        print(f"\n📝 Preenchendo novo formulário...")
        print(f"🌐 Acessando: {self.url_nova}")
        
        await page.goto(self.url_nova, wait_until='networkidle')
        await page.wait_for_timeout(3000)  # Aguarda carregamento completo
        
        # Garante que está na aba "Serviço"
        print("  🔄 Garantindo que está na aba 'Serviço'...")
        try:
            aba_servico = await page.query_selector('a[href="#form:tabs:tabServico"]')
            if aba_servico:
                await aba_servico.click()
                await page.wait_for_timeout(1000)
                print("  ✓ Aba 'Serviço' ativada")
        except:
            print("  ⚠ Não foi possível ativar a aba 'Serviço' (pode já estar ativa)")
        
        campos_preenchidos = 0
        campos_nao_encontrados = []
        
        # Lista de campos que precisam ser preenchidos em ordem especial (selects dependentes)
        campos_cascata = ['estadoA', 'municipioA', 'bairroA', 'logradourosA',
                         'estadoB', 'municipioB', 'bairroB', 'logradourosB',
                         'estadoItinerario', 'municipioItinerario', 'bairroItinerario', 'logradouroItinerario']
        
        # Primeiro, preenche os campos de endereço em cascata (Ponta A e B)
        print("\n  🏠 Preenchendo endereços em cascata...")
        campos_preenchidos += await self.preencher_cascata_endereco(page, dados, 'A')
        campos_preenchidos += await self.preencher_cascata_endereco(page, dados, 'B')
        
        # Processa o itinerário (busca e adiciona logradouros)
        await self.processar_itinerario(page, dados)
        
        # Depois, preenche os demais campos
        print("\n  📋 Preenchendo demais campos...")
        campos_cascata_preenchidos = [
            'form:tabs:estadoA', 'form:tabs:municipioA', 'form:tabs:bairroA', 'form:tabs:logradourosA',
            'form:tabs:estadoB', 'form:tabs:municipioB', 'form:tabs:bairroB', 'form:tabs:logradourosB',
            'form:tabs:estadoItinerario', 'form:tabs:municipioItinerario', 
            'form:tabs:bairroItinerario', 'form:tabs:logradouroItinerario',
            '_itinerario_logradouros'  # Campo interno, não deve ser preenchido
        ]
        
        # Campos da aba "Dados Cliente" - preencher apenas CNPJ, ignorar os demais
        campos_dados_cliente = [
            'form:tabs:razaoSocial',
            'form:tabs:nmFantasia',
            'form:tabs:nmPessoaContato',
            'form:tabs:email',
            'form:tabs:celular',
            'form:tabs:foneEmergencia',
            'form:tabs:logradouroPJCompPoste',
            'form:tabs:nrLogrPJCompPoste',
            'form:tabs:complementoPJCompPoste',
            'form:tabs:bairroPJCompPoste',
            'form:tabs:cepPJCompPoste',
            'form:tabs:cidadePJCompPoste',
            'form:tabs:estadoPJCompPoste'
        ]
        
        # Preenche CNPJ primeiro (se existir) e aguarda o sistema preencher os demais campos
        cnpj_campo = 'form:tabs:cnpjCompPoste'
        if cnpj_campo in dados and dados[cnpj_campo]:
            print("\n  👤 Preenchendo CNPJ na aba 'Dados Cliente'...")
            try:
                # Ativa a aba "Dados Cliente"
                aba_cliente = await page.query_selector('a[href="#form:tabs:tabCliente"]')
                if aba_cliente:
                    await aba_cliente.click()
                    await page.wait_for_timeout(1000)
                    print("  ✓ Aba 'Dados Cliente' ativada")
                
                # Preenche o CNPJ
                campo_cnpj = await page.query_selector(f'input[name="{cnpj_campo}"]')
                if campo_cnpj:
                    await campo_cnpj.fill(str(dados[cnpj_campo]))
                    await page.wait_for_timeout(500)
                    
                    # Dispara o evento blur para o sistema buscar os dados automaticamente
                    # Usa evaluate para chamar blur() no elemento ou pressiona Tab
                    try:
                        await campo_cnpj.evaluate('el => el.blur()')
                    except:
                        # Se blur() não funcionar, pressiona Tab para sair do campo
                        await campo_cnpj.press('Tab')
                    
                    await page.wait_for_timeout(3000)  # Aguarda o sistema preencher os demais campos
                    print(f"  ✓ CNPJ preenchido: {dados[cnpj_campo]}")
                    print("  ✓ Sistema deve preencher os demais campos automaticamente")
                else:
                    print(f"  ⚠ Campo CNPJ não encontrado")
            except Exception as e:
                print(f"  ⚠ Erro ao preencher CNPJ: {str(e)}")
        
        # Se houver pasta de anexos informada, muda para aba Anexos após preencher CNPJ
        # Caso contrário, volta para aba Serviço para preencher demais campos
        if self.caminho_pasta_anexos:
            # Muda para aba Anexos - NÃO preenche mais campos da aba Serviço
            print("\n  📎 Mudando para aba 'Anexos' após preencher CNPJ...")
            await self.mudar_para_aba_anexos(page)
            # Para aqui - os anexos serão processados depois no fluxo principal
            return campos_preenchidos
        else:
            # Volta para a aba "Serviço" para preencher os demais campos
            try:
                aba_servico = await page.query_selector('a[href="#form:tabs:tabServico"]')
                if aba_servico:
                    await aba_servico.click()
                    await page.wait_for_timeout(1000)
            except:
                pass
        
        for campo, valor in dados.items():
            if not valor:
                continue
            
            # Pula campos de cascata que já foram preenchidos e campos internos
            if campo in campos_cascata_preenchidos:
                continue
            
            # Ignora campos da aba "Dados Cliente" (exceto CNPJ que já foi preenchido)
            if campo in campos_dados_cliente:
                continue
            
            # Ignora CNPJ (já foi preenchido na aba Dados Cliente)
            if campo == cnpj_campo:
                continue
            
            try:
                # Tenta encontrar o campo por diferentes métodos
                selectors = [
                    f'input[name="{campo}"]',
                    f'textarea[name="{campo}"]',
                    f'select[name="{campo}"]',
                    f'input#{campo}',
                    f'textarea#{campo}',
                    f'select#{campo}',
                    f'[name="{campo}"]'
                ]
                
                elemento = None
                for selector in selectors:
                    try:
                        elemento = await page.query_selector(selector)
                        if elemento:
                            break
                    except:
                        continue
                
                if elemento:
                    tag_name = await elemento.evaluate('el => el.tagName.toLowerCase()')
                    
                    if tag_name == 'select':
                        # Para selects normais (não dependentes)
                        try:
                            await elemento.select_option(value=str(valor))
                            await page.wait_for_timeout(self.delay)
                        except:
                            try:
                                await elemento.select_option(label=str(valor))
                                await page.wait_for_timeout(self.delay)
                            except:
                                print(f"  ⚠ Não foi possível selecionar valor '{valor}' no select {campo}")
                                campos_nao_encontrados.append(campo)
                                continue
                    elif tag_name == 'input':
                        input_type = await elemento.get_attribute('type')
                        if input_type in ['checkbox', 'radio']:
                            if str(valor).lower() in ['true', '1', 'on', 'yes', 'sim']:
                                await elemento.check()
                        else:
                            await elemento.fill(str(valor))
                    elif tag_name == 'textarea':
                        await elemento.fill(str(valor))
                    
                    await page.wait_for_timeout(self.delay)
                    campos_preenchidos += 1
                    print(f"  ✓ {campo} = {valor}")
                else:
                    campos_nao_encontrados.append(campo)
                    
            except Exception as e:
                print(f"  ⚠ Erro ao preencher {campo}: {str(e)}")
                campos_nao_encontrados.append(campo)
        
        print(f"\n✅ {campos_preenchidos} campos preenchidos com sucesso")
        if campos_nao_encontrados:
            print(f"⚠️ {len(campos_nao_encontrados)} campos não foram encontrados no novo formulário:")
            for campo in campos_nao_encontrados[:10]:  # Mostra apenas os 10 primeiros
                print(f"    - {campo}")
        
        return campos_preenchidos

    async def executar_migracao(self):
        """
        Executa o processo completo de migração
        """
        print("=" * 60)
        print("🚀 MIGRADOR AUTOMÁTICO PEP CELESC")
        print("=" * 60)
        print(f"📋 Protocolo: {self.protocolo}")
        print(f"🔗 URL Antiga: {self.url_antiga}")
        print(f"🔗 URL Nova: {self.url_nova}")
        print("=" * 60)
        
        p = None
        browser = None
        context = None
        page = None
        page_nova = None
        
        try:
            print("🔧 Inicializando Playwright...")
            
            # Inicializa Playwright (sem context manager quando manter_navegador_aberto=True)
            p = await async_playwright().start()
            print("🌐 Iniciando navegador...")
            
            # Tenta lançar o navegador com configurações para evitar detecção
            browser = await p.chromium.launch(
                headless=self.headless,
                slow_mo=50,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-web-security',
                    '--disable-features=IsolateOrigins,site-per-process',
                    '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                ]
            )
            
            # Verifica se o navegador está aberto
            if not browser:
                raise Exception("Falha ao iniciar o navegador")
            
            print("📄 Criando contexto do navegador...")
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                locale='pt-BR',
                timezone_id='America/Sao_Paulo',
                # Remove flags de automação
                ignore_https_errors=False
            )
            
            # Remove flags que identificam automação
            await context.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    
                    window.chrome = {
                        runtime: {}
                    };
                    
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5]
                    });
                    
                    Object.defineProperty(navigator, 'languages', {
                    get: () => ['pt-BR', 'pt', 'en']
                });
            """)
            
            # Verifica se o contexto foi criado
            if not context:
                raise Exception("Falha ao criar contexto do navegador")
            
            print("📑 Criando primeira página...")
            page = await context.new_page()
            
            # Verifica se a página foi criada
            if not page:
                raise Exception("Falha ao criar página")
            
            print("✅ Navegador inicializado com sucesso!")
            
            # Passo 1: Fazer login
            self.atualizar_progresso("Login", "🔄", "Fazendo login...")
            await self.fazer_login(page)
            self.atualizar_progresso("Login", "✅", "Login realizado com sucesso")
            
            # Passo 2: Extrair dados do formulário antigo
            self.atualizar_progresso("Extração", "🔄", "Extraindo dados do formulário antigo...")
            dados = await self.extrair_dados_formulario_antigo(page)
            self.atualizar_progresso("Extração", "✅", f"Dados extraídos: {len(dados)} campos")
            
            if not dados:
                print("\n⚠️ Nenhum dado encontrado no formulário antigo")
                print("📸 Verificando página...")
                await page.screenshot(path='debug_formulario_antigo.png')
                print("  Screenshot salvo em debug_formulario_antigo.png")
                if not self.manter_navegador_aberto:
                    if not self.headless:
                        print("\n⚠️ Pressione Enter para fechar o navegador...")
                        input()
                    await browser.close()
                    if p:
                        await p.stop()
                else:
                    print("\n✅ Navegador mantido aberto para verificação manual")
                return
            
            # Mostra os dados extraídos
            print("\n📋 Dados extraídos do formulário antigo:")
            print("-" * 60)
            for campo, valor in dados.items():
                # Trunca valores muito longos
                valor_display = str(valor)[:50] + "..." if len(str(valor)) > 50 else str(valor)
                print(f"  • {campo}: {valor_display}")
            print("-" * 60)
            
            # Passo 3: Abrir nova aba com formulário novo
            print("\n🆕 Abrindo nova aba para o formulário novo...")
            self.atualizar_progresso("Preenchimento", "🔄", "Abrindo formulário novo...")
            page_nova = await context.new_page()
            await page_nova.goto(self.url_nova, wait_until='networkidle')
            await page_nova.wait_for_timeout(2000)
            
            # Passo 4: Preencher o novo formulário
            self.atualizar_progresso("Preenchimento", "🔄", "Preenchendo campos...")
            await self.preencher_formulario_novo(page_nova, dados)
            self.atualizar_progresso("Preenchimento", "✅", "Formulário preenchido com sucesso")
            
            # Passo 5: Processar anexos locais (se fornecido)
            if self.caminho_pasta_anexos:
                print("\n" + "=" * 60)
                print("📎 PROCESSANDO ANEXOS")
                print("=" * 60)
                
                try:
                    self.atualizar_progresso("Anexos", "🔄", "Listando arquivos...")
                    # Lista arquivos da pasta local
                    arquivos = self.listar_arquivos_locais(self.caminho_pasta_anexos)
                    
                    self.atualizar_progresso("Anexos", "🔄", f"Fazendo upload de {len(arquivos)} arquivo(s)...")
                    # Faz upload (a função já ativa aba Anexos e preenche campo de texto)
                    await self.fazer_upload_anexos(page_nova, arquivos)
                    self.atualizar_progresso("Anexos", "✅", f"Upload concluído: {len(arquivos)} arquivo(s)")
                except Exception as e:
                    print(f"  ⚠ Erro ao processar anexos: {str(e)}")
                    self.atualizar_progresso("Anexos", "❌", f"Erro: {str(e)}")
                    import traceback
                    traceback.print_exc()
            
            print("\n" + "=" * 60)
            print("✨ MIGRAÇÃO CONCLUÍDA!")
            print("=" * 60)
            print("\n📌 IMPORTANTE:")
            print("  • Duas abas estão abertas:")
            print(f"    1. Formulário ANTIGO (protocolo {self.protocolo})")
            print("    2. Formulário NOVO (preenchido)")
            print("  • Revise ambos os formulários antes de submeter")
            print("  • NENHUM formulário será submetido automaticamente")
            
            # Mantém o navegador aberto para revisão (se não for modo GUI)
            if not self.manter_navegador_aberto:
                if not self.headless:
                    print("\n⚠️ Pressione Enter para fechar o navegador...")
                    input()
                # Fecha o navegador após o usuário pressionar Enter
                await browser.close()
                # Fecha o Playwright
                if p:
                    await p.stop()
            else:
                print("\n✅ Navegador mantido aberto para revisão (modo GUI)")
                print("   ⚠️  IMPORTANTE: As abas permanecerão abertas para você revisar e salvar manualmente.")
                print("   💡 Feche o navegador manualmente quando terminar a verificação.")
                print("   💡 O Playwright permanecerá ativo para manter o navegador aberto.")
                # NÃO fecha o navegador nem o Playwright quando manter_navegador_aberto=True
                
        except Exception as e:
            print(f"\n❌ Erro durante a migração: {str(e)}")
            import traceback
            traceback.print_exc()
            try:
                if page:
                    await page.screenshot(path='debug_erro.png')
                    print("📸 Screenshot do erro salvo em debug_erro.png")
            except:
                pass
            # Fecha o navegador em caso de erro (apenas se não for para manter aberto)
            if browser:
                if not self.manter_navegador_aberto:
                    try:
                        await browser.close()
                    except:
                        pass
                    # Fecha o Playwright também
                    if p:
                        try:
                            await p.stop()
                        except:
                            pass
                else:
                    print("\n⚠️ Erro ocorreu, mas navegador mantido aberto para verificação manual")
                    print("   💡 O Playwright permanecerá ativo para manter o navegador aberto.")
            elif p and not self.manter_navegador_aberto:
                # Se não conseguiu criar browser mas criou Playwright, fecha
                try:
                    await p.stop()
                except:
                    pass
            # Não faz raise para evitar erro duplo
            return


async def main():
    """
    Função principal
    Uso: python3 migrador_pep.py <protocolo> [caminho_pasta_anexos]
    Exemplo: 
        python3 migrador_pep.py 876686
        python3 migrador_pep.py 664276 /Users/gabrielrosch/git/ATPS-23-LGS-012
    """
    if len(sys.argv) < 2:
        print("❌ Erro: Protocolo não informado")
        print("\n📖 Uso:")
        print("   python3 migrador_pep.py <protocolo> [caminho_pasta_anexos]")
        print("\n📝 Exemplos:")
        print("   python3 migrador_pep.py 876686")
        print("   python3 migrador_pep.py 664276 /Users/gabrielrosch/git/ATPS-23-LGS-012")
        sys.exit(1)
    
    protocolo = sys.argv[1]
    caminho_pasta_anexos = sys.argv[2] if len(sys.argv) > 2 else None
    
    if caminho_pasta_anexos:
        # Expande ~ para home directory se necessário
        caminho_pasta_anexos = os.path.expanduser(caminho_pasta_anexos)
        
        # Valida se a pasta existe
        if not os.path.exists(caminho_pasta_anexos):
            print(f"❌ Erro: Pasta não encontrada: {caminho_pasta_anexos}")
            print("⚠️ A migração não será executada.")
            sys.exit(1)
        
        if not os.path.isdir(caminho_pasta_anexos):
            print(f"❌ Erro: Caminho não é uma pasta: {caminho_pasta_anexos}")
            print("⚠️ A migração não será executada.")
            sys.exit(1)
        
        print(f"📁 Pasta de anexos informada: {caminho_pasta_anexos}")
        print(f"✓ Pasta validada com sucesso")
    
    migrador = MigradorPEP(protocolo, caminho_pasta_anexos)
    await migrador.executar_migracao()


if __name__ == "__main__":
    asyncio.run(main())

