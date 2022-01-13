from pydantic import BaseModel


class ContentBase(BaseModel):
    position: int
    type: str
    value: str

