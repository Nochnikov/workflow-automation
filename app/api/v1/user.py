from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter

from app.services.user.base import UserServiceProtocol

router = APIRouter()


@router.post(
    '/filling-user-data',
    summary='Filling user related data in order to create their profile.',
    description='**Filling user related data in order to create their profile.**',
)
@inject
async def filling_user_anketa_data(
    *,
    service: FromDishka[UserServiceProtocol]

):
    return {'status': 'ok'}
