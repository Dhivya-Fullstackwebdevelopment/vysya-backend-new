import requests
from django.conf import settings

EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send"


def send_expo(token, title, body):
    if not token.startswith("ExponentPushToken["):
        token = f"ExponentPushToken[{token}]"

    response = requests.post(
        EXPO_PUSH_URL,
        json={"to": token, "title": title, "body": body, "sound": "default"},
        headers={"Accept": "application/json"},
        timeout=10,
    )
    return response.json()


def send_firebase(token, title, body):
    # Imported here so local (expo) mode works without firebase-admin
    import firebase_admin
    from firebase_admin import credentials, messaging

    if not firebase_admin._apps:
        cred = credentials.Certificate(str(settings.FIREBASE_CREDENTIALS))
        firebase_admin.initialize_app(cred)

    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        token=token,
    )
    return {"message_id": messaging.send(message)}


def send_push(token, title, body):
    if settings.PUSH_PROVIDER == "firebase":
        return "firebase", send_firebase(token, title, body)
    return "expo", send_expo(token, title, body)