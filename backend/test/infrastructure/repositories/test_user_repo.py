from app.infrastructure.repositories.user_repo import UserRepository

def test_create_and_get_user(db_session):
    repo = UserRepository(db_session)
    user_data = {
        "email": "nuevo@user.com",
        "password_hash": "hash",
        "nombre": "Nuevo",
        "rol": "cliente"
    }
    user = repo.create(user_data)
    assert user.id is not None
    retrieved = repo.get_by_email("nuevo@user.com")
    assert retrieved.nombre == "Nuevo"