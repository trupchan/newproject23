from django.urls import path
from .views import send_code_view, confirm_code_view


urlpatterns = [
    path("send-code/", send_code_view),
    path("confirm-code/", confirm_code_view),
]
