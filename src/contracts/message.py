import uuid
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Message:
    id: str
    title: str
    description: str
    author: str
    message: str
    status: str = "created"
    priority: int = 3