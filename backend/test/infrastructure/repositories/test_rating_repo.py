from app.infrastructure.repositories.rating_repo import RatingRepository
from app.infrastructure.models import Rating
from datetime import datetime

def test_create_rating(db_session):
    repo = RatingRepository(db_session)
    rating = Rating(
        servicio_id=1,
        calificador_id=1,
        calificado_id=2,
        puntuacion=5,
        comentario="Excelente",
        fecha=datetime.utcnow()
    )
    created = repo.create(rating)
    assert created.id is not None