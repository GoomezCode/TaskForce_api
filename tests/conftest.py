import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_service
from app.main import create_app
from app.repositories.json_task_repository import JsonTaskRepository
from app.services.task_service import TaskService


@pytest.fixture()
def client(tmp_path):
    repo = JsonTaskRepository(path=str(tmp_path / "tasks.json"))
    app = create_app()
    app.dependency_overrides[get_service] = lambda: TaskService(repo=repo)
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
