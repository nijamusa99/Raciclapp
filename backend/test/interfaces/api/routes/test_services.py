def test_create_service_requires_auth(client):
    response = client.post("/api/v1/servicios", json={"descripcion": "Residuos"})
    assert response.status_code == 401

def test_create_service_with_token(client, auth_token):
    response = client.post(
        "/api/v1/servicios",
        json={"descripcion": "Papel"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["estado"] == "pendiente"