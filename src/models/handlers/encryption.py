from src.models.task import Task
import asyncio
import logging

logger = logging.getLogger(__name__)


def CaesarCipher(text: str, key: int = 100) -> str: # Шифратор Цезаря
    
    result = ""
    
    for index in range(len(text)):
        result += chr(ord(text[index]) + key) # Сдвиг на key символов Unicode
        
    return result


class EncryptionHandler:
    """Обработчик для задач типа 'encryption'"""
    
    async def handle(self, task: Task) -> dict:
        logger.info(f"Шифрование: {task.description}")
        
        await asyncio.sleep(0.5)
        
        result = {
            "status": "completed",
            "task_id": task.id,
            "message": CaesarCipher(task.description, 500),
            "key": 500
        }
        
        logger.info(f"Текст зашифрован: {task.id}")
        return result
