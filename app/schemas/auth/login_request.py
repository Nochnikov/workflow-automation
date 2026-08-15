from pydantic import BaseModel


class LoginRequest(BaseModel):
    """*Credentials submitted to the authorization endpoint.*"""

    email: str
    password: str
