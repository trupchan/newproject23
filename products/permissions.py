from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
    Модератор:
    - is_staff = True
    - может GET, PUT, PATCH, DELETE
    - НЕ может POST
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        # модератор = сотрудник
        if not user.is_staff:
            return False

        # запрет на создание
        if request.method == "POST":
            return False

        return True
