from typing import Protocol


class UserServiceProtocol(Protocol):
    """*Contract of the user service.*"""

    async def filling_user_anketa_data(self, data: dict):
        """*Fills in the user anketa data in order to create their profile.*"""
        ...
