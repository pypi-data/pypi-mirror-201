from typing import Awaitable
from functools import wraps


class ZvukoGramError(Exception):
    """Base class for all ZvukoGram exceptions"""

    def __init__(self, message: str):
        
        self.message = message

        super().__init__(message)


def raise_for_status(func: Awaitable):

    @wraps(func)
    async def wrapper(*args, **kwargs):
        
        response = await func(*args, **kwargs)
        
        if error := response.get('error'):

            raise ZvukoGramError(error)

        return response
    
    return wrapper
