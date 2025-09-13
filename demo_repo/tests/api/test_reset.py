# tests/api/test_reset.py

from src.api.reset import request_password_reset

def test_reset_ok():
    res = request_password_reset("user@example.com")
    assert res["ok"] is True
