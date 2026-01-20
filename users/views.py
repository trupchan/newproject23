from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .services.send_code import send_confirmation_code
from .services.verify_code import verify_confirmation_code


@api_view(["POST"])
def send_code_view(request):
    """
    Отправка одноразового кода подтверждения
    """
    email = request.data.get("email")

    if not email:
        return Response(
            {"detail": "Email is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    send_confirmation_code(email)

    return Response(
        {"detail": "Confirmation code sent"},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def confirm_code_view(request):
    """
    Проверка одноразового кода подтверждения
    """
    email = request.data.get("email")
    code = request.data.get("code")

    if not email or not code:
        return Response(
            {"detail": "Email and code are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    is_valid = verify_confirmation_code(email, code)

    if not is_valid:
        return Response(
            {"detail": "Invalid or expired confirmation code"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(
        {"detail": "Code confirmed successfully"},
        status=status.HTTP_200_OK,
    )
