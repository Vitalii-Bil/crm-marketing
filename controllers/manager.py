from fastapi import APIRouter, HTTPException
from pydantic_models.common import (
    OrderStatus,
    LeaveCommentRequest,
    ManagerRegistrationRequest,
    OrderStatusUpdate,
    SignInRequest,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, text

from db.models.models_base import Orders, Managers
from user_management.cognito import CognitoUserManagement

router = APIRouter()


class ManagerController:
    _cognito_manager = CognitoUserManagement()

    async def _check_if_manager_active(self, manager_id, session: AsyncSession):
        result = await session.execute(select(Managers).filter(Managers.id == manager_id, Managers.status == True))
        response = result.scalars().all()
        print(response)
        if response:
            return True
        return False

    async def client_sign_up(self, sign_up_data: ManagerRegistrationRequest, session: AsyncSession):
        user_sub = await self._cognito_manager.manager_sign_up(sign_up_data.email, sign_up_data.password)
        await self._cognito_manager.manager_confirm_sign_up(sign_up_data.email)
        try:
            new_manager = Managers(
                id=user_sub,
                email=sign_up_data.email,
                first_name=sign_up_data.first_name,
                last_name=sign_up_data.last_name,
                birthday=sign_up_data.birthday,
                phone_number=sign_up_data.phone_number,
            )
            session.add(new_manager)
            await session.commit()
            return {"message": "User signed up"}
        except Exception:
            raise HTTPException(status_code=404, detail="Failed database insertion")

    async def client_sign_in(self, sign_in_data: SignInRequest):
        access_token = await self._cognito_manager.manager_sign_in(sign_in_data.email, sign_in_data.password)
        return {"access_token": access_token}

    async def get_free_orders(self, manager_id, session: AsyncSession):
        try:
            if await self._check_if_manager_active(manager_id, session):
                result = await session.execute(select(Orders).filter(Orders.order_status == OrderStatus.Free))
                response = result.scalars().all()
                if not response:
                    return {"message": "No free orders found"}
                return response
            return {"message": "Manager is inactive"}
        except Exception:
            raise HTTPException(status_code=404, detail="Failed database selection")

    async def make_order_in_work(self, manager_id, order_id, session: AsyncSession):
        try:
            if await self._check_if_manager_active(manager_id, session):
                await session.execute(
                    update(Orders)
                    .where(
                        Orders.pk == order_id,
                        Orders.order_status == OrderStatus.Free,
                    )
                    .values({"order_status": OrderStatus.InWork, "manager_id": manager_id})
                )
                await session.commit()
                return {"message": "Order got in work"}
            return {"message": "Manager is inactive"}
        except Exception:
            raise HTTPException(status_code=404, detail="Failed database insertion")

    async def get_in_work_orders(self, manager_id, session: AsyncSession):
        try:
            if await self._check_if_manager_active(manager_id, session):
                result = await session.execute(select(Orders).filter(Orders.manager_id == manager_id))
                response = result.scalars().all()
                if not response:
                    return {"message": "No in work orders found"}
                return response
            return {"message": "Manager is inactive"}
        except Exception:
            raise HTTPException(status_code=404, detail="Failed database selection")

    async def get_in_work_order_by_id(self, manager_id, order_id, session: AsyncSession):
        try:
            if await self._check_if_manager_active(manager_id, session):
                result = await session.execute(
                    select(Orders).filter(
                        Orders.manager_id == manager_id,
                        Orders.pk == order_id,
                    )
                )
                response = result.scalars().all()
                if not response:
                    return {"message": "Order was not found"}
                return response
            return {"message": "Manager is inactive"}
        except Exception:
            raise HTTPException(status_code=404, detail="Failed database selection")

    async def update_status_in_work_order_by_id(
        self, manager_id, order_id, status: OrderStatusUpdate, session: AsyncSession
    ):
        try:
            if await self._check_if_manager_active(manager_id, session):
                await session.execute(
                    update(Orders)
                    .where(
                        Orders.pk == order_id,
                        Orders.manager_id == manager_id,
                    )
                    .values({"order_status": status.name})
                )
                await session.commit()
                return {"message": "Order status updated"}
            return {"message": "Manager is inactive"}
        except Exception:
            raise HTTPException(status_code=404, detail="Failed database insertion")

    async def make_order_free(self, manager_id, order_id, session: AsyncSession):
        try:
            if await self._check_if_manager_active(manager_id, session):
                await session.execute(
                    update(Orders)
                    .where(
                        Orders.pk == order_id,
                        Orders.manager_id == manager_id,
                    )
                    .values({"order_status": OrderStatus.Free, "manager_id": None})
                )
                await session.commit()
                return {"message": "Order made free"}
            return {"message": "Manager is inactive"}
        except Exception:
            raise HTTPException(status_code=404, detail="Failed database insertion")
