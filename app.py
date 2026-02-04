"""
Arquivo principal da aplicação Flask
Site de Agendamento de Consultas Nutricionistas
Projeto Acadêmico - Programação Web 1
"""
from app import criar_app

# Criar a aplicação usando a factory function
app = criar_app()

if __name__ == '__main__':
    # Rodar a aplicação em modo debug
    app.run(debug=True, host='0.0.0.0', port=5000)
