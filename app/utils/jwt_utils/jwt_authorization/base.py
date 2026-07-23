from abc import ABC, abstractmethod
from typing import Any


class JWTAuthProviderABC(ABC):
    @abstractmethod
    async def get_claims(self) -> Any:
        raise NotImplementedError()

    @abstractmethod
    async def get_user_id(self) -> int:
        raise NotImplementedError()
