from flask import Flask, render_template, redirect, url_for, request, jsonify, session, flash
import mysql.connector

app = Flask(__name__)

app.secret_key = 'rochakkj.'


def get_carros():
    conn = mysql.connector.connect(
        host="switchyard.proxy.rlwy.net",
        port=41357,
        user="root",
        password="EHnlBexYxFZuogtSOZHuvNloklbjNFqt",
        database="railway"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Carro")
    carros = cursor.fetchall()
    cursor.close()
    conn.close()
    return carros


@app.route("/")
def landingpage():
    get_carros()
    return redirect(url_for("questionario"))


@app.route("/questionario", methods=['GET', 'POST'])
def questionario():

    return render_template("questionario.html")


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