from pydantic import BaseModel

class Commit(BaseModel):
    author: str
    message: str
