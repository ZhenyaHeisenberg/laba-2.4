from .descriptors import IdDescriptor, DescriptionDescriptor, PriorityDescriptor, StatusDescriptor, CreationTimeDescriptor
from src.constants import READY
from datetime import datetime


class Task:

    id = IdDescriptor()
    description = DescriptionDescriptor()
    priority = PriorityDescriptor()
    status = StatusDescriptor()
    creationTime = CreationTimeDescriptor()
    
    def __init__(self, id: str, description: str, priority: int, status: str):
        self.id = id
        self.description = description
        self.priority = priority
        self.status = status
    
    @property
    def is_ready(self) -> bool:
        return self.status.lower() in READY
    
    @property
    def time_in_queue(self) -> float:
        if self.status.lower() not in READY:
            return 0.0
        return abs((datetime.now() - self.creationTime).total_seconds() / 60)