from sqlalchemy.orm import Session
from app.infrastructure.models import Rating
from typing import List, Optional

class RatingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, rating: Rating) -> Rating:
        self.db.add(rating)
        self.db.commit()
        self.db.refresh(rating)
        return rating

    def get_by_service(self, service_id: int) -> Optional[Rating]:
        return self.db.query(Rating).filter(Rating.servicio_id == service_id).first()

    def list_by_recycler(self, reciclador_id: int) -> List[Rating]:
        return self.db.query(Rating).filter(Rating.calificado_id == reciclador_id).all()

    def list_all(self) -> List[Rating]:
        return self.db.query(Rating).all()