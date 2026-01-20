from .confirmation_codes import generate_code, save_confirmation_code


def send_confirmation_code(email: str):
    code = generate_code()
    save_confirmation_code(email, code)

    # Здесь обычно отправка email
    print(f"Confirmation code for {email}: {code}")
