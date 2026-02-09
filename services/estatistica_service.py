"""
Serviço de cálculo de estatísticas da Super Sete.
"""
from typing import Dict, List
from collections import defaultdict
from config import SuperSeteConfig


class EstatisticaService:
    """
    Serviço para cálculo de estatísticas dos resultados da Super Sete.
    Foca em análises por coluna, já que cada coluna é independente.
    """
    
    def __init__(self, modelo_resultado):
        """
        Inicializa o serviço com o modelo de resultados.
        
        Args:
            modelo_resultado: Instância do ResultadoModel
        """
        self.modelo = modelo_resultado
    
    def calcular_frequencia_por_coluna(self) -> Dict:
        """
        Calcula a frequência de cada número (0-9) em cada coluna (1-7).
        
        Returns:
            Estrutura: {"coluna_1": {"0": freq, "1": freq, ...}, "coluna_2": {...}, ...}
        """
        resultados = self.modelo.buscar_todos()
        
        # Inicializar estrutura de frequências
        frequencias = {}
        for coluna in range(1, SuperSeteConfig.TOTAL_COLUNAS + 1):
            frequencias[f'coluna_{coluna}'] = {
                str(num): 0 for num in range(SuperSeteConfig.MIN_NUMERO_COLUNA, 
                                              SuperSeteConfig.MAX_NUMERO_COLUNA + 1)
            }
        
        # Contar frequências
        for resultado in resultados:
            for coluna in range(1, SuperSeteConfig.TOTAL_COLUNAS + 1):
                numero = resultado.get(f'coluna_{coluna}')
                if numero is not None:
                    frequencias[f'coluna_{coluna}'][str(numero)] += 1
        
        return frequencias
    
    def calcular_atrasos_por_coluna(self) -> Dict:
        """
        Calcula o atraso (número de concursos desde a última aparição) 
        de cada número em cada coluna.
        
        Returns:
            Estrutura: {"coluna_1": {"0": atraso, "1": atraso, ...}, "coluna_2": {...}, ...}
        """
        resultados = self.modelo.buscar_todos()
        
        # Inicializar estrutura de atrasos
        atrasos = {}
        for coluna in range(1, SuperSeteConfig.TOTAL_COLUNAS + 1):
            atrasos[f'coluna_{coluna}'] = {
                str(num): 0 for num in range(SuperSeteConfig.MIN_NUMERO_COLUNA, 
                                              SuperSeteConfig.MAX_NUMERO_COLUNA + 1)
            }
        
        # Calcular atrasos (do mais recente para o mais antigo)
        for idx, resultado in enumerate(resultados):
            for coluna in range(1, SuperSeteConfig.TOTAL_COLUNAS + 1):
                numero = resultado.get(f'coluna_{coluna}')
                if numero is not None:
                    numero_str = str(numero)
                    # Se o atraso ainda é 0, significa que é a primeira aparição
                    if atrasos[f'coluna_{coluna}'][numero_str] == 0:
                        atrasos[f'coluna_{coluna}'][numero_str] = idx
        
        # Para números que nunca apareceram, o atraso é o total de concursos
        total_concursos = len(resultados)
        for coluna in range(1, SuperSeteConfig.TOTAL_COLUNAS + 1):
            for numero_str in atrasos[f'coluna_{coluna}']:
                if atrasos[f'coluna_{coluna}'][numero_str] == 0:
                    # Verificar se o número realmente nunca apareceu
                    apareceu = False
                    for resultado in resultados:
                        if resultado.get(f'coluna_{coluna}') == int(numero_str):
                            apareceu = True
                            break
                    if not apareceu:
                        atrasos[f'coluna_{coluna}'][numero_str] = total_concursos
        
        return atrasos
    
    def calcular_numeros_mais_frequentes_por_coluna(self, top: int = 3) -> Dict:
        """
        Retorna os números mais frequentes de cada coluna.
        
        Args:
            top: Quantidade de números a retornar por coluna
            
        Returns:
            Estrutura: {"coluna_1": [(numero, freq), ...], "coluna_2": [...], ...}
        """
        frequencias = self.calcular_frequencia_por_coluna()
        
        mais_frequentes = {}
        for coluna, nums in frequencias.items():
            # Ordenar por frequência (decrescente)
            sorted_nums = sorted(nums.items(), key=lambda x: x[1], reverse=True)
            mais_frequentes[coluna] = sorted_nums[:top]
        
        return mais_frequentes
    
    def calcular_numeros_mais_atrasados_por_coluna(self, top: int = 3) -> Dict:
        """
        Retorna os números mais atrasados de cada coluna.
        
        Args:
            top: Quantidade de números a retornar por coluna
            
        Returns:
            Estrutura: {"coluna_1": [(numero, atraso), ...], "coluna_2": [...], ...}
        """
        atrasos = self.calcular_atrasos_por_coluna()
        
        mais_atrasados = {}
        for coluna, nums in atrasos.items():
            # Ordenar por atraso (decrescente)
            sorted_nums = sorted(nums.items(), key=lambda x: x[1], reverse=True)
            mais_atrasados[coluna] = sorted_nums[:top]
        
        return mais_atrasados
    
    def calcular_pares_impares_por_coluna(self) -> Dict:
        """
        Calcula a distribuição de números pares e ímpares por coluna.
        
        Returns:
            Estrutura: {"coluna_1": {"pares": count, "impares": count}, ...}
        """
        resultados = self.modelo.buscar_todos()
        
        distribuicao = {}
        for coluna in range(1, SuperSeteConfig.TOTAL_COLUNAS + 1):
            distribuicao[f'coluna_{coluna}'] = {'pares': 0, 'impares': 0}
        
        for resultado in resultados:
            for coluna in range(1, SuperSeteConfig.TOTAL_COLUNAS + 1):
                numero = resultado.get(f'coluna_{coluna}')
                if numero is not None:
                    if numero % 2 == 0:
                        distribuicao[f'coluna_{coluna}']['pares'] += 1
                    else:
                        distribuicao[f'coluna_{coluna}']['impares'] += 1
        
        return distribuicao
    
    def calcular_sequencias_comuns(self, top: int = 10) -> List[Dict]:
        """
        Identifica padrões de sequências que aparecem frequentemente.
        Exemplo: quantas vezes apareceu [5, 0, 2, 3, 9, 8, 1]
        
        Args:
            top: Quantidade de sequências a retornar
            
        Returns:
            Lista de dicionários com as sequências mais comuns
        """
        resultados = self.modelo.buscar_todos()
        
        sequencias = defaultdict(int)
        for resultado in resultados:
            sequencia = tuple([
                resultado.get(f'coluna_{i}') 
                for i in range(1, SuperSeteConfig.TOTAL_COLUNAS + 1)
            ])
            sequencias[sequencia] += 1
        
        # Ordenar por frequência
        sequencias_ordenadas = sorted(
            sequencias.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Formatar resultado
        resultado = []
        for sequencia, freq in sequencias_ordenadas[:top]:
            resultado.append({
                'sequencia': list(sequencia),
                'frequencia': freq
            })
        
        return resultado
    
    def calcular_estatisticas_completas(self) -> Dict:
        """
        Calcula todas as estatísticas disponíveis.
        
        Returns:
            Dicionário com todas as estatísticas
        """
        total_concursos = self.modelo.contar_resultados()
        
        return {
            'total_concursos': total_concursos,
            'frequencia_por_coluna': self.calcular_frequencia_por_coluna(),
            'atrasos_por_coluna': self.calcular_atrasos_por_coluna(),
            'mais_frequentes_por_coluna': self.calcular_numeros_mais_frequentes_por_coluna(),
            'mais_atrasados_por_coluna': self.calcular_numeros_mais_atrasados_por_coluna(),
            'pares_impares_por_coluna': self.calcular_pares_impares_por_coluna(),
            'sequencias_comuns': self.calcular_sequencias_comuns()
        }
    
    def calcular_estatisticas_coluna(self, numero_coluna: int) -> Dict:
        """
        Calcula estatísticas específicas de uma coluna.
        
        Args:
            numero_coluna: Número da coluna (1-7)
            
        Returns:
            Dicionário com estatísticas da coluna
        """
        if numero_coluna < 1 or numero_coluna > SuperSeteConfig.TOTAL_COLUNAS:
            return {'erro': 'Número de coluna inválido'}
        
        coluna_nome = f'coluna_{numero_coluna}'
        
        frequencias = self.calcular_frequencia_por_coluna()
        atrasos = self.calcular_atrasos_por_coluna()
        pares_impares = self.calcular_pares_impares_por_coluna()
        mais_frequentes = self.calcular_numeros_mais_frequentes_por_coluna()
        mais_atrasados = self.calcular_numeros_mais_atrasados_por_coluna()
        
        return {
            'coluna': numero_coluna,
            'frequencias': frequencias.get(coluna_nome, {}),
            'atrasos': atrasos.get(coluna_nome, {}),
            'pares_impares': pares_impares.get(coluna_nome, {}),
            'mais_frequentes': mais_frequentes.get(coluna_nome, []),
            'mais_atrasados': mais_atrasados.get(coluna_nome, [])
        }
