from pydantic import BaseModel


class MessageData(BaseModel):
    username: str
    message: str
    project:int