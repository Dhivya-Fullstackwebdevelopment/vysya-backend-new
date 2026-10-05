import sys
import time
import json
import requests

EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send"
EXPO_RECEIPT_URL = "https://exp.host/--/api/v2/push/getReceipts"
FIREBASE_KEY_FILE = "serviceAccountKey.json"  # live-ku mattum venum
EXPO_PREFIXES = ("ExponentPushToken[", "ExpoPushToken[")
HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}


def is_expo_token(token):
    # Wrapped Expo token, illana raw ID. FCM token 100+ chars, ":" irukkum
    return token.startswith(EXPO_PREFIXES) or (len(token) < 50 and ":" not in token)


def send_expo(token, title, body, data=None):
    if not token.startswith(EXPO_PREFIXES):
        token = f"ExponentPushToken[{token}]"

    res = requests.post(
        EXPO_PUSH_URL,
        json={"to": token, "title": title, "body": body,
              "sound": "default", "data": data or {}},
        headers=HEADERS,
        timeout=10,
    )
    res.raise_for_status()
    result = res.json()

    item = result.get("data")
    if isinstance(item, dict) and item.get("status") == "error":
        raise Exception(item.get("message", "Expo push failed"))
    return result


def check_expo_receipt(ticket_id):
    res = requests.post(
        EXPO_RECEIPT_URL, json={"ids": [ticket_id]}, headers=HEADERS, timeout=10
    )
    res.raise_for_status()
    return res.json().get("data", {}).get(ticket_id, {})


def send_firebase(token, title, body, data=None):
    import firebase_admin
    from firebase_admin import credentials, messaging

    if not firebase_admin._apps:
        firebase_admin.initialize_app(credentials.Certificate(FIREBASE_KEY_FILE))

    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        data={k: str(v) for k, v in (data or {}).items()},  # FCM data string mattum
        token=token,
    )
    return {"message_id": messaging.send(message)}


def send_push(token, title="Notification", body="", data=None):
    token = (token or "").strip()
    if not token:
        raise ValueError("token is required")
    if is_expo_token(token):
        return "expo", send_expo(token, title, body, data)
    return "firebase", send_firebase(token, title, body, data)


if __name__ == "__main__":
    # Usage: python send_push.py <token> "Title" "Body" '{"screen":"Notifications"}'
    if len(sys.argv) < 2:
        print('Usage: python send_push.py <token> "Title" "Body" [\'{"key":"value"}\']')
        sys.exit(1)

    token = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else "Notification"
    body = sys.argv[3] if len(sys.argv) > 3 else "Hello"
    data = json.loads(sys.argv[4]) if len(sys.argv) > 4 else {}

    try:
        provider, result = send_push(token, title, body, data)
        print(f"Sent via {provider}: {result}")

        if provider == "expo":
            ticket_id = result.get("data", {}).get("id")
            if ticket_id:
                time.sleep(5)  # receipt ready aaga konjam neram aagum
                print("Receipt:", check_expo_receipt(ticket_id))
    except Exception as e:
        print("Failed:", e)