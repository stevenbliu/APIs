from sqlmodel import SQLModel


class ModelRequest(SQLModel):
    prompt: str
    max_tokens: int
    temperature: float
