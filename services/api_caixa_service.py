"""
Serviço para integração com a API da Caixa Econômica Federal.
"""
import requests
import logging
from typing import Optional, Dict
from config import Config

# Configurar logging
logger = logging.getLogger(__name__)


class ApiCaixaService:
    """
    Serviço para consumir a API oficial da loteria Super Sete da Caixa.
    """
    
    def __init__(self):
        """Inicializa o serviço com a URL base da API"""
        self.base_url = Config.API_SUPERSETE_URL
        self.timeout = 30  # Timeout de 30 segundos
    
    def buscar_ultimo_concurso(self) -> Optional[Dict]:
        """
        Busca o último concurso disponível na API da Caixa.
        
        Returns:
            Dicionário com os dados do último concurso ou None em caso de erro
        """
        try:
            response = requests.get(self.base_url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao buscar último concurso: {e}")
            return None
        except ValueError as e:
            logger.error(f"Erro ao decodificar JSON: {e}")
            return None
    
    def buscar_concurso_especifico(self, numero: int) -> Optional[Dict]:
        """
        Busca um concurso específico na API da Caixa.
        
        Args:
            numero: Número do concurso a buscar
            
        Returns:
            Dicionário com os dados do concurso ou None em caso de erro
        """
        try:
            url = f"{self.base_url}/{numero}"
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao buscar concurso {numero}: {e}")
            return None
        except ValueError as e:
            logger.error(f"Erro ao decodificar JSON: {e}")
            return None
    
    def atualizar_base_completa(self, modelo_resultado) -> Dict:
        """
        Atualiza a base de dados com todos os concursos disponíveis.
        Faz uma atualização incremental, buscando apenas os concursos novos.
        
        Args:
            modelo_resultado: Instância do ResultadoModel para salvar os dados
            
        Returns:
            Dicionário com estatísticas da atualização
        """
        resultado_estatisticas = {
            'concursos_inseridos': 0,
            'concursos_atualizados': 0,
            'erros': 0,
            'ultimo_concurso': None
        }
        
        try:
            # Buscar o último concurso disponível na API
            ultimo_api = self.buscar_ultimo_concurso()
            if not ultimo_api:
                return resultado_estatisticas
            
            numero_ultimo_api = ultimo_api.get('numero')
            resultado_estatisticas['ultimo_concurso'] = numero_ultimo_api
            
            # Buscar o último concurso no banco de dados
            ultimo_banco = modelo_resultado.buscar_ultimo()
            numero_ultimo_banco = ultimo_banco['numero'] if ultimo_banco else 0
            
            # Inserir o último concurso da API
            if numero_ultimo_api > numero_ultimo_banco:
                if modelo_resultado.inserir(ultimo_api):
                    resultado_estatisticas['concursos_inseridos'] += 1
                else:
                    resultado_estatisticas['erros'] += 1
            
            # Buscar concursos anteriores que possam estar faltando
            # Começamos do último do banco e vamos até o último da API
            for numero in range(numero_ultimo_banco + 1, numero_ultimo_api):
                concurso = self.buscar_concurso_especifico(numero)
                if concurso:
                    if modelo_resultado.inserir(concurso):
                        resultado_estatisticas['concursos_inseridos'] += 1
                    else:
                        resultado_estatisticas['erros'] += 1
                else:
                    # Concurso não existe (pode ser número pulado)
                    continue
            
            return resultado_estatisticas
            
        except Exception as e:
            logger.error(f"Erro ao atualizar base completa: {e}")
            resultado_estatisticas['erros'] += 1
            return resultado_estatisticas
