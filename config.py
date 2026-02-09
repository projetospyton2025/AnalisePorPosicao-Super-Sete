"""
Configurações e constantes do sistema de análise Super Sete.
"""
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do Flask
class Config:
    """Configurações gerais da aplicação"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'super-sete-secret-key-2025')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5057))
    
    # Banco de dados
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'database.db')
    
    # API Caixa
    API_SUPERSETE_URL = os.getenv(
        'API_SUPERSETE_URL',
        'https://servicebus2.caixa.gov.br/portaldeloterias/api/supersete'
    )

# Constantes da Super Sete
class SuperSeteConfig:
    """Constantes específicas da loteria Super Sete"""
    TOTAL_COLUNAS = 7
    MIN_NUMERO_COLUNA = 0
    MAX_NUMERO_COLUNA = 9
    NUMEROS_POR_COLUNA = 10  # 0 a 9
    
    # Identidade visual
    COR_PRINCIPAL = '#A9CF46'  # Verde-limão (54%)
    
    # Paleta de cores (0% a 100%)
    PALETA_CORES = {
        100: '#ffffff',
        95: '#f6faeb',
        90: '#ecf5d6',
        85: '#e3efc2',
        80: '#d9eaae',
        75: '#d0e59a',
        70: '#c6e085',
        65: '#bdda71',
        60: '#b3d55d',
        55: '#aad049',
        54: '#A9CF46',  # Cor principal
        50: '#a0cb34',
        45: '#90b62f',
        40: '#80a22a',
        35: '#708e25',
        30: '#607a1f',
        25: '#50651a',
        20: '#405115',
        15: '#303d10',
        10: '#20290a',
        5: '#101405',
        0: '#000000'
    }
    
    # Logo
    LOGO_URL = 'https://i.postimg.cc/wBthkvvc/supersete.png'
    
    # Estratégias de geração de palpites
    ESTRATEGIAS = [
        'equilibrada',
        'agressiva',
        'conservadora',
        'mista',
        'atrasados',
        'aleatorio_inteligente',
        'personalizado_por_coluna'
    ]
