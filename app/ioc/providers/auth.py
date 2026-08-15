from async_fastapi_jwt_auth import AuthJWT
from dishka import Provider, Scope, from_context, provide
from fastapi import Request

from app.services.jwt_tokens.jwt_handler import JWTHandler
from app.utils.jwt_utils.jwt_authorization.base import JWTAuthProviderABC
from app.utils.jwt_utils.jwt_authorization.jwt_authorization import JWTAuthProvider


class AuthProvider(Provider):
    """*DI provider of the request scoped JWT authorization dependencies.*"""

    scope = Scope.REQUEST

    request = from_context(provides=Request, scope=scope)

    @provide(scope=scope)
    def auth_jwt(self, request: Request) -> AuthJWT:
        """*Creates the JWT authorization provider bound to the current request.*

        Returns:
            AuthJWT: authorization provider for the current request.
        """
        return JWTAuthProvider(req=request)

    @provide(scope=scope)
    def jwt_auth_provider(self, auth_jwt: AuthJWT) -> JWTAuthProviderABC:
        """*Exposes the JWT authorization provider behind its abstract interface.*

        Returns:
            JWTAuthProviderABC: authorization provider implementation.
        """
        return auth_jwt

    @provide(scope=scope)
    def jwt_handler(self, auth_jwt: AuthJWT) -> JWTHandler:
        """*Creates the token handler used to issue access and refresh tokens.*

        Returns:
            JWTHandler: token handler bound to the current request.
        """
        return JWTHandler(auth_jwt)
