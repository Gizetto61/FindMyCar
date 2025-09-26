from flask import Blueprint

# Define o Blueprint 'api' e adiciona um prefixo de URL a todas as suas rotas.
bp = Blueprint('api', __name__, url_prefix='/api')

# Importa o arquivo de rotas para conectá-lo ao Blueprint.
from app.api import routes