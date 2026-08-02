from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Request

from app.schemas.auth.login_request import LoginRequest
from app.schemas.tokens import TokenResponse
from app.services.auth.base import AuthServiceProtocol

router = APIRouter()


@router.post(
    '/login',
    description='*Authorization endpoint*',
    summary='Authorization endpoint',
    response_model=TokenResponse,
)
@inject
async def login(
    *,
    service: FromDishka[AuthServiceProtocol],
    request: Request,
    login_dto: LoginRequest,
):
    """*Authorizes a user by email and password and issues a token pair.*

    Returns:
        TokenResponse: freshly issued access and refresh tokens.
    """
    pass
