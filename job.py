import time
from enum import Enum
from typing import Any

from logger import logger


class JobStatus(str, Enum):
    """Статус задания."""

    COMPLETED = 'completed'
    RUNNING = 'running'
    WAITING = 'waiting'
    FAILED = 'failed'


class Job:
    """Задание."""

    def __init__(
            self,
            task_id: int,
            func: Any,
            duration: float | None = None,
            start_time: float | None = None,
            restarts: int = 0,
            max_restarts: int = 1,
            dependencies: list["Job"] | None = None,
            **kwargs: dict[Any, Any],
    ):
        self.task_id = task_id
        self.duration = duration
        self.start_time = start_time
        self.restarts = restarts
        self.max_restarts = max_restarts
        self.dependencies = dependencies or []
        self.status = JobStatus.WAITING
        self.func = func
        self.kwargs = kwargs

    def execute(self) -> None:
        """Выполняет задание."""
        logger.info("TASK %s: EXECUTE.", self.task_id)
        self.status = JobStatus.RUNNING
        if self.start_time:
            time.sleep(self.start_time)

        for _ in range(self.max_restarts + 1):
            try:
                coroutine = self.run()
                while True:
                    try:
                        next(coroutine)
                    except StopIteration:
                        break
                self.status = JobStatus.COMPLETED
                break
            except Exception as e:
                self.status = JobStatus.FAILED
                logger.error("TASK %s: %s ERROR %s", self.task_id, str(e))
        logger.info("TASK %s: SUCCESS.", self.task_id)

    def run(self) -> None:
        """Запускает задание."""
        logger.info("TASK %s: START.", self.task_id)
        if self.duration:
            time.sleep(self.duration)
        yield from self.func(**self.kwargs)
        logger.info("TASK %s: END.", self.task_id)
