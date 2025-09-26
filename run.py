# run.py

from app import create_app

# Chama a função fábrica para criar a instância da aplicação
app = create_app()

# Bloco padrão para executar a aplicação quando o script é chamado diretamente
if __name__ == "__main__":
    # Inicia o servidor de desenvolvimento do Flask
    app.run(debug=True)