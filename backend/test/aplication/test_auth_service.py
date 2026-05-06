import pytest
from app.application.auth_service import AuthService
from app.infrastructure.repositories.user_repo import UserRepository

def test_register_and_authenticate(db_session):
    repo = UserRepository(db_session)
    service = AuthService(repo)
    user_data = {
        "email": "auth@test.com",
        "password": "clave123",
        "nombre": "Auth",
        "rol": "cliente"
    }
    # Registro
    user = service.register(user_data.copy())
    assert user.email == "auth@test.com"
    # Autenticación exitosa
    token = service.authenticate("auth@test.com", "clave123")
    assert token is not None
    # Contraseña incorrecta
    token = service.authenticate("auth@test.com", "incorrecta")
    assert token is None