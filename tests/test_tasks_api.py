def test_crud_flow(client):
    created = client.post("/api/v1/tasks", json={"title": "Estudar FastAPI"})
    assert created.status_code == 201, created.text
    task_id = created.json()["id"]

    listed = client.get("/api/v1/tasks")
    assert listed.status_code == 200, listed.text
    assert listed.json()["total"] == 1

    fetched = client.get(f"/api/v1/tasks/{task_id}")
    assert fetched.status_code == 200, fetched.text

    toggled = client.patch(f"/api/v1/tasks/{task_id}/done")
    assert toggled.status_code == 200, toggled.text
    assert toggled.json()["feito"] is True

    updated = client.patch(f"/api/v1/tasks/{task_id}", json={"title": "Estudar uvicorn"})
    assert updated.status_code == 200, updated.text
    assert updated.json()["tarefa"] == "Estudar uvicorn"

    deleted = client.delete(f"/api/v1/tasks/{task_id}")
    assert deleted.status_code == 204, deleted.text

    assert client.get(f"/api/v1/tasks/{task_id}").status_code == 404


def test_duplicate_returns_409(client):
    assert client.post("/api/v1/tasks", json={"title": "Duplicada"}).status_code == 201
    dup = client.post("/api/v1/tasks", json={"title": "duplicada"})
    assert dup.status_code == 409
