"""
Versão avançada do migrador com mapeamento customizado de campos
Use este arquivo se os nomes dos campos forem diferentes entre os formulários
"""
import asyncio
from playwright.async_api import async_playwright
import config


# Mapeamento customizado: {campo_antigo: campo_novo}
MAPEAMENTO_CAMPOS = {
    # Exemplo:
    # 'nome_completo': 'nome',
    # 'email_usuario': 'email',
    # 'telefone_contato': 'telefone',
    # Adicione seus mapeamentos aqui
}


class MigradorFormularioAvancado:
    def __init__(self):
        self.url_antiga = config.URL_FORMULARIO_ANTIGO
        self.url_nova = config.URL_FORMULARIO_NOVO
        self.delay = config.DELAY_PREENCHIMENTO
        self.headless = config.HEADLESS
        self.mapeamento = MAPEAMENTO_CAMPOS

    def mapear_campo(self, campo_antigo):
        """
        Retorna o nome do campo no novo formulário
        """
        return self.mapeamento.get(campo_antigo, campo_antigo)

    async def extrair_dados_formulario_antigo(self, page):
        """
        Extrai os dados do formulário antigo
        """
        print(f"🌐 Acessando formulário antigo: {self.url_antiga}")
        await page.goto(self.url_antiga, wait_until='networkidle')
        await page.wait_for_timeout(2000)
        
        dados = {}
        
        # Extrai todos os tipos de campos
        selectors = [
            'input[type="text"], input[type="email"], input[type="tel"], input[type="number"], input:not([type])',
            'textarea',
            'select',
            'input[type="checkbox"]:checked, input[type="radio"]:checked'
        ]
        
        for selector in selectors:
            elementos = await page.query_selector_all(selector)
            for elem in elementos:
                name = await elem.get_attribute('name')
                id_attr = await elem.get_attribute('id')
                
                # Pega o valor dependendo do tipo
                tag = await elem.evaluate('el => el.tagName.toLowerCase()')
                if tag == 'select':
                    value = await elem.evaluate('el => el.value')
                elif tag == 'input':
                    input_type = await elem.get_attribute('type')
                    if input_type in ['checkbox', 'radio']:
                        value = await elem.get_attribute('value')
                    else:
                        value = await elem.input_value()
                else:
                    value = await elem.input_value()
                
                if name:
                    dados[name] = value
                elif id_attr:
                    dados[id_attr] = value
        
        print(f"✅ Dados extraídos: {len(dados)} campos encontrados")
        return dados

    async def preencher_formulario_novo(self, page, dados):
        """
        Preenche o novo formulário com mapeamento customizado
        """
        print(f"🌐 Acessando formulário novo: {self.url_nova}")
        await page.goto(self.url_nova, wait_until='networkidle')
        await page.wait_for_timeout(2000)
        
        campos_preenchidos = 0
        
        for campo_antigo, valor in dados.items():
            if not valor:
                continue
            
            # Mapeia para o nome do campo no novo formulário
            campo_novo = self.mapear_campo(campo_antigo)
            
            try:
                # Tenta encontrar o campo
                selectors = [
                    f'input[name="{campo_novo}"]',
                    f'textarea[name="{campo_novo}"]',
                    f'select[name="{campo_novo}"]',
                    f'input#{campo_novo}',
                    f'textarea#{campo_novo}',
                    f'select#{campo_novo}',
                    f'[name="{campo_novo}"]',
                    f'#{campo_novo}'
                ]
                
                elemento = None
                for selector in selectors:
                    elemento = await page.query_selector(selector)
                    if elemento:
                        break
                
                if elemento:
                    tag_name = await elemento.evaluate('el => el.tagName.toLowerCase()')
                    
                    if tag_name == 'select':
                        # Tenta selecionar por valor ou texto
                        try:
                            await elemento.select_option(value=str(valor))
                        except:
                            await elemento.select_option(label=str(valor))
                    elif tag_name == 'input':
                        input_type = await elemento.get_attribute('type')
                        if input_type in ['checkbox', 'radio']:
                            if str(valor).lower() in ['true', '1', 'on', 'yes']:
                                await elemento.check()
                        else:
                            await elemento.fill(str(valor))
                    elif tag_name == 'textarea':
                        await elemento.fill(str(valor))
                    
                    await page.wait_for_timeout(self.delay)
                    campos_preenchidos += 1
                    print(f"  ✓ {campo_antigo} → {campo_novo} = {valor}")
                else:
                    print(f"  ⚠ Campo não encontrado: {campo_novo} (original: {campo_antigo})")
                    
            except Exception as e:
                print(f"  ❌ Erro ao preencher {campo_antigo} → {campo_novo}: {str(e)}")
        
        print(f"\n✅ {campos_preenchidos} campos preenchidos com sucesso")
        return campos_preenchidos

    async def executar_migracao(self):
        """
        Executa o processo completo de migração
        """
        async with async_playwright() as p:
            print("🚀 Iniciando migração avançada de formulários...")
            
            browser = await p.chromium.launch(headless=self.headless)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                dados = await self.extrair_dados_formulario_antigo(page)
                
                if not dados:
                    print("⚠️ Nenhum dado encontrado no formulário antigo")
                    return
                
                print("\n📋 Dados extraídos:")
                for campo, valor in dados.items():
                    print(f"  - {campo}: {valor}")
                
                print("\n📝 Preenchendo novo formulário...")
                await self.preencher_formulario_novo(page, dados)
                
                print("\n✨ Migração concluída!")
                print("⚠️ Por favor, revise o formulário antes de submeter.")
                
                if not self.headless:
                    print("Pressione Enter para fechar o navegador...")
                    input()
                
            except Exception as e:
                print(f"❌ Erro durante a migração: {str(e)}")
                raise
            finally:
                await browser.close()


async def main():
    migrador = MigradorFormularioAvancado()
    await migrador.executar_migracao()


if __name__ == "__main__":
    asyncio.run(main())


