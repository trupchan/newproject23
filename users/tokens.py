from rest_framework_simplejwt.tokens import RefreshToken


class CustomRefreshToken(RefreshToken):

    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)

        token["email"] = user.email
        token["birthdate"] = (
            user.birthdate.isoformat() if user.birthdate else None
        )

        return token
