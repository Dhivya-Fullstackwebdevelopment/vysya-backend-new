from django.urls import path
from .views import generate_token

urlpatterns = [
    path("generate-token/", generate_token, name="generate_token"),
]