from src.models.task import Task
import asyncio
import logging
import random

logger = logging.getLogger(__name__)

random.seed(42)

def get_random_status_code():
    result = random.randint(1, 10)
    if result > 2:
        return 200
    elif result == 2:
        return 404
    else:
        return 501


class HttpHandler:
    """Обработчик для задач типа 'http'"""
    
    async def handle(self, task: Task) -> dict:
        logger.info(f"Отправка http запроса: {task.description}")
        
        await asyncio.sleep(0.5)
        
        result = {
            "status": "completed",
            "task_id": task.id,
            "message": task.description,
            "response_code": get_random_status_code()
        }
        
        logger.info(f"Запрос отправлен: {task.id}, response_code: {result['response_code']}")
        return result
