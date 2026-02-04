"""
Módulo de inicialização da aplicação Flask
"""
from flask import Flask

def criar_app():
    """
    Factory function para criar e configurar a aplicação Flask
    """
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    # Configuração da secret key para sessões
    app.config['SECRET_KEY'] = 'nutri_secret_key_2024_programacao_web'
    
    # Importar e registrar as rotas
    from app.routes import registrar_rotas
    registrar_rotas(app)
    
    return app
