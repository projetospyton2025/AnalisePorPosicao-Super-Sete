"""
Model para armazenamento e gerenciamento de resultados da Super Sete.
"""
import sqlite3
import logging
from datetime import datetime
from typing import List, Dict, Optional
from config import Config, SuperSeteConfig

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResultadoModel:
    """
    Gerencia o armazenamento e recuperação de resultados da Super Sete no SQLite.
    """
    
    def __init__(self, db_path: str = None):
        """
        Inicializa o modelo com o caminho do banco de dados.
        
        Args:
            db_path: Caminho para o arquivo do banco SQLite
        """
        self.db_path = db_path or Config.DATABASE_PATH
        self._criar_tabela()
    
    def _criar_tabela(self):
        """Cria a tabela de resultados se não existir"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS resultados (
                    numero INTEGER PRIMARY KEY,
                    data_apuracao TEXT,
                    data_proximo_concurso TEXT,
                    coluna_1 INTEGER,
                    coluna_2 INTEGER,
                    coluna_3 INTEGER,
                    coluna_4 INTEGER,
                    coluna_5 INTEGER,
                    coluna_6 INTEGER,
                    coluna_7 INTEGER,
                    acumulado INTEGER,
                    valor_acumulado_proximo_concurso REAL,
                    valor_estimado_proximo_concurso REAL,
                    valor_arrecadado REAL,
                    valor_total_premio_faixa_um REAL,
                    ganhadores_faixa_1 INTEGER,
                    ganhadores_faixa_2 INTEGER,
                    ganhadores_faixa_3 INTEGER,
                    ganhadores_faixa_4 INTEGER,
                    ganhadores_faixa_5 INTEGER,
                    valor_premio_faixa_1 REAL,
                    valor_premio_faixa_2 REAL,
                    valor_premio_faixa_3 REAL,
                    valor_premio_faixa_4 REAL,
                    valor_premio_faixa_5 REAL,
                    local_sorteio TEXT,
                    municipio_uf_sorteio TEXT,
                    numero_concurso_anterior INTEGER,
                    numero_concurso_proximo INTEGER,
                    tipo_jogo TEXT,
                    data_insercao TEXT
                )
            ''')
            conn.commit()
    
    def inserir(self, resultado: Dict) -> bool:
        """
        Insere ou atualiza um resultado no banco de dados.
        
        Args:
            resultado: Dicionário com os dados do resultado da API
            
        Returns:
            True se a operação foi bem sucedida, False caso contrário
        """
        try:
            # Extrair os números das colunas
            lista_dezenas = resultado.get('listaDezenas', [])
            if len(lista_dezenas) != SuperSeteConfig.TOTAL_COLUNAS:
                return False
            
            # Extrair dados dos prêmios
            lista_rateio = resultado.get('listaRateioPremio', [])
            
            ganhadores = [0] * 5
            valores_premio = [0.0] * 5
            
            for rateio in lista_rateio:
                faixa = rateio.get('faixa', 0)
                if 1 <= faixa <= 5:
                    ganhadores[faixa - 1] = rateio.get('numeroDeGanhadores', 0)
                    valores_premio[faixa - 1] = rateio.get('valorPremio', 0.0)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO resultados (
                        numero, data_apuracao, data_proximo_concurso,
                        coluna_1, coluna_2, coluna_3, coluna_4, coluna_5, coluna_6, coluna_7,
                        acumulado, valor_acumulado_proximo_concurso, 
                        valor_estimado_proximo_concurso, valor_arrecadado,
                        valor_total_premio_faixa_um,
                        ganhadores_faixa_1, ganhadores_faixa_2, ganhadores_faixa_3,
                        ganhadores_faixa_4, ganhadores_faixa_5,
                        valor_premio_faixa_1, valor_premio_faixa_2, valor_premio_faixa_3,
                        valor_premio_faixa_4, valor_premio_faixa_5,
                        local_sorteio, municipio_uf_sorteio,
                        numero_concurso_anterior, numero_concurso_proximo,
                        tipo_jogo, data_insercao
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    resultado.get('numero'),
                    resultado.get('dataApuracao'),
                    resultado.get('dataProximoConcurso'),
                    int(lista_dezenas[0]),
                    int(lista_dezenas[1]),
                    int(lista_dezenas[2]),
                    int(lista_dezenas[3]),
                    int(lista_dezenas[4]),
                    int(lista_dezenas[5]),
                    int(lista_dezenas[6]),
                    1 if resultado.get('acumulado') else 0,
                    resultado.get('valorAcumuladoProximoConcurso', 0.0),
                    resultado.get('valorEstimadoProximoConcurso', 0.0),
                    resultado.get('valorArrecadado', 0.0),
                    resultado.get('valorTotalPremioFaixaUm', 0.0),
                    ganhadores[0], ganhadores[1], ganhadores[2], ganhadores[3], ganhadores[4],
                    valores_premio[0], valores_premio[1], valores_premio[2], 
                    valores_premio[3], valores_premio[4],
                    resultado.get('localSorteio'),
                    resultado.get('nomeMunicipioUFSorteio'),
                    resultado.get('numeroConcursoAnterior'),
                    resultado.get('numeroConcursoProximo'),
                    resultado.get('tipoJogo'),
                    datetime.now().isoformat()
                ))
                conn.commit()
            return True
        except Exception as e:
            logger.error(f"Erro ao inserir resultado: {e}")
            return False
    
    def buscar_ultimo(self) -> Optional[Dict]:
        """
        Busca o último resultado cadastrado.
        
        Returns:
            Dicionário com os dados do último resultado ou None
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM resultados ORDER BY numero DESC LIMIT 1')
                row = cursor.fetchone()
                
                if row:
                    return dict(row)
                return None
        except Exception as e:
            logger.error(f"Erro ao buscar último resultado: {e}")
            return None
    
    def buscar_todos(self, limite: int = None) -> List[Dict]:
        """
        Busca todos os resultados cadastrados.
        
        Args:
            limite: Número máximo de resultados a retornar
            
        Returns:
            Lista de dicionários com os resultados
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                if limite:
                    cursor.execute(
                        'SELECT * FROM resultados ORDER BY numero DESC LIMIT ?',
                        (limite,)
                    )
                else:
                    cursor.execute('SELECT * FROM resultados ORDER BY numero DESC')
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Erro ao buscar todos os resultados: {e}")
            return []
    
    def buscar_por_numero(self, numero: int) -> Optional[Dict]:
        """
        Busca um resultado específico pelo número do concurso.
        
        Args:
            numero: Número do concurso
            
        Returns:
            Dicionário com os dados do resultado ou None
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM resultados WHERE numero = ?', (numero,))
                row = cursor.fetchone()
                
                if row:
                    return dict(row)
                return None
        except Exception as e:
            logger.error(f"Erro ao buscar resultado por número: {e}")
            return None
    
    def contar_resultados(self) -> int:
        """
        Conta o número total de resultados cadastrados.
        
        Returns:
            Número total de resultados
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM resultados')
                return cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"Erro ao contar resultados: {e}")
            return 0
