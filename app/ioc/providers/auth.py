from dishka import Provider, from_context, Scope, provide
from fastapi import Request


class AuthProvider(Provider):

    scope = Scope.REQUEST

    request = from_context(provides=Request, scope=scope)
