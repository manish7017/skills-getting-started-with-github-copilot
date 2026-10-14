def test_get_activities_returns_data_without_cache(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert "Chess Club" in response.json()
    assert response.headers["cache-control"] == "no-store"


def test_signup_adds_participant(client):
    activity = "Basketball Team"
    email = "new-student@mergington.edu"

    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}
    assert email in client.get("/activities").json()[activity]["participants"]


def test_signup_rejects_unknown_activity(client):
    response = client.post(
        "/activities/Unknown/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_rejects_duplicate_participant(client):
    activity = "Basketball Team"
    email = "student@mergington.edu"
    client.post(f"/activities/{activity}/signup", params={"email": email})

    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_removes_participant(client):
    activity = "Basketball Team"
    email = "student@mergington.edu"
    client.post(f"/activities/{activity}/signup", params={"email": email})

    response = client.delete(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity}"}
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_unregister_rejects_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_rejects_unregistered_participant(client):
    activity = "Basketball Team"
    response = client.delete(
        f"/activities/{activity}/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
