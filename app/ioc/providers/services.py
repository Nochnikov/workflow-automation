from dishka import Provider, provide

from app.services.auth.user_service import UserService
from app.services.user.base import UserServiceProtocol


class ServiceProvider(Provider):

    @provide
    def user_service(self) -> UserServiceProtocol:
        return UserService()