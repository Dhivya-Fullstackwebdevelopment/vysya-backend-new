from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .google_auth import (
    verify_google_access_token,
    GoogleAuthError,
)
from .services import send_push


@api_view(["POST"])
@permission_classes([AllowAny])
def google_login(request):
    access_token = request.data.get("access_token")

    # Verify Google account first
    try:
        google_user = verify_google_access_token(access_token)
    except GoogleAuthError as exc:
        return Response(
            {
                "status": 0,
                "message": str(exc),
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # STATIC RESPONSE - TESTING ONLY
    return Response(
        {
            "status": 1,
            "token": "TEST_TOKEN_NOT_FOR_PRODUCTION",
            "profile_id": "VM56639",
            "login_username": "Dhivya test",
            "age": 24,
            "message": "Login Successful",
            "notification_count": 2,
            "cur_plan_id": "8",
            "plan_name": "Prospect",
            "profile_image": "https://vysyamat.blob.core.windows.net/vysyamala/men.jpg",
            "profile_completion": 0,
            "gender": "male",
            "height": "182",
            "marital_status": "2",
            "custom_message": 1,
            "birth_star_id": "15",
            "birth_rasi_id": "7",
            "profile_owner": "Admin",
            "quick_reg": "0",
            "plan_limits": [],
            "valid_till": "2027-09-23T18:29:59Z",
            "google_email": google_user["email"],
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def send_notification(request):
    token = request.data.get("token")
    title = request.data.get("title", "Notification")
    body = request.data.get("body", "")

    if not isinstance(token, str) or not token.strip():
        return Response(
            {
                "success": False,
                "message": "token is required",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    provider, result = send_push(token.strip(), title, body)
    return Response(
        {
            "success": True,
            "provider": provider,
            "result": result,
        },
        status=status.HTTP_200_OK,
    )