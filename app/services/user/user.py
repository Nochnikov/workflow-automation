from app.schemas.user.request.user_data_request import UserDataRequestDTO
from app.schemas.user.response.response import UserDataFillingResponse
from app.services.user.base import UserServiceProtocol


class UserService(UserServiceProtocol):
    """*User service implementation.*"""

    async def filling_user_anketa_data(self, data: UserDataRequestDTO) -> UserDataFillingResponse:
        """*Fills in the user anketa data in order to create their profile.*"""

        pass
