# app/auth/routes.py

from flask import render_template, redirect, url_for, request, jsonify, session, flash, abort, current_app
from urllib.parse import quote_plus, urlencode
import requests
import jwt

from app.auth import bp
from app import oauth

# Importa as funções do nosso novo módulo de serviço
from app.services.auth0_service import create_password_change_ticket, resend_verification_email
from app.core.database import get_user_by_email

# --- Rotas de Login, Cadastro e Callback ---

@bp.route('/login')
def login():
    if 'user' in session:
        return redirect(url_for("main.perfil"))
        
    # Usando o nome que demos ao provedor no __init__.py principal
    return oauth.auth0_google.authorize_redirect(
        redirect_uri=url_for('auth.authorize', _external=True)
    )

@bp.route("/signup")
def signup():
    return oauth.auth0_google.authorize_redirect(
        redirect_uri=url_for('auth.authorize', _external=True),
        screen_hint='signup'
    )

@bp.route('/authorize')
def authorize():
    if request.args.get("error"):
        flash("Acesso negado.", "error")
        return redirect(url_for("main.start"))

    try:
        token = oauth.auth0_google.authorize_access_token()
        user_info_from_auth0 = token['userinfo']
        user_email = user_info_from_auth0.get('email')

        if not user_email:
            flash("Não foi possível obter o e-mail do seu perfil. Tente novamente.", "error")

        user_from_db = get_user_by_email(user_email)
        if not user_from_db:
            # Este erro pode acontecer se a sua Action no Auth0 falhar ao criar o usuário.
            flash("Seu perfil não foi encontrado em nosso sistema. Tente se cadastrar novamente.", "error")
            return redirect(url_for("main.start"))
        session['user'] = user_info_from_auth0
        session['user_db_id'] = user_from_db['id']    
        print(f"Login bem-sucedido! E-mail: {user_email}, ID do Banco: {session['user_db_id']}")

        return redirect(url_for('main.questionario'))
    except Exception as e:  
        flash(f"Erro durante a autenticação: {e}", "error")
        return redirect(url_for("main.start"))

@bp.route("/logout")
def logout():
    session.clear()
    # Usando app.config para pegar as variáveis
    domain = f"https://{current_app.config['AUTH0_DOMAIN']}"
    client_id = oauth.auth0_google.client_id
    
    return redirect(
        f"{domain}/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("main.start", _external=True),
                "client_id": client_id,
            },
            quote_via=quote_plus,
        )
    )

# --- Rotas de Gerenciamento de Conta ---

@bp.route("/perfil/alterar-senha")
def change_password():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user'].get('sub')
    if not user_id:
        abort(401)
    
    # A rota agora é muito mais limpa. Ela apenas chama o serviço.
    try:
        ticket_url = create_password_change_ticket(user_id)
        return redirect(ticket_url, code=302)
    except ConnectionError as e:
        flash(f"Erro de comunicação ao tentar alterar a senha. Tente novamente mais tarde.", "error")
        return redirect(url_for("main.perfil"))

@bp.route("/pwd-changed")
def password_changed():
    flash("Senha atualizada com sucesso.")
    return redirect(url_for("main.perfil"))

@bp.route("/verify-email")
def verify_email():
    return render_template("auth/verify_email.html") # Supondo que o template esteja em templates/auth/

@bp.route("/api/auth0/resend-verification", methods=['POST'])
def resend_verification():
    # 1. Obter o token da requisição (lógica original)
    data = request.get_json(silent=True) or {}
    session_token = data.get("session_token")
    if not session_token:
        return jsonify(error="missing_session_token"), 400

    # 2. Validar o token JWT para extrair o user_id (lógica original)
    try:
        # Busca a chave secreta da configuração centralizada do app
        secret = current_app.config.get('REDIRECT_SECRET')
        payload = jwt.decode(session_token, secret, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return jsonify(error="invalid_session_token"), 401

    user_id = payload.get("user_id")
    if not user_id:
        return jsonify(error="missing_user_id"), 400

    # 3. Chamar o nosso novo serviço para fazer o trabalho pesado
    try:
        response_data = resend_verification_email(user_id)
        return jsonify(response_data), 200 # Sucesso
    except ConnectionError as e:
        # Se o nosso serviço falhar ao se conectar com o Auth0
        return jsonify(error="service_communication_error", detail=str(e)), 502