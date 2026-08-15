from pydantic import BaseModel


class UserAnketaFillingResponse(BaseModel):
    """*Result of filling in the user anketa data.*"""

    message: str
    status_code: str
