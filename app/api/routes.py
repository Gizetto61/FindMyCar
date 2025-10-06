# app/api/routes.py (versão final e refatorada)

from flask import request, jsonify, session, abort
from app.api import bp

# Importa as funções de lógica de negócio dos seus respectivos módulos
from app.core.database import get_db_connection, create_anuncio, add_imagem_to_anuncio, get_user_phone_by_id, get_carros_com_avaliacoes
from app.core.recommendation import calculate_recommendations

@bp.route('/recomendar', methods=['POST'])
def recomendar_api():
    dados = request.json
    pesos = dados
    
    carros = get_carros_com_avaliacoes()
    top_5_recomendados = calculate_recommendations(carros, pesos)

    ids_dos_recomendados = [carro['id'] for carro in top_5_recomendados]
    session['recomendacoes_ids'] = ids_dos_recomendados

    return jsonify({'status': 'ok'})

@bp.route('/anunciar', methods=['POST'])
def criar_anuncio():
    # 1. Proteção da Rota: Garante que o usuário está logado
    if 'user' not in session:
        return jsonify(error="Autenticação necessária."), 401

    # 2. Recebimento dos Dados
    data = request.get_json()
    if not data:
        return jsonify(error="Requisição sem dados JSON."), 400

    # Pega o ID do usuário da sessão (ID do seu banco, não do Auth0)
    # Você precisará salvar isso na sessão durante o login.
    user_id = session.get('user_db_id')
    if not user_id:
        return jsonify(error="ID de usuário não encontrado na sessão."), 401

    # 3. Lógica do Telefone
    if data.get('telefone') == 'usar_perfil':
        phone = get_user_phone_by_id(user_id)
        if not phone:
            return jsonify(error="Telefone não encontrado no perfil do usuário."), 400
        data['telefone'] = phone
    
    # 4. Transação do Banco de Dados
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Inicia a transação
        conn.start_transaction()

        # Insere o anúncio principal e pega seu ID
        novo_anuncio_id = create_anuncio(cursor, data, user_id)

        # Itera sobre as imagens e insere cada uma
        imagens = data.get('imagens', [])
        if not imagens:
            raise ValueError("Pelo menos uma imagem é necessária.")
            
        for i, base64_img in enumerate(imagens):
            add_imagem_to_anuncio(cursor, novo_anuncio_id, base64_img)
        
        # Se tudo deu certo, salva as alterações permanentemente
        conn.commit()

        # 5. Retorno de Sucesso
        return jsonify(success=True, message="Anúncio criado com sucesso!", anuncio_id=novo_anuncio_id), 201

    except Exception as e:
        # Se qualquer passo falhar, desfaz todas as operações
        if conn:
            conn.rollback()
        print(f"Erro ao criar anúncio: {e}") # Logar o erro é importante
        return jsonify(error="Ocorreu um erro interno ao criar o anúncio.", detail=str(e)), 500
    
    finally:
        # Garante que a conexão seja sempre fechada
        if conn and conn.is_connected():
            cursor.close()
            conn.close()