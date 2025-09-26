import os
from flask import Flask, render_template
from authlib.integrations.flask_client import OAuth
from urllib.parse import quote_plus, urlencode
from dotenv import find_dotenv, load_dotenv

# Carrega as variáveis de ambiente no início
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# Inicializa as extensões FORA da função fábrica
# Isso evita problemas de importação circular depois
oauth = OAuth()

def create_app():
    """
    Função que cria e configura a instância da aplicação Flask.
    """
    app = Flask(__name__, instance_relative_config=True)

    # --- 1. CONFIGURAÇÃO CENTRALIZADA ---
    # Carrega todas as configurações importantes para o app.config
    app.config.from_mapping(
        SECRET_KEY=os.getenv("APP_SECRET_KEY"),
        AUTH0_DOMAIN=os.getenv("AUTH0_DOMAIN"),
        AUTH0_CLIENT_ID=os.getenv("AUTH0_CLIENT_ID"),
        AUTH0_CLIENT_SECRET=os.getenv("AUTH0_CLIENT_SECRET"),
        M2M_CLIENT_ID=os.getenv("M2M_CLIENT_ID"),
        M2M_CLIENT_SECRET=os.getenv("M2M_CLIENT_SECRET"),
        REDIRECT_SECRET=os.getenv("REDIRECT_SECRET")
    )

    # --- 2. INICIALIZAÇÃO DE EXTENSÕES ---
    # Conecta as extensões (como o OAuth) à instância do app
    oauth.init_app(app)
    
    # Registra o provedor OAuth (Auth0/Google)
    oauth.register(
        name='auth0_google', # Renomeado para clareza
        client_id=app.config.get("AUTH0_CLIENT_ID"),
        client_secret=app.config.get("AUTH0_CLIENT_SECRET"),
        client_kwargs={
            "scope": "openid profile email",
        },
        server_metadata_url=f'https://{app.config.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
    )

    # --- 3. REGISTRO DOS BLUEPRINTS ---
    # Importa e registra os "mini-aplicativos" (nossas rotas)
    with app.app_context():
        # Importamos os blueprints aqui para evitar importações circulares
        from . import main, auth, api

        app.register_blueprint(main.bp)
        app.register_blueprint(auth.bp)
        app.register_blueprint(api.bp)

    # --- 4. REGISTRO DE ERROR HANDLERS ---
    # Define o que fazer em caso de erros específicos, como 404
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    # Retorna a aplicação montada e pronta para ser executada
    return app