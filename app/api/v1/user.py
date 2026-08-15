from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter

from app.schemas.user.request.user_data_request import UserDataRequestDTO
from app.services.user.base import UserServiceProtocol

router = APIRouter()


@router.post(
    '/filling-user-data',
    summary='Filling user related data in order to create their profile.',
    description='**Filling user related data in order to create their profile.**',
)
@inject
async def filling_user_anketa_data(
    *, service: FromDishka[UserServiceProtocol], requested_data: UserDataRequestDTO
):
    """*Fills in the user related data in order to create their profile.*

    Returns:
        dict: operation status.
    """
    return {'status': 'ok'}
