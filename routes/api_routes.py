"""
Rotas da API REST.
"""
from flask import Blueprint, request, jsonify
from models.resultado_model import ResultadoModel
from services.api_caixa_service import ApiCaixaService
from services.estatistica_service import EstatisticaService
from services.supersete_service import SuperSeteService

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Inicializar serviços
modelo_resultado = ResultadoModel()
api_caixa_service = ApiCaixaService()
estatistica_service = EstatisticaService(modelo_resultado)
supersete_service = SuperSeteService(estatistica_service)


@api_bp.route('/atualizar', methods=['POST'])
def atualizar():
    """
    Atualiza a base de dados com os últimos concursos da API da Caixa.
    
    Returns:
        JSON com estatísticas da atualização
    """
    try:
        resultado = api_caixa_service.atualizar_base_completa(modelo_resultado)
        return jsonify({
            'sucesso': True,
            'dados': resultado
        }), 200
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'erro': str(e)
        }), 500


@api_bp.route('/ultimo-resultado', methods=['GET'])
def ultimo_resultado():
    """
    Retorna o último resultado cadastrado no banco.
    
    Returns:
        JSON com os dados do último resultado
    """
    try:
        resultado = modelo_resultado.buscar_ultimo()
        if resultado:
            return jsonify({
                'sucesso': True,
                'dados': resultado
            }), 200
        else:
            return jsonify({
                'sucesso': False,
                'mensagem': 'Nenhum resultado encontrado. Execute /api/atualizar primeiro.'
            }), 404
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'erro': str(e)
        }), 500


@api_bp.route('/resultados', methods=['GET'])
def resultados():
    """
    Retorna lista de resultados com paginação opcional.
    
    Query params:
        limite: Número máximo de resultados a retornar
    
    Returns:
        JSON com lista de resultados
    """
    try:
        limite = request.args.get('limite', type=int)
        resultados = modelo_resultado.buscar_todos(limite=limite)
        
        return jsonify({
            'sucesso': True,
            'total': len(resultados),
            'dados': resultados
        }), 200
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'erro': str(e)
        }), 500


@api_bp.route('/resultado/<int:numero>', methods=['GET'])
def resultado_especifico(numero):
    """
    Busca um concurso específico pelo número.
    
    Args:
        numero: Número do concurso
    
    Returns:
        JSON com os dados do concurso
    """
    try:
        resultado = modelo_resultado.buscar_por_numero(numero)
        if resultado:
            return jsonify({
                'sucesso': True,
                'dados': resultado
            }), 200
        else:
            return jsonify({
                'sucesso': False,
                'mensagem': f'Concurso {numero} não encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'erro': str(e)
        }), 500


@api_bp.route('/estatisticas', methods=['GET'])
def estatisticas():
    """
    Retorna todas as estatísticas calculadas.
    
    Returns:
        JSON com estatísticas completas
    """
    try:
        stats = estatistica_service.calcular_estatisticas_completas()
        return jsonify({
            'sucesso': True,
            'dados': stats
        }), 200
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'erro': str(e)
        }), 500


@api_bp.route('/estatisticas/coluna/<int:coluna>', methods=['GET'])
def estatisticas_coluna(coluna):
    """
    Retorna estatísticas de uma coluna específica.
    
    Args:
        coluna: Número da coluna (1-7)
    
    Returns:
        JSON com estatísticas da coluna
    """
    try:
        stats = estatistica_service.calcular_estatisticas_coluna(coluna)
        
        if 'erro' in stats:
            return jsonify({
                'sucesso': False,
                'erro': stats['erro']
            }), 400
        
        return jsonify({
            'sucesso': True,
            'dados': stats
        }), 200
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'erro': str(e)
        }), 500


@api_bp.route('/gerar-palpite', methods=['POST'])
def gerar_palpite():
    """
    Gera palpites baseados na estratégia escolhida.
    
    Body JSON:
        estrategia: Nome da estratégia (padrão: equilibrada)
        quantidade_jogos: Quantidade de jogos a gerar (padrão: 1)
        estrategias_por_coluna: Opcional, dicionário com estratégias por coluna
    
    Returns:
        JSON com os palpites gerados
    """
    try:
        dados = request.get_json() or {}
        estrategia = dados.get('estrategia', 'equilibrada')
        quantidade_jogos = dados.get('quantidade_jogos', 1)
        estrategias_por_coluna = dados.get('estrategias_por_coluna')
        
        # Validar quantidade
        if quantidade_jogos < 1 or quantidade_jogos > 100:
            return jsonify({
                'sucesso': False,
                'erro': 'Quantidade de jogos deve estar entre 1 e 100'
            }), 400
        
        palpites = supersete_service.gerar_palpite(
            estrategia=estrategia,
            quantidade_jogos=quantidade_jogos,
            estrategias_por_coluna=estrategias_por_coluna
        )
        
        return jsonify({
            'sucesso': True,
            'estrategia': estrategia,
            'quantidade': len(palpites),
            'palpites': palpites
        }), 200
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'erro': str(e)
        }), 500


@api_bp.route('/conferir', methods=['POST'])
def conferir():
    """
    Confere um palpite com um resultado oficial.
    
    Body JSON:
        palpite: Lista com 7 números
        numero_concurso: Número do concurso a conferir (opcional, usa o último se não informado)
    
    Returns:
        JSON com informações sobre acertos
    """
    try:
        dados = request.get_json()
        if not dados or 'palpite' not in dados:
            return jsonify({
                'sucesso': False,
                'erro': 'Palpite não informado'
            }), 400
        
        palpite = dados['palpite']
        numero_concurso = dados.get('numero_concurso')
        
        # Buscar resultado
        if numero_concurso:
            resultado = modelo_resultado.buscar_por_numero(numero_concurso)
        else:
            resultado = modelo_resultado.buscar_ultimo()
        
        if not resultado:
            return jsonify({
                'sucesso': False,
                'erro': 'Resultado não encontrado'
            }), 404
        
        # Conferir palpite
        conferencia = supersete_service.conferir_palpite(palpite, resultado)
        
        if 'erro' in conferencia:
            return jsonify({
                'sucesso': False,
                'erro': conferencia['erro']
            }), 400
        
        return jsonify({
            'sucesso': True,
            'concurso': resultado['numero'],
            'data': resultado['data_apuracao'],
            'conferencia': conferencia
        }), 200
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'erro': str(e)
        }), 500
