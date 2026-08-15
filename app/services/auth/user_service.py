from app.services.user.base import UserServiceProtocol


class UserService(UserServiceProtocol):
    """*User service implementation.*"""

    async def filling_user_anketa_data(self, data: dict):
        """*Fills in the user anketa data in order to create their profile.*"""
        pass
