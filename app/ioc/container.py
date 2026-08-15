from dishka import AsyncContainer, make_async_container

from app.ioc.providers.database import DatabaseProvider


def create_container() -> AsyncContainer:
    """*Builds the application dependency injection container.*

    Returns:
        AsyncContainer: configured dishka container.
    """
    return make_async_container(DatabaseProvider())
