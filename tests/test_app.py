"""Tests for the FastAPI app using Arrange-Act-Assert pattern."""


def test_get_root_serves_index(client):
    # Arrange: client fixture (TestClient) provided by conftest

    # Act
    resp = client.get("/", follow_redirects=True)

    # Assert
    assert resp.status_code == 200
    content_type = resp.headers.get("content-type", "")
    assert "text/html" in content_type


def test_get_activities_returns_expected_keys(client):
    # Arrange: client fixture

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_post_signup_adds_student(client):
    # Arrange
    activity = "Chess Club"
    email = "new_student@mergington.edu"

    # Ensure not already signed up
    initial = client.get("/activities").json()
    assert email not in initial[activity]["participants"]

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]


def test_delete_signup_removes_student(client):
    # Arrange
    activity = "Chess Club"
    email = "removable_student@mergington.edu"

    # Ensure student is present by signing up first
    post_resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert post_resp.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]

    # Act
    del_resp = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert del_resp.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]
