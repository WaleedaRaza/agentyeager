from typing import Callable, Any
from functools import wraps
import asyncio

class Skill:
    def __init__(self, name: str, func: Callable):
        self.name = name
        self.func = func
    
    async def execute(self, input_data: Any) -> Any:
        if asyncio.iscoroutinefunction(self.func):
            return await self.func(input_data)
        return self.func(input_data)

def skill(func: Callable) -> Skill:
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
    return Skill(name=func.__name__, func=wrapper)