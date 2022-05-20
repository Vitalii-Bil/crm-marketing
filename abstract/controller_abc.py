from abc import ABC, abstractmethod


class BaseControllerAbstract(ABC):

    @abstractmethod
    async def sign_in(self, sign_in_data):
        pass
