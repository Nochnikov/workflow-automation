from dishka import FromDishka
from fastapi import APIRouter
from fastapi import Request

from app.schemas.auth.LoginRequest import LoginRequest
from app.schemas.tokens import TokenResponse
from app.service.auth.base import AuthServiceProvider

router = APIRouter()

@router.post(
    '/login',
    description='*Authorization endpoint*',
    summary='Authorization endpoint',
    response_model=TokenResponse,
)
async def login(
    *,
    service: FromDishka[AuthServiceProvider],
    request: Request,
    login_dto: LoginRequest
):
    pass