from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.infrastructure.repositories.user_repo import UserRepository
from app.application.auth_service import AuthService
from app.interfaces.api.models import UserRegister, UserLogin, Token
from app.domain.enums import UserRole

router = APIRouter()

@router.post("/register", response_model=Token)
def register(data: UserRegister, db: Session = Depends(get_db)):
    if data.rol not in [r.value for r in UserRole]:
        raise HTTPException(status_code=400, detail="Rol no válido")
    user_repo = UserRepository(db)
    auth = AuthService(user_repo)
    try:
        # Pasar el diccionario completo (incluye 'password')
        auth.register(data.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    token = auth.authenticate(data.email, data.password)
    if not token:
        raise HTTPException(status_code=400, detail="Error al autenticar")
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    auth = AuthService(user_repo)
    token = auth.authenticate(data.email, data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return {"access_token": token, "token_type": "bearer"}