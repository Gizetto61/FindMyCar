from flask import Flask, render_template, redirect, url_for, request, jsonify, session, flash, abort
import mysql.connector
from authlib.integrations.flask_client import OAuth
import os
import requests, jwt
from dotenv import find_dotenv, load_dotenv
from urllib.parse import quote_plus, urlencode


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
    
from m2m_auth0 import get_management_token

AUTH0_DOMAIN   = os.getenv("AUTH0_DOMAIN")
REDIRECT_SECRET = os.getenv("REDIRECT_SECRET")

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")

oauth = OAuth(app)
oauth.register(
    name = 'google',
    client_id=os.getenv("AUTH0_CLIENT_ID"),
    client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{AUTH0_DOMAIN}/.well-known/openid-configuration'
)

@app.get("/verify-email")
def verify_email():
    return render_template("verify_email.html")

@app.post("/api/auth0/resend-verification")
def resend_verification():
    data = request.get_json(silent=True) or {}
    session_token = data.get("session_token")
    if not session_token:
        return jsonify(error="missing_session_token"), 400

    # valida token assinado pela Action
    try:
        payload = jwt.decode(session_token, REDIRECT_SECRET, algorithms=["HS256"])
    except Exception:
        return jsonify(error="invalid_session_token"), 401

    user_id = payload.get("user_id")
    if not user_id:
        return jsonify(error="missing_user_id"), 400

    # token M2M
    try:
        token = get_management_token()
    except Exception as e:
        return jsonify(error="m2m_token_error", detail=str(e)), 502

    # chama Management API
    try:
        r = requests.post(
            f"https://{AUTH0_DOMAIN}/api/v2/jobs/verification-email",
            json={"user_id": user_id},
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            timeout=10
        )
        # propaga a resposta da Management API em JSON
        # (se não for JSON, devolve texto mesmo)
        try:
            body = r.json()
            return jsonify(body), r.status_code
        except ValueError:
            return (r.text, r.status_code, {"Content-Type": "application/json"})
    except requests.RequestException as e:
        return jsonify(error="auth0_request_failed", detail=str(e)), 502



def get_carros():
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=os.getenv("MYSQL_PORT"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Carro")
    carros = cursor.fetchall()
    cursor.close()
    conn.close()
    return carros


@app.route("/homepage")
def homepage():
    return redirect(url_for("start"))

@app.route("/home")
def home():
    return redirect(url_for("homepage"))

@app.route("/")
def start():
    return render_template("homepage.html")

@app.route("/signup")
def signup():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri, screen_hint='signup')

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    # Se o Auth0 negou o login, vem com ?error=access_denied
    if request.args.get("error"):
        return "<h1>Erro!</h1>"  # sua homepage "/"

    # Se não há erro, processa normalmente
    token = oauth.google.authorize_access_token()
    session['user'] = token['userinfo']
    return redirect(url_for('questionario'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + os.getenv("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("start", _external=True),
                "client_id": os.getenv("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/questionario", methods=['GET', 'POST'])
def questionario():
    if 'user' in session:
        return render_template("questionario.html")
    return redirect(url_for("login"))


@app.route('/recomendacao')
def recomendacao():
    if 'user' in session:
        if "recomendacoes" in session:
            top_5 = session.get('recomendacoes')

            if not top_5 or len(top_5) < 1:
                return redirect(url_for('questionario'))

            return render_template('recomendacao.html',
                                carro_principal=top_5[0],
                                outros_carros=top_5[1:])
        else:
            return redirect(url_for("questionario"))
    return(redirect(url_for("login")))


@app.route('/logout/questionario')
def logout_questionario():
    if "recomendacoes" in session:
        session.pop("recomendacoes", None)
        flash(f"Realize o questionário antes de ver as recomendações", "info")
    

    return redirect(url_for("questionario"))

@app.route('/api/recomendar', methods=['POST'])
def recomendar_api():
    dados = request.json

    pesos = {
        'conforto': dados['conforto'],
        'consumo': dados['consumo'],
        'espaco': dados['tamanho'],
        'preco': dados['preco'],
        'manutencao': dados['manutencao']
    }

    carros = get_carros()
    resultados = []

    for carro in carros:
        score = 0
        for chave, preferencia in pesos.items():
            valor_carro = carro.get(chave.capitalize())
            if valor_carro is None:
                continue
            proximidade = 1 - abs(preferencia - int(valor_carro)) / 4
            score += proximidade

        resultados.append({'carro': carro, 'score': score})

    top_5 = sorted(resultados, key=lambda x: x['score'], reverse=True)[:5]

    # Salva somente os dados dos carros, sem score
    session['recomendacoes'] = [r['carro'] for r in top_5]

    return jsonify({'status': 'ok'})


if __name__ == "__main__":
    app.run(debug=True)