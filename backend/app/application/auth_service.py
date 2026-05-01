from app.infrastructure.security import get_password_hash, verify_password, create_access_token
from app.infrastructure.repositories.user_repo import UserRepository
from app.infrastructure.models import User as UserModel
from typing import Optional

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register(self, user_data: dict) -> UserModel:
        if self.user_repo.get_by_email(user_data['email']):
            raise ValueError("El email ya está registrado")
    
        # Extraer la contraseña antes de hashearla
        password = user_data.pop('password')
        hashed = get_password_hash(password)
        user_data['password_hash'] = hashed
        user_data.setdefault('activo', True)
        return self.user_repo.create(user_data)

    def authenticate(self, email: str, password: str) -> Optional[str]:
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            return None
        return create_access_token(data={"sub": str(user.id), "rol": user.rol})