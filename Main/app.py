from flask import Flask, render_template, redirect, url_for, request, jsonify, session, flash
import mysql.connector
from authlib.integrations.flask_client import OAuth
from os import environ as env
from dotenv import find_dotenv, load_dotenv
from urllib.parse import quote_plus, urlencode

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)
oauth.register(
    name = 'google',
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)


def get_carros():
    conn = mysql.connector.connect(
        host=env.get("MYSQL_HOST"),
        port=env.get("MYSQL_PORT"),
        user=env.get("MYSQL_USER"),
        password=env.get("MYSQL_PASSWORD"),
        database=env.get("MYSQL_DATABASE")
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

@app.route("/cadastro")
def cadastro():
    return redirect(url_for("login"))

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = oauth.google.authorize_access_token()
    #print(token['userinfo'])
    session['user'] = token['userinfo']
    return redirect(url_for('questionario'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("start", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
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
    if "recomendacoes" in session:
        top_5 = session.get('recomendacoes')

        if not top_5 or len(top_5) < 1:
            return redirect(url_for('questionario'))

        return render_template('recomendacao.html',
                            carro_principal=top_5[0],
                            outros_carros=top_5[1:])
    else:
        return redirect(url_for("questionario"))


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