from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.core.exceptions import TaskAlreadyExistsError, TaskNotFoundError
from app.repositories.json_task_repository import JsonTaskRepository, repository
from app.schemas.task import Task, TaskList, TaskUpdate


class TaskService:
    """Business logic for task management."""

    def __init__(self, repo: JsonTaskRepository | None = None) -> None:
        self._repo = repo or repository

    def create(self, title: str) -> Task:
        cleaned = title.strip()
        normalized = cleaned.casefold()
        for t in self._repo.list_all():
            if str(t.get("tarefa", "")).strip().casefold() == normalized:
                raise TaskAlreadyExistsError(title=cleaned)

        new_task: Dict[str, Any] = {
            "id": self._repo.next_id(),
            "tarefa": cleaned,
            "feito": False,
            "data": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "hora": datetime.now(timezone.utc).strftime("%H:%M:%S"),
        }
        self._repo.add(new_task)
        return Task(**new_task)

    def get_all(self) -> List[Task]:
        return [Task(**t) for t in self._repo.list_all()]

    def list_tasks(
        self,
        search: Optional[str] = None,
        is_done: Optional[bool] = None,
        page: int = 1,
        size: int = 10,
    ) -> TaskList:
        """List tasks with optional filters and pagination."""
        tasks = self._repo.list_all()

        if search:
            needle = search.strip().lower()
            tasks = [t for t in tasks if needle in str(t.get("tarefa", "")).lower()]

        if is_done is not None:
            tasks = [t for t in tasks if bool(t.get("feito")) is is_done]

        total = len(tasks)
        start = (page - 1) * size
        page_items = [Task(**t) for t in tasks[start : start + size]]

        return TaskList(
            items=page_items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size if total > 0 else 0,
        )

    def get_by_id(self, task_id: int) -> Optional[Task]:
        task_dict = self._repo.get_by_id(task_id)
        return Task(**task_dict) if task_dict is not None else None

    def toggle_done(self, task_id: int) -> Task:
        task_dict = self._repo.update_toggle(task_id)
        if task_dict is None:
            raise TaskNotFoundError(task_id)
        return Task(**task_dict)

    def update_task(self, task_id: int, payload: TaskUpdate) -> Task:
        current = self._repo.get_by_id(task_id)
        if current is None:
            raise TaskNotFoundError(task_id)

        fields: Dict[str, Any] = {}
        if payload.title is not None:
            cleaned = payload.title.strip()
            normalized = cleaned.casefold()
            for t in self._repo.list_all():
                if t.get("id") != task_id and str(t.get("tarefa", "")).strip().casefold() == normalized:
                    raise TaskAlreadyExistsError(title=cleaned)
            fields["tarefa"] = cleaned
        if payload.done is not None:
            fields["feito"] = payload.done

        updated = self._repo.update(task_id, fields) if fields else current
        if updated is None:
            raise TaskNotFoundError(task_id)
        return Task(**updated)

    def delete(self, task_id: int) -> Dict[str, Any]:
        removed = self._repo.delete(task_id)
        if removed is None:
            raise TaskNotFoundError(task_id)
        return removed

    def stats(self) -> Dict[str, Any]:
        tasks = self._repo.list_all()
        total = len(tasks)
        done = sum(1 for t in tasks if t.get("feito"))
        return {"total": total, "done": done, "pending": total - done}
