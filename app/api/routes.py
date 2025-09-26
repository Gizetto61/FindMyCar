# app/api/routes.py (versão final e refatorada)

from flask import request, jsonify, session
from app.api import bp

# Importa as funções de lógica de negócio dos seus respectivos módulos
from app.core.database import get_carros
from app.core.recommendation import calculate_recommendations

@bp.route('/recomendar', methods=['POST'])
def recomendar_api():
    dados = request.json
    
    pesos = {
        'conforto': dados['conforto'],
        'consumo': dados['consumo'],
        'espaco': dados['tamanho'], # 'espaco' é o nome da chave nos pesos
        'preco': dados['preco'],
        'manutencao': dados['manutencao']
    }

    # Passo 1: Busca os dados
    carros = get_carros()
    
    # Passo 2: Executa a lógica de negócio
    top_5_recomendados = calculate_recommendations(carros, pesos)

    # Passo 3: Salva o resultado na sessão
    session['recomendacoes'] = top_5_recomendados

    return jsonify({'status': 'ok'})