import pytest
import sys
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

from app.infrastructure.database import Base, get_db
from app.infrastructure.models import User
from app.infrastructure.security import create_access_token, get_password_hash
from app.interfaces.main import app


root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

    
# Base de datos en memoria para pruebas
@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

# Sobreescribimos la dependencia de base de datos con la de testing
@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

# Fixture para crear un token válido de un usuario
@pytest.fixture(scope="function")
def auth_token(db_session):
    # Creamos un usuario de prueba
    user = User(
        email="test@example.com",
        password_hash=get_password_hash("secret"),
        nombre="Test User",
        rol="cliente"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    token = create_access_token(data={"sub": str(user.id), "rol": user.rol})
    return token

# Fixture para un usuario admin
@pytest.fixture(scope="function")
def admin_token(db_session):
    admin = User(
        email="admin@test.com",
        password_hash=get_password_hash("adminsecret"),
        nombre="Admin",
        rol="superadmin"
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return create_access_token(data={"sub": str(admin.id), "rol": admin.rol})

@pytest.fixture(scope="function")
def reciclador_user(db_session):
    """Crea un usuario reciclador de prueba y lo retorna"""
    from app.infrastructure.repositories.user_repo import UserRepository
    repo = UserRepository(db_session)
    user_dict = {
        "email": "reciclador@test.com",
        "password_hash": get_password_hash("recicladorpass"),
        "nombre": "Reciclador Test",
        "rol": "reciclador",
        "tipo_vehiculo": "Camioneta"
    }
    user = repo.create(user_dict)
    return user

@pytest.fixture(scope="function")
def reciclador_token(db_session, reciclador_user):
    """Token JWT válido para el reciclador"""
    token = create_access_token(data={"sub": str(reciclador_user.id), "rol": reciclador_user.rol})
    return token