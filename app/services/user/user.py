from app.schemas.user.request.user_data_request import UserDataRequestDTO
from app.schemas.user.response.response import UserAnketaFillingResponse
from app.services.user.base import UserServiceProtocol


class UserService(UserServiceProtocol):
    """*User service implementation.*"""

    def filling_user_anketa_data(self, data: UserDataRequestDTO) -> UserAnketaFillingResponse:
        """*Fills in the user anketa data in order to create their profile.*"""

        pass
