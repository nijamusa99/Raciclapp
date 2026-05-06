def test_admin_can_list_users(client, admin_token):
    response = client.get(
        "/api/v1/admin/usuarios",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_non_admin_cannot_list_users(client, auth_token):
    response = client.get(
        "/api/v1/admin/usuarios",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 403