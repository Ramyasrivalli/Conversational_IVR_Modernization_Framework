from pydantic import BaseModel

class UserInput(BaseModel):
    session_id: str
    caller_id: str
    message: str