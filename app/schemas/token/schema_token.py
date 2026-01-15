from pydantic import BaseModel

class Token(BaseModel):
    access_token: str # token gerado
    token_type: str # modelo de uso