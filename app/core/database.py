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
