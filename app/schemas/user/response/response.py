from pydantic import BaseModel


class UserDataFillingResponse(BaseModel):
    """*Result of filling in the user anketa data.*"""

    message: str
    status_code: str
