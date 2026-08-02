from dishka import AsyncContainer, make_async_container


def create_container() -> AsyncContainer:
    """*Builds the application dependency injection container.*

    Returns:
        AsyncContainer: configured dishka container.
    """
    return make_async_container()
