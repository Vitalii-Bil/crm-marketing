from fastapi import APIRouter, Depends, Body, Header, Security, HTTPException
from fastapi.security import SecurityScopes
from sqlalchemy.ext.asyncio import AsyncSession

from controllers import client
from db.session import get_session
from pydantic_models import common
from user_management import cognito

router = APIRouter()
client_controller = client.ClientController()
cognito_manager = cognito.CognitoUserManagement()


async def get_sub_security(access_token: str = Header(...)):
    async def get_sub():
        try:
            return await cognito_manager.get_user_sub_from_token(access_token)
        except Exception:
            raise HTTPException(status_code=404, detail="Access token was not validated")
    return await get_sub()


@router.post("/client/sign_up/", tags=["client"])
async def sign_up(sign_up_data: common.ClientRegisterRequest, session: AsyncSession = Depends(get_session)):
    return await client_controller.client_sign_up(sign_up_data, session)


@router.post("/client/sign_in/", tags=["client"])
async def sign_in(sign_in_data: common.SignInRequest):
    return await client_controller.client_sign_in(sign_in_data)


@router.post("/client/create_order/", tags=["client"])
async def create_order(
    data: common.OrderCreateRequest = Body(...),
    client_id: str = Security(get_sub_security),
    session: AsyncSession = Depends(get_session),
):
    return await client_controller.create_order(client_id, data, session)


@router.get("/client/orders/", tags=["client"])
async def get_orders(client_id: str = Security(get_sub_security), session: AsyncSession = Depends(get_session)):
    return await client_controller.get_orders(client_id, session)


@router.get("/client/order/", tags=["client"])
async def get_order_by_id(order_id: str, client_id: str = Security(get_sub_security), session: AsyncSession = Depends(get_session)):
    return await client_controller.get_order_by_id(client_id, order_id, session)


@router.put("/client/order/", tags=["client"])
async def update_order(
    order_id: str, update_data: common.OrderUpdateRequest, client_id: str = Security(get_sub_security), session: AsyncSession = Depends(get_session)
):
    return await client_controller.update_order(client_id, order_id, update_data, session)


@router.delete("/client/order/", tags=["client"])
async def delete_order(order_id: str, client_id: str = Security(get_sub_security), session: AsyncSession = Depends(get_session)):
    return await client_controller.delete_order(client_id, order_id, session)
