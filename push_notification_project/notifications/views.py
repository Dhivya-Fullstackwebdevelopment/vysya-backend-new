from rest_framework.decorators import api_view
from rest_framework.response import Response

from .services import send_push


@api_view(["POST"])
def send_notification(request):
    token = request.data.get("token")
    title = request.data.get("title", "Notification")
    body = request.data.get("body", "")

    if not token:
        return Response(
            {"success": False, "message": "token is required"}, status=400
        )

    try:
        provider, result = send_push(token, title, body)
    except Exception as e:
        return Response({"success": False, "message": str(e)}, status=502)

    return Response({"success": True, "provider": provider, "result": result})