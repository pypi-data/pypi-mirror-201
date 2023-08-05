from pydantic import BaseModel


class Voice(BaseModel):

    voice: str
    price: float
    pro: bool
    sex: str
