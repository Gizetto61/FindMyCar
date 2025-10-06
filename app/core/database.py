# app/core/database.py

import mysql.connector
import os

def get_db_connection():
    """Cria e retorna uma nova conexão com o banco de dados."""
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=os.getenv("MYSQL_PORT"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )
    return conn

def get_carros():
    """Busca e retorna todos os carros do banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM Carro")
        carros = cursor.fetchall()
        return carros
    except Exception as e:
        # Em uma aplicação real, você poderia logar o erro aqui
        print(f"Ocorreu um erro ao buscar os carros: {e}")
        return [] # Retorna uma lista vazia em caso de erro
    finally:
        # Garante que o cursor e a conexão sejam sempre fechados
        cursor.close()
        conn.close()

def get_carro(id):
    """Busca e retorna um carro pelo id."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(f"SELECT * FROM Consulta_Carros WHERE id = '{id}';")
        carro = cursor.fetchall()
        carro = carro[0]
        return carro
    except Exception as e:
        # Em uma aplicação real, você poderia logar o erro aqui
        print(f"Ocorreu um erro ao buscar os carros: {e}")
        return [] # Retorna uma lista vazia em caso de erro
    finally:
        # Garante que o cursor e a conexão sejam sempre fechados
        cursor.close()
        conn.close()

def get_anuncio(id):
    """Busca e retorna um anuncio pelo id."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(f"SELECT * FROM Anuncio WHERE id_Anuncio = '{id}';")
        anuncio = cursor.fetchall()
        anuncio = anuncio[0]
        return anuncio
    except Exception as e:
        # Em uma aplicação real, você poderia logar o erro aqui
        print(f"Ocorreu um erro ao buscar um anuncio: {e}")
        return [] # Retorna uma lista vazia em caso de erro
    finally:
        # Garante que o cursor e a conexão sejam sempre fechados
        cursor.close()
        conn.close()        

def get_imagens_by_anuncio_id(anuncio_id):
    """
    Busca todas as imagens (strings base64) de um anúncio específico,
    ordenadas pela coluna 'ordem'.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT dados_base64 
            FROM ImagensAnuncio 
            WHERE fk_Anuncio_id_Anuncio = %s 
        """
        cursor.execute(query, (anuncio_id,))
        # fetchall() retorna uma lista de dicionários, ex: [{'dados_base64': '...'}, {...}]
        imagens = cursor.fetchall()
        # Extrai apenas as strings base64 da lista de dicionários
        return [img['dados_base64'] for img in imagens]
    except Exception as e:
        print(f"Erro ao buscar imagens do anúncio {anuncio_id}: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_nota(id):
    """Busca e retorna as notas de um carro pelo id."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(f"SELECT nota_preco as Preço, nota_espaco as Espaço, nota_potencia as Potência, nota_desempenho as Desempenho, nota_consumo as Consumo, nota_conforto as Conforto FROM Classificacao_Carros WHERE carro_id = '{id}';")
        notas = cursor.fetchall()
        notas = notas[0]
        return notas
    except Exception as e:
        # Em uma aplicação real, você poderia logar o erro aqui
        print(f"Ocorreu um erro ao buscar notas do carro: {e}")
        return [] # Retorna uma lista vazia em caso de erro
    finally:
        # Garante que o cursor e a conexão sejam sempre fechados
        cursor.close()
        conn.close()


def update_user_profile(user_id, profile_data):
    """
    Atualiza os dados de um usuário no banco de dados.
    'profile_data' é um dicionário com os campos a serem atualizados.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    # Monta a query e os dados para a atualização
    # NUNCA use f-strings ou concatenação para montar queries. Isso previne SQL Injection.
    query = """
        UPDATE users 
        SET name = %s, nickname = %s, birthdate = %s, phone = %s, cpf = %s
        WHERE id = %s 
    """ # Supondo que você tenha um 'id' na sua tabela de usuários
    
    # Os valores devem estar na mesma ordem da query
    values = (
        profile_data.get('name'),
        profile_data.get('nickname'),
        profile_data.get('birthdate'),
        profile_data.get('phone'),
        profile_data.get('cpf'),
        user_id
    )
    
    try:
        cursor.execute(query, values)
        conn.commit()  # ESSENCIAL: .commit() salva as alterações no banco
        print(f"Usuário {user_id} atualizado com sucesso.")
        return True # Retorna sucesso
    except Exception as e:
        conn.rollback() # Desfaz a transação em caso de erro
        print(f"Erro ao atualizar usuário {user_id}: {e}")
        return False # Retorna falha
    finally:
        cursor.close()
        conn.close()

def create_anuncio(cursor, anuncio_data, user_id):
    """
    Insere um novo anúncio na tabela Anuncios.
    Retorna o ID do anúncio recém-criado.
    Recebe o cursor para operar dentro de uma transação.
    """
    query = """
        INSERT INTO Anuncio 
        (data_Anun, fk_users_id, Quilometragem, Transmissao, Condicao, Observacoes, Telefone, Estado, Cidade, Endereco, fk_carro_id, Ano_Fabric, Ano_Mod, Cor, Preco)
        VALUES (CURDATE(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    # NOTA: fk_Carro_id_Carro não está no seu formulário. Adicionei como None.
    # Você precisará de um campo no formulário para o usuário selecionar o carro.
    values = (
        user_id,
        anuncio_data.get('km'),
        anuncio_data.get('transmissao'),
        anuncio_data.get('condicao'),
        anuncio_data.get('observacoes'),
        anuncio_data.get('telefone'),
        anuncio_data.get('estado'),
        anuncio_data.get('cidade'),
        anuncio_data.get('endereco'),
        anuncio_data.get('carro_id'),
        anuncio_data.get('ano_fabricacao'),
        anuncio_data.get('ano_modelo'),
        anuncio_data.get('cor'),
        anuncio_data.get('preco')
    )
    cursor.execute(query, values)
    return cursor.lastrowid # Retorna o ID do anúncio que acabamos de inserir

def add_imagem_to_anuncio(cursor, anuncio_id, base64_string):
    """
    Insere uma imagem Base64 na tabela ImagensAnuncio, associada a um anúncio.
    Recebe o cursor para operar dentro de uma transação.
    """
    query = "INSERT INTO ImagensAnuncio (dados_base64, fk_Anuncio_id_Anuncio) VALUES (%s, %s)"
    values = (base64_string, anuncio_id)
    cursor.execute(query, values)

def get_user_by_email(email):
    """
    Busca um usuário na tabela 'Usuario' pelo seu email.
    Retorna um dicionário com os dados do usuário ou None se não for encontrado.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Adapte o nome da tabela (Usuario) e das colunas (Email, id_Usuario) se necessário
        cursor.execute("SELECT id, nickname, email FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        return user # Retorna o dicionário do usuário ou None
    except Exception as e:
        print(f"Erro ao buscar usuário por e-mail: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_user_phone_by_id(user_id):
    """Busca o telefone de um usuário pelo seu ID do banco."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # ATENÇÃO: A query abaixo é um exemplo. Adapte para sua tabela de usuários.
        cursor.execute("SELECT phone FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        return user['phone'] if user else None
    finally:
        cursor.close()
        conn.close()

def get_all_car_models():
    """Busca ID, Marca e Modelo de todos os carros para o select do formulário."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Seleciona apenas os campos que precisamos
        cursor.execute("SELECT id, marca, modelo FROM Consulta_Carros ORDER BY marca, modelo")
        carros = cursor.fetchall()
        return carros
    except Exception as e:
        print(f"Erro ao buscar modelos de carro: {e}")
        return []
    finally:
        cursor.close()
        conn.close()