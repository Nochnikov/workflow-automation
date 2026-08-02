from pydantic import BaseModel


class UserDataRequestDTO(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
