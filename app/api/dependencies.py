from app.services.task_service import TaskService


def get_service() -> TaskService:
    return TaskService()
