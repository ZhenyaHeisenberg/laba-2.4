from src.sources.api import ApiSource
from src.models.executor import Executor
import asyncio

async def main():
    api = ApiSource(count=5)
    
    executor = Executor(api)
    
    await executor.run(max_concurrent=3)
    
    print("all tasks done")

if __name__ == "__main__":
    asyncio.run(main())