import json
import os
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional


class JsonTaskRepository:
    """JSON file storage with atomic writes and thread safety."""

    def __init__(self, path: str = "storage/tasks.json") -> None:
        self._path = Path(path)
        self._lock = threading.RLock()
        self._ensure_dir()

    def _ensure_dir(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def _read(self) -> List[Dict[str, Any]]:
        with self._lock:
            if not self._path.exists():
                with open(self._path, "w", encoding="utf-8") as w:
                    json.dump([], w)
                return []

            try:
                with open(self._path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data if isinstance(data, list) else []
            except json.JSONDecodeError:
                backup = self._path.with_suffix(".bak")
                try:
                    os.replace(self._path, backup)
                except OSError:
                    pass
                with open(self._path, "w", encoding="utf-8") as w:
                    json.dump([], w)
                return []

    def _write(self, tasks: List[Dict[str, Any]]) -> None:
        with self._lock:
            tmp = self._path.with_suffix(".tmp")
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(tasks, f, indent=4)
            os.replace(tmp, self._path)

    def save_all(self, tasks: List[Dict[str, Any]]) -> None:
        self._write(tasks)

    def list_all(self) -> List[Dict[str, Any]]:
        return self._read()

    def get_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        for t in self._read():
            if t.get("id") == task_id:
                return t
        return None

    def next_id(self) -> int:
        ids = [t.get("id", 0) for t in self._read() if isinstance(t.get("id"), int)]
        return max(ids, default=0) + 1

    def add(self, task: Dict[str, Any]) -> Dict[str, Any]:
        with self._lock:
            tasks = self._read()
            tasks.append(task)
            self._write(tasks)
            return task

    def update(self, task_id: int, fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        with self._lock:
            tasks = self._read()
            for t in tasks:
                if t.get("id") == task_id:
                    t.update(fields)
                    self._write(tasks)
                    return t
        return None

    def update_toggle(self, task_id: int) -> Optional[Dict[str, Any]]:
        with self._lock:
            tasks = self._read()
            for t in tasks:
                if t.get("id") == task_id:
                    t["feito"] = not t.get("feito", False)
                    self._write(tasks)
                    return t
        return None

    def delete(self, task_id: int) -> Optional[Dict[str, Any]]:
        with self._lock:
            tasks = self._read()
            for i, t in enumerate(tasks):
                if t.get("id") == task_id:
                    removed = tasks.pop(i)
                    self._write(tasks)
                    return {"id": task_id, "tarefa": removed.get("tarefa", "")}
        return None


repository = JsonTaskRepository()
