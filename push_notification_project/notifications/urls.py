from django.urls import path
from .views import google_login, send_notification

urlpatterns = [
    path(
        "google-login/",
        google_login,
        name="google_login",
    ),
    path(
        "send-notification/",
        send_notification,
        name="send_notification",
    ),
]