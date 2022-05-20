from abc import ABC, abstractmethod


class CognitoUserManagementAbstract(ABC):

    @abstractmethod
    def _manager_get_secret_hash(self, username):
        pass

    @abstractmethod
    async def manager_sign_up(self, user_email, user_password):
        pass

    @abstractmethod
    async def manager_confirm_sign_up(self, user_email):
        pass

    @abstractmethod
    async def manager_sign_in(self, user_email, user_password):
        pass
