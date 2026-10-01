from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import PushToken


@api_view(['POST'])
def save_push_token(request):

    user_id = request.data.get('user_id')
    mobile = request.data.get('mobile')
    name = request.data.get('name')
    token = request.data.get('token')

    if not token:
        return Response(
            {
                "success": False,
                "message": "Push token is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    push_token, created = PushToken.objects.update_or_create(
        token=token,
        defaults={
            "user_id": user_id,
            "mobile": mobile,
            "name": name,
        }
    )

    return Response({
        "success": True,
        "message": "Push token saved successfully",
        "created": created,
        "data": {
            "id": push_token.id,
            "user_id": push_token.user_id,
            "mobile": push_token.mobile,
            "name": push_token.name,
            "token": push_token.token,
        }
    })