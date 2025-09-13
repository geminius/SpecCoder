# src/api/reset.py

def request_password_reset(email: str) -> dict:
    # Demo stub: In real code, generate token, persist, enqueue email
    if not isinstance(email, str) or "@" not in email:
        raise ValueError("invalid email")
    return {"ok": True}
