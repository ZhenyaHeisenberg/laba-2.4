from uuid import uuid4
from collections.abc import Iterable
from dataclasses import dataclass

from src.contracts.message import Message
from src.sources.repository import register_source
from ..constants import STATUSES

from random import randint

import logging
from ..common.config import LOGGING_CONFIG
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class ApiSource:
    count: int = 5 # Количество запросов
    name: str = "api"
    
    
    def api_call(self) -> list[dict]:
        """Имитация запроса к API"""
        logger.info(f"{self.name}: Выполняется запрос к API")
        
        
        result = []
        for i in range(self.count):
            result.append({
                "id": str(uuid4()),
                "title": f"API Task {i}",
                "description": f"API Task: {i}",
                "author": "System",
                "message": f"Auto-generated message #{i}",
                "status": STATUSES[randint(0, len(STATUSES)-1)],
                "priority": randint(1, 5)
            })
        logger.info(f"{self.name}: API вернул сообщение")
        return result
    
    
    
    

    def fetch(self) -> Iterable[Message]:
        try:
            response = self.api_call()
            
            for item in response:
                yield Message(
                    id=item["id"],
                    title=item["title"],
                    description=item["description"],
                    author=item["author"],
                    message=item["message"],
                    status=item["status"],
                    priority=item["priority"]
                    
                )
            
            
        except Exception as e:
            print(f"Ошибка запроса: {e}")
            logger.error(f"Ошибка запроса: {e}")
            return


@register_source("api")
def create_api_source(count: int) -> ApiSource:
    return ApiSource(count=count)
