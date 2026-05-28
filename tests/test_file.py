from src.models.task import Task
from src.models.task_queue import TaskQueue
from src.models.executor import Executor

from src.models.handlers.email import EmailHandler
from src.models.handlers.http import HttpHandler
from src.models.handlers.encryption import EncryptionHandler
from src.models.handlers.encryption import CaesarCipher

from uuid import uuid4
import asyncio

from pytest import raises


def test_executor_get_handler_good_type():
    executor = Executor(source=None)
    
    task = Task(
        id=str(uuid4()),
        type="email",
        description="test description",
        status="created",
        priority=5
    )
    
    handler = executor.get_handler(task)
    
    assert callable(handler)
    assert handler.__name__ == "handle"


def test_executor_get_handler_unknown_type():
    executor = Executor(source=None)
    
    task = Task(
        id=str(uuid4()),
        type="unknown_type",
        description="test description",
        status="created",
        priority=5
    )
    
    with raises(ValueError, match="No handler for task type: unknown_type"):
        executor.get_handler(task)


def test_executor_get_handler_for_email():
    executor = Executor(source=None)
    
    task = Task(
        id=str(uuid4()),
        type="email",
        description="send email",
        status="created",
        priority=3
    )
    
    handler = executor.get_handler(task)
    
    assert callable(handler)
    assert "EmailHandler" in str(handler)


def test_executor_get_handler_for_http():
    executor = Executor(source=None)
    
    task = Task(
        id=str(uuid4()),
        type="http",
        description="http request",
        status="created",
        priority=4
    )
    
    handler = executor.get_handler(task)
    
    assert callable(handler)
    assert "HttpHandler" in str(handler)


def test_executor_get_handler_for_encryption():
    executor = Executor(source=None)
    
    task = Task(
        id=str(uuid4()),
        type="encryption",
        description="encrypt the text",
        status="created",
        priority=5
    )
    
    handler = executor.get_handler(task)
    
    assert callable(handler)
    assert "EncryptionHandler" in str(handler)


def test_executor_run_no_errors():    
    
    task = Task(
        id=str(uuid4()),
        type="encryption",
        description="test description",
        status="created",
        priority=5
    )
    
    def generator():
        yield task
    
    queue = TaskQueue(generator())
        
    executor = Executor()
    executor.queue = queue
    
    async def run_test():
        await executor.run(max_concurrent=3)
    
    asyncio.run(run_test())


def test_send_email():
    task = Task(
        id=str(uuid4()),
        type="email",
        description="test description",
        status="created",
        priority=5
    )
    
    email_handler = EmailHandler()
    
    async def run_test():
        result = await email_handler.handle(task)
        return result
    
    result = asyncio.run(run_test())
    
    assert result == {
        "status": "sent",
        "task_id": task.id,
        "message": task.description
    }


def test_http_request():
    task = Task(
        id=str(uuid4()),
        type="http",
        description="test description",
        status="created",
        priority=5
    )
    
    http_handler = HttpHandler()
    async def run_test():
        result = await http_handler.handle(task)
        return result
    
    result = asyncio.run(run_test())
    assert result == {
            "status": "completed",
            "task_id": task.id,
            "message": task.description,
            "response_code": 404
        }
    
    result = asyncio.run(run_test())
    assert result == {
            "status": "completed",
            "task_id": task.id,
            "message": task.description,
            "response_code": 501
        }
    
    result = asyncio.run(run_test())
    assert result == {
            "status": "completed",
            "task_id": task.id,
            "message": task.description,
            "response_code": 200
        }


def test_encryptor():
    task = Task(
        id=str(uuid4()),
        type="encryption",
        description="test encryption",
        status="created",
        priority=5
    )
    
    encryption_handler = EncryptionHandler()
    
    async def run_test():
        result = await encryption_handler.handle(task)
        return result
    
    result = asyncio.run(run_test())
    
    assert result == {
        "status": "completed",
        "task_id": task.id,
        "message": CaesarCipher(task.description, 500),
        "key": 500
    }