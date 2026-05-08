def test_create_task(auth_client):
    resp = auth_client.post("/tasks/", json={"title": "Buy milk"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Buy milk"
    assert data["status"] == "todo"


def test_list_tasks(auth_client):
    auth_client.post("/tasks/", json={"title": "Task 1"})
    auth_client.post("/tasks/", json={"title": "Task 2"})
    resp = auth_client.get("/tasks/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_update_task_status(auth_client):
    task_id = auth_client.post("/tasks/", json={"title": "Task"}).json()["id"]
    resp = auth_client.patch(f"/tasks/{task_id}", json={"status": "in_progress"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "in_progress"


def test_delete_task(auth_client):
    task_id = auth_client.post("/tasks/", json={"title": "Task"}).json()["id"]
    resp = auth_client.delete(f"/tasks/{task_id}")
    assert resp.status_code == 204
    assert auth_client.get("/tasks/").json() == []


def test_task_isolation(client):
    """Tasks of one user should not be visible to another."""
    client.post("/auth/register", json={"email": "alice@test.com", "password": "pass"})
    client.post("/auth/register", json={"email": "bob@test.com", "password": "pass"})

    def login(email):
        r = client.post("/auth/login", data={"username": email, "password": "pass"})
        return r.json()["access_token"]

    alice_token = login("alice@test.com")
    bob_token = login("bob@test.com")

    client.headers.update({"Authorization": f"Bearer {alice_token}"})
    client.post("/tasks/", json={"title": "Alice task"})

    client.headers.update({"Authorization": f"Bearer {bob_token}"})
    resp = client.get("/tasks/")
    assert resp.json() == []


def test_unauthorized_access(client):
    resp = client.get("/tasks/")
    assert resp.status_code == 401
