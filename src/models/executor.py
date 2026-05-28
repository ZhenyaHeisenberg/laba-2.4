from src.models.task import Task
from src.models.task_queue import TaskQueue

import asyncio

from src.models.handlers.email import EmailHandler
from src.models.handlers.encryption import EncryptionHandler
from src.models.handlers.http import HttpHandler

import logging

logger = logging.getLogger(__name__)


class Executor:
    """Асинхронный исполнитель задач"""
    
    def __init__(self, source=None):
        self.queue = TaskQueue.create_from(source) if source else TaskQueue(iter([]))
        self._handlers = {
            "email": EmailHandler(),
            "encryption": EncryptionHandler(),
            "http": HttpHandler()
        }
    
    
    def get_handler(self, task: Task):
        """Возвращает обработчик для задачи по ее типу"""
        task_type = getattr(task, 'type', 'default')
        
        if task_type not in self._handlers:
            logger.error(f"No handler for task type: {task_type}")
            raise ValueError(f"No handler for task type: {task_type}")
        
        handler = self._handlers[task_type]
        return handler.handle 
    
    
    async def run(self, max_concurrent: int = 5):
        """Запускает асинхронное выполнение всех задач"""
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process(task: Task):
            async with semaphore:
                handler = self.get_handler(task)
                return await handler(task)
        
        tasks = [process(task) for task in self.queue]
        
        await asyncio.gather(*tasks)
        logger.info("Выполнение завершено")