"""
Script principal para migração automática de formulários
"""
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import config


class MigradorFormulario:
    def __init__(self):
        self.url_antiga = config.URL_FORMULARIO_ANTIGO
        self.url_nova = config.URL_FORMULARIO_NOVO
        self.delay = config.DELAY_PREENCHIMENTO
        self.headless = config.HEADLESS

    async def extrair_dados_formulario_antigo(self, page):
        """
        Extrai os dados do formulário antigo
        """
        print(f"🌐 Acessando formulário antigo: {self.url_antiga}")
        await page.goto(self.url_antiga, wait_until='networkidle')
        
        # Aguarda o formulário carregar
        await page.wait_for_timeout(2000)
        
        # Extrai todos os campos do formulário
        dados = {}
        
        # Inputs de texto, email, tel, etc.
        inputs = await page.query_selector_all('input[type="text"], input[type="email"], input[type="tel"], input[type="number"], input:not([type])')
        for input_elem in inputs:
            name = await input_elem.get_attribute('name')
            id_attr = await input_elem.get_attribute('id')
            value = await input_elem.input_value()
            if name:
                dados[name] = value
            elif id_attr:
                dados[id_attr] = value
        
        # Textareas
        textareas = await page.query_selector_all('textarea')
        for textarea in textareas:
            name = await textarea.get_attribute('name')
            id_attr = await textarea.get_attribute('id')
            value = await textarea.input_value()
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
            if name:
                dados[name] = value
            elif id_attr:
                dados[id_attr] = value
        
        print(f"✅ Dados extraídos: {len(dados)} campos encontrados")
        return dados

    async def preencher_formulario_novo(self, page, dados):
        """
        Preenche o novo formulário com os dados extraídos
        """
        print(f"🌐 Acessando formulário novo: {self.url_nova}")
        await page.goto(self.url_nova, wait_until='networkidle')
        
        # Aguarda o formulário carregar
        await page.wait_for_timeout(2000)
        
        campos_preenchidos = 0
        
        # Preenche campos por name
        for campo, valor in dados.items():
            if not valor:
                continue
                
            try:
                # Tenta encontrar por name
                selector_name = f'input[name="{campo}"], textarea[name="{campo}"], select[name="{campo}"]'
                elemento = await page.query_selector(selector_name)
                
                # Se não encontrar por name, tenta por id
                if not elemento:
                    selector_id = f'input#{campo}, textarea#{campo}, select#{campo}'
                    elemento = await page.query_selector(selector_id)
                
                if elemento:
                    tag_name = await elemento.evaluate('el => el.tagName.toLowerCase()')
                    
                    if tag_name == 'select':
                        await elemento.select_option(value=valor)
                    elif tag_name == 'input':
                        input_type = await elemento.get_attribute('type')
                        if input_type in ['checkbox', 'radio']:
                            await elemento.check()
                        else:
                            await elemento.fill(str(valor))
                    elif tag_name == 'textarea':
                        await elemento.fill(str(valor))
                    
                    await page.wait_for_timeout(self.delay)
                    campos_preenchidos += 1
                    print(f"  ✓ Preenchido: {campo} = {valor}")
                    
            except Exception as e:
                print(f"  ⚠ Erro ao preencher {campo}: {str(e)}")
        
        print(f"✅ {campos_preenchidos} campos preenchidos com sucesso")
        return campos_preenchidos

    async def executar_migracao(self):
        """
        Executa o processo completo de migração
        """
        async with async_playwright() as p:
            print("🚀 Iniciando migração de formulários...")
            
            # Inicia o navegador
            browser = await p.chromium.launch(headless=self.headless)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                # Passo 1: Extrair dados do formulário antigo
                dados = await self.extrair_dados_formulario_antigo(page)
                
                if not dados:
                    print("⚠️ Nenhum dado encontrado no formulário antigo")
                    return
                
                # Mostra os dados extraídos
                print("\n📋 Dados extraídos:")
                for campo, valor in dados.items():
                    print(f"  - {campo}: {valor}")
                
                # Passo 2: Preencher o novo formulário
                print("\n📝 Preenchendo novo formulário...")
                await self.preencher_formulario_novo(page, dados)
                
                print("\n✨ Migração concluída!")
                print("⚠️ Por favor, revise o formulário antes de submeter.")
                
                # Mantém o navegador aberto para revisão
                if not self.headless:
                    print("Pressione Enter para fechar o navegador...")
                    input()
                
            except Exception as e:
                print(f"❌ Erro durante a migração: {str(e)}")
                raise
            finally:
                await browser.close()


async def main():
    migrador = MigradorFormulario()
    await migrador.executar_migracao()


if __name__ == "__main__":
    asyncio.run(main())


