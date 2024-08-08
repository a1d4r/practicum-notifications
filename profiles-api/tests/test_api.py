from uuid import uuid4

from starlette.testclient import TestClient

from profiles_api.main import app

client = TestClient(app)


def test_get_user_profile():
    # Arrange
    user_id = uuid4()

    # Act
    response = client.get(f"/profiles/{user_id}")

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert body["user_id"] == str(user_id)
    assert body["first_name"]
    assert body["last_name"]
    assert body["email"]
    assert body["timezone"]
    assert body["notification_preferences"]


def test_get_user_profiles():
    # Arrange
    group_id = uuid4()

    # Act
    response = client.get(f"/groups/{group_id}/profiles")

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert len(body["profiles"]) == body["total"]
    assert body["profiles"][0]["user_id"]
    assert body["profiles"][0]["first_name"]
    assert body["profiles"][0]["last_name"]
    assert body["profiles"][0]["email"]
    assert body["profiles"][0]["timezone"]
    assert body["profiles"][0]["notification_preferences"]
