from flask import Blueprint

# Cria uma instância de Blueprint.
# 'main' é o nome do Blueprint.
# __name__ ajuda o Flask a localizar o Blueprint.
bp = Blueprint('main', __name__)

# Importamos as rotas no final para evitar importações circulares.
# Isso conecta as rotas definidas em routes.py a este Blueprint.
from app.main import routes