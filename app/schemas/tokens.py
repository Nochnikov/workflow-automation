from pydantic import BaseModel


class TokenResponse(BaseModel):
    """*Pair of JWT tokens returned after a successful authorization.*"""

    access_token: str
    refresh_token: str
