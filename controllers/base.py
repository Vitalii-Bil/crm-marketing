from pydantic_models.common import SignInRequest
from abstract.controller_abc import BaseControllerAbstract


class BaseController(BaseControllerAbstract):
    _cognito_manager = None

    async def sign_in(self, sign_in_data: SignInRequest):
        access_token = await self._cognito_manager.manager_sign_in(sign_in_data.email, sign_in_data.password)
        return {"access_token": access_token}
