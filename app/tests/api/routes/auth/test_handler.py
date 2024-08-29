from fastapi import HTTPException


# tests for "/api/auth/create-user"
def test_create_new_user_success(client):
    user_data = {
        "email": "john@doe.com",
        "username": "john",
        "first_name": "john",
        "last_name": "doe",
        "password": "password123",
        "role": "user",
        "phone_number": "999999999"
    }
    response = client.post("/api/auth/create-user", json=user_data)
    assert response.status_code == 201


def test_create_new_user_missing_field(client):
    user_data = {
        "email": "john@doe.com",
        "username": "john",
        "first_name": "john",
        "last_name": "doe",
        "password": "password123",
        "role": "user"
    }
    response = client.post("/api/auth/create-user", json=user_data)
    assert response.status_code == 422


def test_create_new_user_invalid_email(client):
    user_data = {
        "email": "",
        "username": "john",
        "first_name": "john",
        "last_name": "doe",
        "password": "password123",
        "role": "user",
        "phone_number": "999999999"
    }
    response = client.post("/api/auth/create-user", json=user_data)
    assert response.status_code == 422


# tests for "/api/auth/sign-in"
def test_sign_in_success(client):
    sign_in_data = {
        "username": "john",
        "password": "password123"
    }
    response = client.post("/api/auth/sign-in", json=sign_in_data)
    assert response.status_code == 200
    assert "access_token" in response.json()["data"]
    assert "refresh_token" in response.json()["data"]


def test_sign_in_invalid_credentials(client):
    sign_in_data = {
        "username": "john",
        "password": "wrongpassword"
    }
    response = client.post("/api/auth/sign-in", json=sign_in_data)
    assert response.status_code == 401


def test_sign_in_missing_field(client):
    sign_in_data = {
        "username": "john"
    }
    response = client.post("/api/auth/sign-in", json=sign_in_data)
    assert response.status_code == 422


# tests for "/refresh-token"
def test_refresh_token_success(client, mocker):
    mocker.patch("app.api.routes.auth.service.new_access_token", return_value="new_access_token")
    response = client.get("/api/auth/refresh-token", headers={"Authorization": "Bearer mocked_token"})
    assert response.status_code == 200
    assert response.json()["data"]["access_token"] == "new_access_token"
    assert response.json()["message"] == "new access token"


def test_refresh_token_invalid_token(client, mocker):
    mocker.patch(
        "app.api.routes.auth.service.new_access_token",
        side_effect=HTTPException(status_code=401, detail="Invalid token")
    )
    response = client.get("/api/auth/refresh-token", headers={"Authorization": "Bearer invalid_refresh_token"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


def test_refresh_token_missing_token(client):
    response = client.get("/api/auth/refresh-token")
    assert response.status_code == 403


# test for "/api/auth/sign-out"
def sign_out_success(client, mocker):
    mocker.patch("app.api.routes.auth.service.sign_out", return_value=None)
    response = client.post("/api/auth/sign-out", headers={"Authorization": "Bearer mocked_token"})
    assert response.status_code == 200


def sign_out_invalid_token(client, mocker):
    mocker.patch(
        "app.api.routes.auth.service.sign_out",
        side_effect=HTTPException(status_code=401, detail="Invalid token")
    )
    response = client.post("/api/auth/sign-out", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


def sign_out_missing_token(client):
    response = client.post("/api/auth/sign-out")
    assert response.status_code == 403
