# app/services/auth0_service.py

import requests
import time
from flask import current_app

# O cache de token, exatamente como no seu arquivo original
_token_cache = {"value": None, "exp": 0}

def get_management_api_token():
    """
    Obtém um token de acesso para a Auth0 Management API, utilizando um cache
    para evitar requisições desnecessárias.
    """
    now = time.time()
    # Verifica se o token no cache ainda é válido (com 60s de folga)
    if _token_cache["value"] and (_token_cache["exp"] - 60) > now:
        return _token_cache["value"]

    # Se não houver token válido no cache, busca um novo
    domain = current_app.config['AUTH0_DOMAIN']
    client_id = current_app.config['M2M_CLIENT_ID']
    client_secret = current_app.config['M2M_CLIENT_SECRET']
    audience = f"https://{domain}/api/v2/"
    
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'audience': audience,
        'grant_type': 'client_credentials'
    }
    headers = {'content-type': 'application/json'}
    
    try:
        r = requests.post(f"https://{domain}/oauth/token", json=payload, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()

        # Armazena o novo token e seu tempo de expiração no cache
        _token_cache["value"] = data["access_token"]
        _token_cache["exp"]   = now + data.get("expires_in", 3600)
        return _token_cache["value"]

    except requests.RequestException as e:
        print(f"Erro ao obter token do Auth0: {e}")
        raise ConnectionError("Não foi possível obter o token da Management API.") from e

def create_password_change_ticket(user_id):
    """
    Cria um ticket para alteração de senha para um usuário específico.
    """
    try:
        token = get_management_api_token()
        domain = current_app.config['AUTH0_DOMAIN']
        client_id = current_app.config['AUTH0_CLIENT_ID']

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "user_id": user_id,
            "client_id": client_id,
            "ttl_sec": 900, # O link será válido por 15 minutos
        }

        r = requests.post(f"https://{domain}/api/v2/tickets/password-change", headers=headers, json=payload, timeout=10)
        r.raise_for_status()
        
        return r.json()["ticket"]
    except requests.RequestException as e:
        print(f"Erro ao criar ticket de alteração de senha: {e}")
        raise ConnectionError("Não foi possível criar o ticket de alteração de senha.") from e
    
def resend_verification_email(user_id):
    """
    Cria um job para reenviar o e-mail de verificação para um usuário.
    """
    try:
        token = get_management_api_token()
        domain = current_app.config['AUTH0_DOMAIN']

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        payload = {"user_id": user_id}

        r = requests.post(f"https://{domain}/api/v2/jobs/verification-email", headers=headers, json=payload, timeout=10)
        r.raise_for_status()
        
        return r.json()
    except requests.RequestException as e:
        print(f"Erro ao reenviar e-mail de verificação: {e}")
        raise ConnectionError("Não foi possível reenviar o e-mail de verificação.") from e