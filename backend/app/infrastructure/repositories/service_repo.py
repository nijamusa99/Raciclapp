from sqlalchemy.orm import Session
from app.infrastructure.models import Service
from typing import List, Optional

class ServiceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, service: Service) -> Service:
        self.db.add(service)
        self.db.commit()
        self.db.refresh(service)
        return service

    def get_by_id(self, service_id: int) -> Optional[Service]:
        return self.db.query(Service).filter(Service.id == service_id).first()

    def list_by_client(self, client_id: int) -> List[Service]:
        return self.db.query(Service).filter(Service.cliente_id == client_id).all()

    def list_by_recycler(self, reciclador_id: int) -> List[Service]:
        return self.db.query(Service).filter(Service.reciclador_id == reciclador_id).all()

    def list_all(self) -> List[Service]:
        return self.db.query(Service).all()

    def update(self, service: Service) -> Service:
        self.db.commit()
        self.db.refresh(service)
        return service