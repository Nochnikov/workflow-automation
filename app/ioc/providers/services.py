from dishka import Provider, provide

from app.services.auth.user_service import UserService
from app.services.user.base import UserServiceProtocol


class ServiceProvider(Provider):
    """*DI provider of the application service layer.*"""

    @provide
    def user_service(self) -> UserServiceProtocol:
        """*Creates the user service implementation.*

        Returns:
            UserServiceProtocol: service handling user profile operations.
        """
        return UserService()
