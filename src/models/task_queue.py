from typing import Iterator
from src.models.task import Task

class TaskIterator:
    def __init__(self, source: Iterator[Task], buffer: list):
        self._iterator = iter(source) if source else None
        self._buffer = buffer
        self._position = 0
        self._finished = False
    
    def __iter__(self):
        return self
    
    def __next__(self) -> Task:
        if self._position < len(self._buffer):
            task = self._buffer[self._position]
            self._position += 1
            return task
        
        if not self._finished and self._iterator:
            try:
                task = next(self._iterator)
                self._buffer.append(task)
                self._position += 1
                return task
            except StopIteration:
                self._finished = True
        
        raise StopIteration

class TaskQueue:
    def __init__(self, source: Iterator[Task]):
        self._source = source
        self._buffer = []
    
    @classmethod
    def create_from(cls, source) -> "TaskQueue":
        """
        Создает очередь из api, json, sdin или generator.
        """
        def convert():
            if hasattr(source, 'fetch'):
                iterator = source.fetch()
            elif hasattr(source, 'generate'):
                iterator = source.generate()
            else:
                raise TypeError(f"Источник {type(source)} не поддерживает итерацию")
            for item in iterator:
                yield Task(
                    id=item.id,
                    description=getattr(item, "description"),
                    priority=getattr(item, "priority"),
                    status=getattr(item, "status")
                )
        return cls(convert())
    
    def __iter__(self) -> TaskIterator:
        return TaskIterator(self)
    
    def filter_by_status(self, status: str) -> "TaskQueue":
        def filtered():
            for task in self:
                if task.status == status:
                    yield task
        return TaskQueue(filtered())
    
    def filter_by_priority(self, min_priority: int = 1, max_priority: int = 5) -> "TaskQueue":
        def filtered():
            for task in self:
                if min_priority <= task.priority <= max_priority:
                    yield task
        return TaskQueue(filtered())
    
    def take(self, n: int) -> "TaskQueue":
        """
        Берет первые n задач.
        """
        def taked():
            count = 0
            for task in self:
                if count >= n:
                    break
                yield task
                count += 1
        return TaskQueue(taked())
    
    def __len__(self) -> int:
        return sum(1 for _ in self)