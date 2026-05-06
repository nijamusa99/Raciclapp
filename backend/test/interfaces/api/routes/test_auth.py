def test_register_and_login(client):
    # Registro
    response = client.post("/api/v1/auth/register", json={
        "email": "apitest@example.com",
        "password": "testpass",
        "nombre": "API Test",
        "rol": "cliente"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

    # Login con las mismas credenciales
    response = client.post("/api/v1/auth/login", json={
        "email": "apitest@example.com",
        "password": "testpass"
    })
    assert response.status_code == 200

    # Login fallido
    response = client.post("/api/v1/auth/login", json={
        "email": "fake@mail.com",
        "password": "nope"
    })
    assert response.status_code == 401