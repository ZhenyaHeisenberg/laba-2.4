from src.sources.api import ApiSource
from src.models.task_queue import TaskQueue
from src.models.generator import Generator

def test_len():
    api = ApiSource(count=100)
    queue = TaskQueue.create_from(api)
    assert len(queue) == 100

def test_filter_by_priority():
    api = ApiSource(count=100)
    queue = TaskQueue.create_from(api)
    
    filtered = (queue.filter_by_priority(2, 4))
    for task in filtered:
        assert (task.priority >=2 and task.priority <= 4)

def test_filter_by_status():
    api = ApiSource(count=100)
    queue = TaskQueue.create_from(api)
    
    filtered = (queue.filter_by_status("created"))
    for task in filtered:
        assert task.status == "created"

    filtered = (queue.filter_by_status("completed"))
    for task in filtered:
        assert task.status == "completed"

def test_take_n_tasks():
    api = ApiSource(count=100)
    queue = TaskQueue.create_from(api)
    
    first_n_tasks = queue.take(20)
    assert len(first_n_tasks) == 20

def test_creating_bygenerator():
    gen = Generator(100)
    queue = TaskQueue.create_from(gen)
    assert len(queue) == 100