from app.models import User
from app.repositories.base import Repository
from app.schemas.user.request.user_data_request import UserDataRequestDTO


class UsersRepository(Repository[User, UserDataRequestDTO, UserDataRequestDTO]):
    """*Repository of the employee accounts.*"""

    async def get_by_email(self, email: str) -> User | None:
        """*Returns the user registered with the given email address.*

        Returns:
            User | None: the user or `None` if nobody uses this email.
        """
        return await self.get_by_field(email=email)

    async def get_by_phone_number(self, phone_number: str) -> User | None:
        """*Returns the user registered with the given phone number.*

        Returns:
            User | None: the user or `None` if nobody uses this phone number.
        """
        return await self.get_by_field(phone_number=phone_number)
