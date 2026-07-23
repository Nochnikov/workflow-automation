from abc import ABC, abstractmethod


class JWTHandlerABC(ABC):
    @abstractmethod
    def create_access_token(self, user_id: int, claims: dict) -> tuple[str, str]:
        raise NotImplementedError()

    @abstractmethod
    def create_refresh_token(self, user_id: int, access_jti: str) -> tuple[str, str]:
        raise NotImplementedError()
