from pydantic import BaseModel

class Usage(BaseModel):
    inputTokens: int 
    outputTokens: int

class Response(BaseModel):
    user_question: str
    answer: str
    usage: list[Usage]
    sources: str