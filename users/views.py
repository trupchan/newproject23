import requests

from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils import timezone

from .models import CustomUser


def google_login(request):
    """
    Редирект пользователя на Google OAuth
    """
    google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"

    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }

    request_url = requests.Request(
        "GET", google_auth_url, params=params
    ).prepare().url

    return redirect(request_url)


def google_callback(request):
    """
    Callback от Google: получаем code → access_token → данные пользователя
    """
    code = request.GET.get("code")

    if not code:
        return JsonResponse({"error": "No code provided"}, status=400)

    # 1️⃣ Получаем access_token
    token_url = "https://oauth2.googleapis.com/token"

    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()

    access_token = token_json.get("access_token")

    if not access_token:
        return JsonResponse({"error": "Failed to get access token"}, status=400)

    # 2️⃣ Получаем данные пользователя
    userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}

    userinfo_response = requests.get(userinfo_url, headers=headers)
    userinfo = userinfo_response.json()

    email = userinfo.get("email")
    first_name = userinfo.get("given_name", "")
    last_name = userinfo.get("family_name", "")

    if not email:
        return JsonResponse({"error": "Email not provided by Google"}, status=400)

    # 3️⃣ Создаём или обновляем пользователя
    user, created = CustomUser.objects.get_or_create(
        email=email,
        defaults={
            "first_name": first_name,
            "last_name": last_name,
            "is_active": True,
            "registration_source": "google",
        },
    )

    if not created:
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = True

    user.last_login = timezone.now()
    user.save()

    return JsonResponse(
        {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "message": "Logged in with Google",
        }
    )
