from sqlalchemy.orm import Session
from app.infrastructure.models import Evidence
from typing import Optional

class EvidenceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, evidence: Evidence) -> Evidence:
        self.db.add(evidence)
        self.db.commit()
        self.db.refresh(evidence)
        return evidence

    def get_by_service(self, service_id: int) -> Optional[Evidence]:
        return self.db.query(Evidence).filter(Evidence.servicio_id == service_id).first()