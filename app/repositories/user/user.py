from app.models.users import User
from app.repositories.sqlalchemy import SQLAlchemyRepository
from app.repositories.user.base import UserRepositoryABC


class UserRepository(SQLAlchemyRepository[User], UserRepositoryABC):
    """*User repository implementation.*"""

    model = User

    async def get_by_email(self, email: str) -> User | None:
        """*Returns the user registered with the given email address.*

        Returns:
            User | None: the user or `None` if nobody uses this email.
        """
        return await self.get_one(email=email)

    async def get_by_phone_number(self, phone_number: str) -> User | None:
        """*Returns the user registered with the given phone number.*

        Returns:
            User | None: the user or `None` if nobody uses this phone number.
        """
        return await self.get_one(phone_number=phone_number)
