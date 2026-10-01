import secrets
import string

from .models import PushToken


def generate_push_token():

    characters = string.ascii_letters + string.digits

    token = ''.join(
        secrets.choice(characters)
        for _ in range(22)
    )

    PushToken.objects.create(
        token=token
    )

    return token