"""
Aplicação Flask principal do sistema de análise Super Sete.
"""
from flask import Flask
from config import Config
from routes.main_routes import main_bp
from routes.api_routes import api_bp


def create_app():
    """
    Factory function para criar a aplicação Flask.
    
    Returns:
        Instância configurada da aplicação Flask
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Registrar blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    
    return app


if __name__ == '__main__':
    app = create_app()
    print(f"🚀 Iniciando servidor Super Sete na porta {Config.PORT}")
    print(f"📊 Acesse: http://{Config.HOST}:{Config.PORT}")
    print(f"📖 API Docs: http://{Config.HOST}:{Config.PORT}/api/estatisticas")
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
