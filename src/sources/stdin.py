import sys
from collections.abc import Iterable
from dataclasses import dataclass
from typing import TextIO

from src.contracts.message import Message
from src.sources.repository import register_source

import logging
from ..common.config import LOGGING_CONFIG
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def extract_messages(lines: list[str], line_no: int) -> dict:
    try:
        return (
            lines[0].strip(),
            lines[1].strip(),
            lines[2].strip(),
            lines[3].strip(),
            lines[4].strip(),
            lines[5].strip(),
            int(lines[6].strip())
        )
    except IndexError:
        logger.error(f"Line: {line_no}. Message must contain at least 4 items, separated by ':' ")
        raise ValueError(
            f"Line: {line_no}. Message must contain at least 4 items, separated by ':' "
        )


@dataclass(frozen=True)
class StdinLineSource:
    stream: TextIO = sys.stdin
    name: str = "stdin"

    def fetch(self) -> Iterable[Message]:
        for line_no, line in enumerate(self.stream, start=1):
            lines = line.split(":")
            if not line.strip():
                continue
            id, title, description, author, message, status, priority = extract_messages(lines, line_no)
            yield Message(id=id,
                            title=title,
                            description=description,
                            author=author,
                            message=message,
                            status=status,
                            priority=int(priority)
                        )
            logger.info(f"{self.name}: Сообщение получено")


@register_source("stdin")
def create_source() -> StdinLineSource:
    return StdinLineSource()