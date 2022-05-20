from fastapi import APIRouter, Depends, Body, Header, HTTPException, Security
from sqlalchemy.ext.asyncio import AsyncSession

from controllers import manager
from db.session import get_session
from pydantic_models.common import (
    OrderStatus,
    ManagerRegistrationRequest,
    OrderStatusUpdate,
    SignInRequest,
)
from user_management import cognito

router = APIRouter()
manager_controller = manager.ManagerController()
cognito_manager = cognito.CognitoUserManagement()


async def get_sub_security(access_token: str = Header(...)):
    async def get_sub():
        try:
            return await cognito_manager.get_user_sub_from_token(access_token)
        except Exception:
            raise HTTPException(status_code=404, detail="Access token was not validated")

    return await get_sub()


@router.post("/manager/sign_up/", tags=["manager"])
async def sign_up(sign_up_data: ManagerRegistrationRequest, session: AsyncSession = Depends(get_session)):
    return await manager_controller.client_sign_up(sign_up_data, session)


@router.post("/manager/sign_in/", tags=["manager"])
async def sign_in(sign_in_data: SignInRequest):
    return await manager_controller.client_sign_in(sign_in_data)


@router.get("/manager/free_orders/", tags=["manager"])
async def get_free_orders(manager_id: str = Security(get_sub_security), session: AsyncSession = Depends(get_session)):
    return await manager_controller.get_free_orders(manager_id, session)


@router.put("/manager/make_order_in_work/", tags=["manager"])
async def make_order_in_work(
    order_id: str, manager_id: str = Security(get_sub_security), session: AsyncSession = Depends(get_session)
):
    return await manager_controller.make_order_in_work(manager_id, order_id, session)


@router.get("/manager/in_work_orders/", tags=["manager"])
async def get_in_work_orders(
    manager_id: str = Security(get_sub_security), session: AsyncSession = Depends(get_session)
):
    return await manager_controller.get_in_work_orders(manager_id, session)


@router.get("/manager/in_work_order/", tags=["manager"])
async def get_in_work_order_by_id(
    order_id: str, manager_id: str = Security(get_sub_security), session: AsyncSession = Depends(get_session)
):
    return await manager_controller.get_in_work_order_by_id(manager_id, order_id, session)


@router.put("/manager/in_work_order/status/", tags=["manager"])
async def update_status_in_work_order_by_id(
    order_id: str,
    status: OrderStatusUpdate,
    manager_id: str = Security(get_sub_security),
    session: AsyncSession = Depends(get_session),
):
    return await manager_controller.update_status_in_work_order_by_id(manager_id, order_id, status, session)


@router.put("/manager/make_order_free/", tags=["manager"])
async def make_order_free(
    order_id: str, manager_id: str = Security(get_sub_security), session: AsyncSession = Depends(get_session)
):
    return await manager_controller.make_order_free(manager_id, order_id, session)
