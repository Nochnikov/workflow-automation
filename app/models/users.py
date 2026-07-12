from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.postgres import Base

NAME_MAX_SIZE = 10
PHONE_NUMBER_MAX_SIZE = 10


class Users(Base):
    __tablename__ = 'users'

    __table_args__ = {'schema': 'application'}

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    first_name: Mapped[str] = mapped_column(
        String(
            length=NAME_MAX_SIZE,
        ),
        comment='First Name of Employee',
        nullable=False,
    )
    last_name: Mapped[str] = mapped_column(
        String(
            length=NAME_MAX_SIZE,
        ),
        comment='Last Name of Employee',
        nullable=False,
    )
    phone_number: Mapped[str] = mapped_column(
        String(
            length=PHONE_NUMBER_MAX_SIZE,
        ),
        comment='Phone number of Employee',
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        comment='Email Address of Employee',
        nullable=False,
    )
    position: Mapped[str] = mapped_column(
        comment='Position of Employee',
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        comment='Is Employee Active',
        nullable=False,
        default=True,
    )
    is_manager: Mapped[bool] = mapped_column(
        comment='Is Employee Admin',
        default=False,
    )
