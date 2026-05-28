# src/handlers/base.py
from typing import Protocol, Any
from src.models.task import Task
import asyncio


class TaskHandler(Protocol):
    """
    Протокол обработчика задач.
    """
    
    async def handle(self, task: Task) -> Any:
        """
        Асинхронная обработка задачи.
        
        Args:
            task: Задача для обработки
            
        Returns:
            Результат обработки (тип зависит от конкретного обработчика)
        """
        ...
    
    @property
    def supported_type(self) -> str:
        """Тип задач, которые обрабатывает этот обработчик."""
        ...