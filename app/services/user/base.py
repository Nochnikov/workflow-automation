from typing import Protocol

from app.schemas.user.request.user_data_request import UserDataRequestDTO
from app.schemas.user.response.response import UserDataFillingResponse


class UserServiceProtocol(Protocol):
    """*Contract of the user service.*"""

    async def filling_user_anketa_data(self, data: UserDataRequestDTO) -> UserDataFillingResponse:
        """*Fills in the user anketa data in order to create their profile.*"""
        ...
