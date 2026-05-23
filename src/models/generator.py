from uuid import uuid4
from typing import Iterable
from src.models.task import Task
from src.constants import STATUSES
from random import randint


class Generator:
    def __init__(self, count: int):
        self.count = count
        self.id = str(uuid4())
    
    def generate(self) -> Iterable[Task]:
        for _ in range(self.count):
            yield Task(
                id=str(uuid4()),
                description=f"Generated task with id: {self.id}",
                priority=randint(1, 5),
                status=STATUSES[randint(0, len(STATUSES)-1)],
            )