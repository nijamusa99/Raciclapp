from app.infrastructure.repositories.evidence_repo import EvidenceRepository
from app.infrastructure.models import Evidence
from datetime import datetime

def test_create_evidence(db_session):
    repo = EvidenceRepository(db_session)
    evidence = Evidence(
        servicio_id=1,
        reciclador_id=2,
        fotos="foto1.jpg,foto2.jpg",
        timestamp_completado=datetime.utcnow()
    )
    created = repo.create(evidence)
    assert created.id is not None
    assert created.servicio_id == 1