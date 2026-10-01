from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_service
from app.core.exceptions import TaskNotFoundError
from app.schemas.task import Task, TaskCreate, TaskList, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])


@router.get("", response_model=TaskList)
def list_tasks(
    search: Optional[str] = Query(default=None, max_length=100),
    is_done: Optional[bool] = Query(default=None),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    service: TaskService = Depends(get_service),
):
    """List tasks with optional filters."""
    return service.list_tasks(search=search, is_done=is_done, page=page, size=size)


@router.get("/stats")
def task_stats(service: TaskService = Depends(get_service)):
    """Return task counters."""
    return service.stats()


@router.post("", response_model=Task, status_code=201)
def create_task(
    payload: TaskCreate,
    service: TaskService = Depends(get_service),
):
    """Create a new task."""
    return service.create(title=payload.title)


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, service: TaskService = Depends(get_service)):
    """Get a single task by ID."""
    task = service.get_by_id(task_id)
    if task is None:
        raise TaskNotFoundError(task_id)
    return task


@router.patch("/{task_id}/done", response_model=Task)
def toggle_done(task_id: int, service: TaskService = Depends(get_service)):
    """Toggle task done status."""
    return service.toggle_done(task_id)


@router.patch("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    service: TaskService = Depends(get_service),
):
    """Update task title or done status."""
    return service.update_task(task_id, payload)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, service: TaskService = Depends(get_service)):
    """Delete a task by ID."""
    service.delete(task_id)
    return None
