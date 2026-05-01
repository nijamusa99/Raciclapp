import sys
import os
# Asegura que el directorio actual (backend) esté en sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.infrastructure.database import SessionLocal, engine, Base
from app.infrastructure.models import User
from app.infrastructure.security import get_password_hash

Base.metadata.create_all(bind=engine)

db = SessionLocal()
admin_exists = db.query(User).filter(User.rol == "superadmin").first()
if not admin_exists:
    admin = User(
        email="admin@reciclap.com",
        password_hash=get_password_hash("Admin123!"),
        nombre="Super Admin",
        rol="superadmin"
    )
    db.add(admin)
    db.commit()
    print("Super Admin creado: admin@reciclap.com / Admin123!")
else:
    print("Super Admin ya existe.")
db.close()