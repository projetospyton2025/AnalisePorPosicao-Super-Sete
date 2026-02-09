"""
Serviço para geração de palpites da Super Sete.
"""
import random
from typing import List, Dict
from config import SuperSeteConfig


class SuperSeteService:
    """
    Serviço para geração de palpites inteligentes baseados em estatísticas.
    """
    
    def __init__(self, estatistica_service):
        """
        Inicializa o serviço com o serviço de estatísticas.
        
        Args:
            estatistica_service: Instância do EstatisticaService
        """
        self.estatistica_service = estatistica_service
    
    def gerar_palpite(self, estrategia: str = 'equilibrada', 
                      quantidade_jogos: int = 1,
                      estrategias_por_coluna: Dict = None) -> List[List[int]]:
        """
        Gera palpites baseados na estratégia escolhida.
        
        Args:
            estrategia: Estratégia a usar (equilibrada, agressiva, etc.)
            quantidade_jogos: Quantidade de jogos a gerar
            estrategias_por_coluna: Dicionário com estratégias específicas por coluna
                                   Ex: {"coluna_1": "agressiva", "coluna_2": "conservadora"}
            
        Returns:
            Lista de palpites (cada palpite é uma lista de 7 números)
        """
        palpites = []
        
        for _ in range(quantidade_jogos):
            if estrategias_por_coluna:
                palpite = self._gerar_palpite_personalizado(estrategias_por_coluna)
            else:
                palpite = self._gerar_palpite_por_estrategia(estrategia)
            palpites.append(palpite)
        
        return palpites
    
    def _gerar_palpite_por_estrategia(self, estrategia: str) -> List[int]:
        """
        Gera um único palpite baseado na estratégia.
        
        Args:
            estrategia: Nome da estratégia
            
        Returns:
            Lista com 7 números (um por coluna)
        """
        if estrategia == 'equilibrada':
            return self._estrategia_equilibrada()
        elif estrategia == 'agressiva':
            return self._estrategia_agressiva()
        elif estrategia == 'conservadora':
            return self._estrategia_conservadora()
        elif estrategia == 'mista':
            return self._estrategia_mista()
        elif estrategia == 'atrasados':
            return self._estrategia_atrasados()
        elif estrategia == 'aleatorio_inteligente':
            return self._estrategia_aleatorio_inteligente()
        else:
            # Padrão: equilibrada
            return self._estrategia_equilibrada()
    
    def _gerar_palpite_personalizado(self, estrategias_por_coluna: Dict) -> List[int]:
        """
        Gera um palpite com estratégias diferentes para cada coluna.
        
        Args:
            estrategias_por_coluna: Dicionário com estratégias por coluna
            
        Returns:
            Lista com 7 números
        """
        palpite = []
        
        for coluna in range(1, SuperSeteConfig.TOTAL_COLUNAS + 1):
            coluna_nome = f'coluna_{coluna}'
            estrategia = estrategias_por_coluna.get(coluna_nome, 'equilibrada')
            
            # Gerar número para esta coluna usando a estratégia específica
            numero = self._gerar_numero_coluna(coluna, estrategia)
            palpite.append(numero)
        
        return palpite
    
    def _gerar_numero_coluna(self, coluna: int, estrategia: str) -> int:
        """
        Gera um número para uma coluna específica usando uma estratégia.
        
        Args:
            coluna: Número da coluna (1-7)
            estrategia: Nome da estratégia
            
        Returns:
            Número de 0 a 9
        """
        coluna_nome = f'coluna_{coluna}'
        
        if estrategia == 'agressiva':
            # Prioriza números frequentes
            mais_frequentes = self.estatistica_service.calcular_numeros_mais_frequentes_por_coluna(top=5)
            candidatos = [int(num) for num, _ in mais_frequentes.get(coluna_nome, [])]
            return random.choice(candidatos) if candidatos else random.randint(0, 9)
            
        elif estrategia == 'conservadora':
            # Prioriza números atrasados
            mais_atrasados = self.estatistica_service.calcular_numeros_mais_atrasados_por_coluna(top=5)
            candidatos = [int(num) for num, _ in mais_atrasados.get(coluna_nome, [])]
            return random.choice(candidatos) if candidatos else random.randint(0, 9)
            
        elif estrategia == 'atrasados':
            # Apenas números atrasados
            mais_atrasados = self.estatistica_service.calcular_numeros_mais_atrasados_por_coluna(top=3)
            candidatos = [int(num) for num, _ in mais_atrasados.get(coluna_nome, [])]
            return random.choice(candidatos) if candidatos else random.randint(0, 9)
            
        else:
            # Equilibrada ou padrão
            frequencias = self.estatistica_service.calcular_frequencia_por_coluna()
            freq_coluna = frequencias.get(coluna_nome, {})
            
            if freq_coluna:
                # Usar frequências como pesos
                numeros = list(range(10))
                pesos = [freq_coluna.get(str(n), 1) for n in numeros]
                # Check if all weights are zero (empty database)
                if sum(pesos) > 0:
                    return random.choices(numeros, weights=pesos, k=1)[0]
                else:
                    return random.randint(0, 9)
            else:
                return random.randint(0, 9)
    
    def _estrategia_equilibrada(self) -> List[int]:
        """
        Estratégia equilibrada: mix de números frequentes e atrasados.
        
        Returns:
            Lista com 7 números
        """
        palpite = []
        mais_frequentes = self.estatistica_service.calcular_numeros_mais_frequentes_por_coluna(top=5)
        mais_atrasados = self.estatistica_service.calcular_numeros_mais_atrasados_por_coluna(top=5)
        
        for coluna in range(1, SuperSeteConfig.TOTAL_COLUNAS + 1):
            coluna_nome = f'coluna_{coluna}'
            
            # 50% de chance de escolher um número frequente ou atrasado
            if random.random() < 0.5:
                candidatos = [int(num) for num, _ in mais_frequentes.get(coluna_nome, [])]
            else:
                candidatos = [int(num) for num, _ in mais_atrasados.get(coluna_nome, [])]
            
            numero = random.choice(candidatos) if candidatos else random.randint(0, 9)
            palpite.append(numero)
        
        return palpite
    
    def _estrategia_agressiva(self) -> List[int]:
        """
        Estratégia agressiva: prioriza números mais frequentes.
        
        Returns:
            Lista com 7 números
        """
        palpite = []
        mais_frequentes = self.estatistica_service.calcular_numeros_mais_frequentes_por_coluna(top=5)
        
        for coluna in range(1, SuperSeteConfig.TOTAL_COLUNAS + 1):
            coluna_nome = f'coluna_{coluna}'
            candidatos = [int(num) for num, _ in mais_frequentes.get(coluna_nome, [])]
            numero = random.choice(candidatos) if candidatos else random.randint(0, 9)
            palpite.append(numero)
        
        return palpite
    
    def _estrategia_conservadora(self) -> List[int]:
        """
        Estratégia conservadora: prioriza números atrasados.
        
        Returns:
            Lista com 7 números
        """
        palpite = []
        mais_atrasados = self.estatistica_service.calcular_numeros_mais_atrasados_por_coluna(top=5)
        
        for coluna in range(1, SuperSeteConfig.TOTAL_COLUNAS + 1):
            coluna_nome = f'coluna_{coluna}'
            candidatos = [int(num) for num, _ in mais_atrasados.get(coluna_nome, [])]
            numero = random.choice(candidatos) if candidatos else random.randint(0, 9)
            palpite.append(numero)
        
        return palpite
    
    def _estrategia_mista(self) -> List[int]:
        """
        Estratégia mista: alterna entre diferentes estratégias por coluna.
        
        Returns:
            Lista com 7 números
        """
        estrategias = ['agressiva', 'conservadora', 'equilibrada']
        palpite = []
        
        for coluna in range(1, SuperSeteConfig.TOTAL_COLUNAS + 1):
            estrategia = random.choice(estrategias)
            numero = self._gerar_numero_coluna(coluna, estrategia)
            palpite.append(numero)
        
        return palpite
    
    def _estrategia_atrasados(self) -> List[int]:
        """
        Estratégia focada em números com maior atraso.
        
        Returns:
            Lista com 7 números
        """
        palpite = []
        mais_atrasados = self.estatistica_service.calcular_numeros_mais_atrasados_por_coluna(top=3)
        
        for coluna in range(1, SuperSeteConfig.TOTAL_COLUNAS + 1):
            coluna_nome = f'coluna_{coluna}'
            candidatos = [int(num) for num, _ in mais_atrasados.get(coluna_nome, [])]
            numero = random.choice(candidatos) if candidatos else random.randint(0, 9)
            palpite.append(numero)
        
        return palpite
    
    def _estrategia_aleatorio_inteligente(self) -> List[int]:
        """
        Estratégia aleatória com pesos baseados em frequência.
        
        Returns:
            Lista com 7 números
        """
        palpite = []
        frequencias = self.estatistica_service.calcular_frequencia_por_coluna()
        
        for coluna in range(1, SuperSeteConfig.TOTAL_COLUNAS + 1):
            coluna_nome = f'coluna_{coluna}'
            freq_coluna = frequencias.get(coluna_nome, {})
            
            if freq_coluna:
                numeros = list(range(10))
                pesos = [freq_coluna.get(str(n), 1) for n in numeros]
                # Check if all weights are zero (empty database)
                if sum(pesos) > 0:
                    numero = random.choices(numeros, weights=pesos, k=1)[0]
                else:
                    numero = random.randint(0, 9)
            else:
                numero = random.randint(0, 9)
            
            palpite.append(numero)
        
        return palpite
    
    def conferir_palpite(self, palpite: List[int], resultado: Dict) -> Dict:
        """
        Confere um palpite com um resultado oficial.
        
        Args:
            palpite: Lista com 7 números do palpite
            resultado: Dicionário com o resultado oficial
            
        Returns:
            Dicionário com informações sobre acertos
        """
        if len(palpite) != SuperSeteConfig.TOTAL_COLUNAS:
            return {'erro': 'Palpite deve conter 7 números'}
        
        acertos = 0
        detalhes = []
        
        for coluna in range(1, SuperSeteConfig.TOTAL_COLUNAS + 1):
            numero_palpite = palpite[coluna - 1]
            numero_resultado = resultado.get(f'coluna_{coluna}')
            
            acertou = numero_palpite == numero_resultado
            if acertou:
                acertos += 1
            
            detalhes.append({
                'coluna': coluna,
                'palpite': numero_palpite,
                'resultado': numero_resultado,
                'acertou': acertou
            })
        
        # Determinar faixa de premiação
        faixa = None
        if acertos >= 3:
            faixa = 8 - acertos  # 7 acertos = faixa 1, 6 = faixa 2, etc.
        
        return {
            'total_acertos': acertos,
            'faixa_premiacao': faixa,
            'detalhes': detalhes
        }
