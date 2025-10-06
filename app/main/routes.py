from flask import render_template, session, redirect, url_for, abort, flash, request
from app.core.database import update_user_profile
from app.main import bp

# As rotas agora usam o decorador @bp.route em vez de @app.route

@bp.route("/")
def start():
    # Verifica se o usuário está logado para decidir a página inicial
    is_logged_in = 'user' in session
    if is_logged_in:
        # Se logado, pode ir direto para o questionário ou outra página interna
        return redirect(url_for("main.questionario"))
    return render_template("homepage.html", is_logged_in=is_logged_in)

@bp.route("/questionario")
def questionario():
    if 'user' in session:
        return render_template('questionario.html', use_vue=True, is_logged_in=True)
    return redirect(url_for("auth.login")) # Redireciona para a rota de login do blueprint 'auth'

@bp.route('/recomendacao')
def recomendacao():
    if 'user' in session:
        if "recomendacoes" in session:
            top_5 = session.get('recomendacoes')
            if not top_5:
                return redirect(url_for('main.questionario'))
            
            return render_template('recomendacao.html',
                                   carro_principal=top_5[0],
                                   outros_carros=top_5[1:], 
                                   is_logged_in=True)
        else:
            return redirect(url_for("main.questionario"))
    return redirect(url_for("auth.login"))

@bp.route("/perfil")
def perfil():
    if 'user' in session:
        return render_template('perfil.html', is_logged_in=True)
    return redirect(url_for("auth.login"))

@bp.route("/perfil/update", methods=['POST'])
def update_perfil():
    if 'user' not in session:
        abort(401) # Proibido se não estiver logado

    # Pega o user_id da sessão (você precisará ter salvo o ID do seu banco na sessão)
    user_id_banco = session['user']['sub'].lstrip("auth0|") 

    # Chama a função do nosso módulo de banco de dados, passando os dados do formulário
    print(request.form.to_dict())
    success = update_user_profile(user_id_banco, request.form.to_dict())

    if success:
        flash("Perfil atualizado com sucesso!", "success")
    else:
        flash("Ocorreu um erro ao atualizar o perfil.", "error")
        
    return redirect(url_for('main.perfil'))

@bp.route("/termos")
def termos():
    return render_template("termos.html", is_logged_in=('user' in session))

@bp.route("/contatos")
def contatos():
    return render_template("contatos.html", is_logged_in=('user' in session))

@bp.route("/sobre")
def sobre():
    return render_template("sobre.html", is_logged_in=('user' in session))

@bp.route("/servicos")
def servicos():
    return render_template("servicos.html", is_logged_in=('user' in session))

@bp.route("/suporte")
def suporte():
    return render_template("suporte.html", is_logged_in=('user' in session))

@bp.route("/anuncio_form")
def anuncio_form():
    return render_template("anuncio_form.html", is_logged_in=('user' in session))

# Manter redirecionamentos de rotas antigas, se necessário
@bp.route("/homepage")
def homepage():
    return redirect(url_for("main.start"))

@bp.route("/home")
def home():
    return redirect(url_for("main.start"))