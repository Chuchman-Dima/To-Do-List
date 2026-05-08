def test_register(client):
    resp = client.post("/auth/register", json={"email": "user@test.com", "password": "secret"})
    assert resp.status_code == 201
    assert resp.json()["email"] == "user@test.com"


def test_register_duplicate(client):
    client.post("/auth/register", json={"email": "user@test.com", "password": "secret"})
    resp = client.post("/auth/register", json={"email": "user@test.com", "password": "secret"})
    assert resp.status_code == 400


def test_login_success(client):
    client.post("/auth/register", json={"email": "user@test.com", "password": "secret"})
    resp = client.post("/auth/login", data={"username": "user@test.com", "password": "secret"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={"email": "user@test.com", "password": "secret"})
    resp = client.post("/auth/login", data={"username": "user@test.com", "password": "wrong"})
    assert resp.status_code == 401
