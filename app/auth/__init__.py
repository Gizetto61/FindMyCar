from flask import Blueprint

# Cria a instância do Blueprint para as rotas de autenticação
bp = Blueprint('auth', __name__)

# Importa as rotas no final para conectar as view functions
from app.auth import routes