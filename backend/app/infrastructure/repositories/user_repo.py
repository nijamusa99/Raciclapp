from sqlalchemy.orm import Session
from app.infrastructure.models import User
from app.domain.entities import Usuario
from typing import List, Optional

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, data: dict) -> User:
        user = User(**data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user_obj: User) -> User:
        self.db.commit()
        self.db.refresh(user_obj)
        return user_obj

    def list_by_role(self, role: str) -> List[User]:
        return self.db.query(User).filter(User.rol == role).all()

    def list_all(self) -> List[User]:
        return self.db.query(User).all()