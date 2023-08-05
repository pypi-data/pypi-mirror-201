from io import BytesIO
from typing import Optional, BinaryIO

from aiohttp import ClientSession
from pydantic import BaseModel, Field


class Audio(BaseModel):

    id: int
    status: int
    error: Optional[str] = None
    
    file: Optional[str] = None
    cuts: list[str] = []
    
    parts: int = 0
    parts_done: int = 0
    duration: int = 0
    format: str

    balance: float = Field(..., alias='balans')
    cost: float = None

    async def download(self, file: Optional[str]=None) -> Optional[BinaryIO]:

        if not file:

            file = BytesIO()

        else:

            file = open(file, 'wb')

        async with ClientSession() as session:
            
            async with session.get(self.file) as response:

                async for chunk in response.content.iter_chunked(1024):

                    file.write(chunk)

        if not isinstance(file, BytesIO):
            
            return file.close()
                    
        file.seek(0)
        return file