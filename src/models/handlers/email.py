from src.models.task import Task
import asyncio
import logging

logger = logging.getLogger(__name__)


class EmailHandler:
    """Обработчик для задач типа 'email'"""
    
    async def handle(self, task: Task) -> dict:
        logger.info(f"Отправка email: {task.description}")
        
        await asyncio.sleep(0.5)
        
        result = {
            "status": "sent",
            "task_id": task.id,
            "message": task.description
        }
        
        logger.info(f"Email отправлен: {task.id}")
        return result
