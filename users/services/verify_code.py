from .confirmation_codes import (
    get_confirmation_code,
    delete_confirmation_code,
)


def verify_confirmation_code(email: str, code: str) -> bool:
    stored_code = get_confirmation_code(email)

    if not stored_code:
        return False

    if stored_code != code:
        return False

    # ❗ КОД ИСПОЛЬЗОВАН → УДАЛЯЕМ
    delete_confirmation_code(email)
    return True
