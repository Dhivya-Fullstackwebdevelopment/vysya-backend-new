import secrets
import string
from datetime import datetime, timezone

# In-memory store
TOKEN_STORE = {}


def generate_push_token():
    characters = string.ascii_letters + string.digits

    while True:
        token = ''.join(secrets.choice(characters) for _ in range(22))
        if token not in TOKEN_STORE:
            break

    TOKEN_STORE[token] = {
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    return token