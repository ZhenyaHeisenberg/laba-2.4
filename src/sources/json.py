import json
import uuid
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.contracts.message import Message
from src.sources.repository import register_source

import logging
from ..common.config import LOGGING_CONFIG
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)



def parse_json_file(line: str, path: str, line_no: int) -> dict[str, Any]:
    try:
        return json.loads(line)
    except json.JSONDecodeError as error:
        logger.error(f"Bad JSON at {path}:{line_no}: {error}")
        raise ValueError(f"Bad JSON at {path}:{line_no}: {error}") from error


@dataclass(frozen=True)
class JsonlSource:
    path: Path
    name: str = "file-jsonl"

    def fetch(self) -> Iterable[Message]:
        with self.path.open("r", encoding="utf-8") as file:
            for line_no, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                message = parse_json_file(line, str(self.path), line_no)
                message_id = str(message.get("id", f"{self.path.name}:{line_no}"))
                message_title = message.get("title", "")
                message_author = message.get("author", "")
                message_content = message.get("content", "")
                status_content = message.get("content", "")
                priority_content = message.get("content", "")
                yield Message(
                    id=message_id,
                    title=message_title,
                    author=message_author,
                    message=message_content,
                    status=status_content,
                    priority=priority_content
                )
                logger.info(f"{self.name}: Сообщение получено")



@register_source("file-jsonl")
def create_json_source(path: Path) -> JsonlSource:
    return JsonlSource(path=path)