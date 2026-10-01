from django.urls import path
from .views import save_push_token

urlpatterns = [
    path('save-token/', save_push_token, name='save_push_token'),
]