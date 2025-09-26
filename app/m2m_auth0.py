# m2m_auth0.py
import os, time, requests

AUTH0_DOMAIN     = os.getenv("AUTH0_DOMAIN")
M2M_CLIENT_ID    = os.getenv("M2M_CLIENT_ID")
M2M_CLIENT_SECRET= os.getenv("M2M_CLIENT_SECRET")

if not (AUTH0_DOMAIN and M2M_CLIENT_ID and M2M_CLIENT_SECRET):
    raise RuntimeError("Faltam AUTH0_DOMAIN / M2M_CLIENT_ID / M2M_CLIENT_SECRET.")

_token_cache = {"value": None, "exp": 0}

def get_management_token():
    # cache de token (folga 60s)
    now = time.time()
    if _token_cache["value"] and (_token_cache["exp"] - 60) > now:
        return _token_cache["value"]

    resp = requests.post(
        f"https://{AUTH0_DOMAIN}/oauth/token",
        json={
            "client_id": M2M_CLIENT_ID,
            "client_secret": M2M_CLIENT_SECRET,
            "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
            "grant_type": "client_credentials"
        },
        timeout=10
    )
    resp.raise_for_status()
    data = resp.json()

    _token_cache["value"] = data["access_token"]
    _token_cache["exp"]   = now + data.get("expires_in", 3600)
    return _token_cache["value"]
