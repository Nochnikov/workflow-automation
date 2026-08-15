from dishka import AsyncContainer, make_async_container

from app.ioc.providers.auth import AuthProvider
from app.ioc.providers.database import DatabaseProvider
from app.ioc.providers.services import ServiceProvider


def create_container() -> AsyncContainer:
    """*Builds the application dependency injection container.*

    Returns:
        AsyncContainer: configured dishka container.
    """
    return make_async_container(DatabaseProvider(), ServiceProvider(), AuthProvider())
