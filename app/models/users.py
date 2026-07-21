from sqlalchemy import String, false
from sqlalchemy import Enum as PgEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.postgres import Base
from app.enums.user_enums import UserAnketaStatus

NAME_MAX_SIZE = 10
PHONE_NUMBER_MAX_SIZE = 10


class User(Base):
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
    hashed_password: Mapped[str] = mapped_column(
        nullable=True,
        comment='Password of Employee',
        default=None,
    )

    status: Mapped[str] = mapped_column(
        PgEnum(
            UserAnketaStatus,
            name='status_enum',
            server_default=UserAnketaStatus.pending.value,
            native_enum=False,
            validate_strings=True,
        ),
        nullable=False,
        comment='Status of Employee Anketa',
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
        server_default=false(),
    )
    is_manager: Mapped[bool] = mapped_column(
        comment='Is Employee Admin',
        server_default=false(),
    )
