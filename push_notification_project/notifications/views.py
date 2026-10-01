from rest_framework.decorators import api_view
from rest_framework.response import Response

from .utils import generate_push_token


@api_view(["GET"])
def generate_token(request):

    token = generate_push_token()

    return Response({
        "success": True,
        "message": "Token generated successfully",
        "token": token
    })