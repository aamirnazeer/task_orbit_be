from fastapi import HTTPException


# tests for "/api/boards/create-board"
def test_create_board_success(client, mocker):
    mocker.patch(
        "app.api.routes.boards.handler.read_token",
        return_value={"id": 1},
    )
    board_data = {"board_name": "Test Board"}
    response = client.post(
        "/api/boards/create-board",
        json=board_data,
        headers={"Authorization": "Bearer mocked_token"},
    )
    assert response.status_code == 201
    assert response.json()["data"]["board_name"] == "Test Board"
    assert response.json()["message"] == "board added successfully"


def test_create_board_invalid_token(client, mocker):
    mocker.patch(
        "app.api.routes.boards.handler.read_token",
        side_effect=HTTPException(status_code=401, detail="Invalid token"),
    )
    board_data = {"board_name": "Test Board"}
    response = client.post(
        "/api/boards/create-board",
        json=board_data,
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


def test_create_board_missing_token(client):
    board_data = {"board_name": "Test Board"}
    response = client.post("/api/boards/create-board", json=board_data)
    assert response.status_code == 403


def test_create_board_missing_field(client):
    board_data = {}
    response = client.post(
        "/api/boards/create-board",
        json=board_data,
        headers={"Authorization": "Bearer mocked_token"},
    )
    assert response.status_code == 422
