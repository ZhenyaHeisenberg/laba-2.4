from collections.abc import Sequence, Iterable

from src.contracts.message import Message
from src.contracts.message_source import MessageSource
from src.models.task import Task
from src.models.task_queue import TaskQueue


class InboxApp:
    def __init__(self, sources: Sequence[MessageSource] = None):
        self._sources = sources or []
        for source in sources:
            if not isinstance(source, MessageSource):
                raise TypeError(
                    f"Объект {source} не соответствует контракту MessageSource.\n"
                    f"Требуются атрибут 'name' и метод 'fetch'\n"
                    f"Получено: {type(source)}\n"
                )
                
        self._task_queue = self.build_task_queue()
    
    def convert_message_to_task(self, msg: Message) -> Task:
        return Task(
            id=msg.id,
            description=msg.description,
            priority=int(msg.priority),
            status=msg.status
        )

    def build_task_queue(self) -> TaskQueue:
        def task_generator():
            for source in self._sources:
                for msg in source.fetch():
                    yield self.convert_message_to_task(msg)
        
        return TaskQueue(task_generator())
    
    
    def iter_messages(self) -> Iterable[Message]:
        for task in self._task_queue:
            yield Message(
                id=task.id,
                title=f'Task with id: {task.id}',
                description=task.description,
                author="System",
                message=task.description,
                priority=task.priority,
                status=task.status
            )
    
    def get_task_queue(self) -> TaskQueue:
        return self._task_queue