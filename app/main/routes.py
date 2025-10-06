from flask import render_template, session, redirect, url_for, abort, flash, request
from app.core.database import update_user_profile, get_carro, get_nota, get_all_car_models, get_anuncio, get_imagens_by_anuncio_id
from app.main import bp

# As rotas agora usam o decorador @bp.route em vez de @app.route

@bp.route("/")
def start():
    # Verifica se o usuário está logado para decidir a página inicial
    is_logged_in = 'user' in session
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

@bp.route("/ficha")
@bp.route("/ficha/<int:car_id>")
def ficha_tecnica(car_id=None):
    is_logged_in = 'user' in session
    
    # Se car_id não for fornecido, usa ID 1 como padrão
    if car_id is None:
        car_id = 1
# Tenta buscar do banco de dados
    carro = get_carro(car_id)
    
    # Se não encontrou o carro no banco, retorna 404
    if carro is None:
        abort(404)
    
    notas = get_nota(car_id)
    media = 0
    for n in notas:
        media += float(notas[n])
    nota_final = round(media/6, 2)
    # Busca carros relacionados (se falhar, lista vazia)
    return render_template('ficha.html', 
                            carro=carro, notas=notas,nota_final=nota_final,
                            is_logged_in=is_logged_in)

@bp.route("/anuncio")
@bp.route("/anuncio/<int:anuncio_id>")
def anuncio(anuncio_id=None):
    is_logged_in = 'user' in session
    
    # Se car_id não for fornecido, usa ID 1 como padrão
    if anuncio_id is None:
        anuncio_id = 20

    anuncio = get_anuncio(anuncio_id)
    car_id = anuncio['fk_carro_id']

    imagens_do_anuncio = get_imagens_by_anuncio_id(anuncio_id)
# Tenta buscar do banco de dados
    carro = get_carro(car_id)
    
    # Se não encontrou o carro no banco, retorna 404
    if carro is None:
        abort(404)
    
    notas = get_nota(car_id)
    media = 0
    for n in notas:
        media += float(notas[n])
    nota_final = round(media/6, 2)
    # Busca carros relacionados (se falhar, lista vazia)
    return render_template('anuncio.html', 
                            carro=carro, notas=notas,nota_final=nota_final, anuncio=anuncio, imagens=imagens_do_anuncio,
                            is_logged_in=is_logged_in)

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

@bp.route('/anunciar')
def criar_anuncio_form():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    # Busca a lista de todos os carros no banco
    lista_de_carros = get_all_car_models()
    
    # Renderiza o template do formulário, passando a lista de carros
    return render_template(
        'anuncio_form.html', # O nome do seu arquivo HTML do formulário
        lista_de_carros=lista_de_carros, 
        is_logged_in=True,
        use_vue=True # Se você estiver usando Vue nesta página
    )

# Manter redirecionamentos de rotas antigas, se necessário
@bp.route("/homepage")
def homepage():
    return redirect(url_for("main.start"))

@bp.route("/home")
def home():
    return redirect(url_for("main.start"))
