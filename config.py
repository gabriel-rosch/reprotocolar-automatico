"""
Configurações do projeto
"""
import os
from dotenv import load_dotenv

load_dotenv()

# URLs
URL_LOGIN = os.getenv('URL_LOGIN', 'https://pep.celesc.com.br/PEP/externo/login.xhtml')
URL_BASE_FORMULARIO = os.getenv('URL_BASE_FORMULARIO', 'https://pep.celesc.com.br/PEP/externo/ot/compartilhamentoPoste.xhtml')

# Credenciais
USUARIO = os.getenv('USUARIO', '00793831903')
SENHA = os.getenv('SENHA', 'b$dEj@6L5#')

# Configurações
DELAY_PREENCHIMENTO = int(os.getenv('DELAY_PREENCHIMENTO', '500'))
HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'

