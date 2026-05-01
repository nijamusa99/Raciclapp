from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.database import engine, Base
from app.interfaces.api.routes import auth, services, reciclador, admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Reciclap API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(services.router, prefix="/api/v1", tags=["services"])
app.include_router(reciclador.router, prefix="/api/v1/reciclador", tags=["reciclador"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])

@app.get("/")
def root():
    return {"message": "Reciclap API funcionando"}