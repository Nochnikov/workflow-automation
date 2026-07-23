from typing import Protocol


class UserServiceProtocol(Protocol):

    async def filling_user_anketa_data(self, data: dict):
        ...