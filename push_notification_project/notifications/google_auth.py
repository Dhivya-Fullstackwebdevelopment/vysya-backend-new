import requests

GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


class GoogleAuthError(Exception):
    pass


def verify_google_access_token(access_token):
    access_token = (access_token or "").strip()

    if not access_token:
        raise GoogleAuthError("access_token is required")

    try:
        response = requests.get(
            GOOGLE_USERINFO_URL,
            headers={
                "Authorization": f"Bearer {access_token}"
            },
            timeout=10,
        )
    except requests.RequestException as exc:
        raise GoogleAuthError(
            "Google verification service is unavailable"
        ) from exc

    if response.status_code != 200:
        raise GoogleAuthError(
            "Invalid or expired Google access token"
        )

    try:
        data = response.json()
    except ValueError as exc:
        raise GoogleAuthError(
            "Invalid response from Google"
        ) from exc

    google_id = data.get("sub")
    email = data.get("email")
    email_verified = data.get("email_verified", True)

    if not google_id or not email or not email_verified:
        raise GoogleAuthError(
            "A verified Google account is required"
        )

    return {
        "google_id": google_id,
        "email": email.lower(),
        "name": data.get("name", ""),
        "picture": data.get("picture", ""),
    }