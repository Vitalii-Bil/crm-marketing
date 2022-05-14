from fastapi import APIRouter, HTTPException
from pydantic_models.common import OrderCreateRequest, OrderUpdateRequest, ClientRegisterRequest, OrderStatus, SignInRequest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from db.models.models_base import Orders, Clients
from user_management.cognito import CognitoUserManagement

router = APIRouter()


class ClientController:
    _cognito_manager = CognitoUserManagement()

    async def client_sign_up(self, sign_up_data: ClientRegisterRequest, session: AsyncSession):
        user_sub = await self._cognito_manager.manager_sign_up(sign_up_data.email, sign_up_data.password)
        await self._cognito_manager.manager_confirm_sign_up(sign_up_data.email)
        try:
            new_client = Clients(
                id=user_sub,
                email=sign_up_data.email,
                first_name=sign_up_data.first_name,
                last_name=sign_up_data.last_name,
                birthday=sign_up_data.birthday,
                phone_number=sign_up_data.phone_number,
                city=sign_up_data.city,
                address=sign_up_data.address,
            )
            session.add(new_client)
            await session.commit()
            return {"message": "User signed up"}
        except Exception:
            raise HTTPException(status_code=404, detail="Failed database insertion")

    async def client_sign_in(self, sign_in_data: SignInRequest):
        access_token = await self._cognito_manager.manager_sign_in(sign_in_data.email, sign_in_data.password)
        return {"access_token": access_token}

    async def create_order(self, client_id, data: OrderCreateRequest, session: AsyncSession):
        try:
            new_order = Orders(
                client_id=client_id,
                order_name=data.order_name,
                order_details=data.order_details,
                sphere_type=data.sphere_type,
                order_status=OrderStatus.Free
            )
            session.add(new_order)
            await session.commit()
            return new_order
        except Exception:
            raise HTTPException(status_code=404, detail="Failed database insertion")

    async def get_orders(self, client_id, session: AsyncSession):
        try:
            result = await session.execute(select(Orders).filter(Orders.client_id == client_id))
            response = result.scalars().all()
            if not response:
                return {"message": "No orders found"}
            return response
        except Exception:
            raise HTTPException(status_code=404, detail="Failed database selection")

    async def get_order_by_id(self, client_id, order_id, session: AsyncSession):
        try:
            result = await session.execute(select(Orders).filter(Orders.client_id == client_id, Orders.pk == order_id))
            response = result.scalars().all()
            if not response:
                return {"message": "Order was not found"}
            return response
        except Exception:
            raise HTTPException(status_code=404, detail="Failed database selection")

    async def update_order(self, client_id, order_id, update_data: OrderUpdateRequest, session: AsyncSession):
        dict_update_data = update_data.dict()
        _dict_update_data = dict_update_data.copy()
        for key in _dict_update_data.keys():
            if dict_update_data[key] is None:
                dict_update_data.pop(key)
        try:
            await session.execute(
                update(Orders).where(Orders.client_id == client_id, Orders.pk == order_id).values(dict_update_data)
            )
            await session.commit()
            return {"message": "Order was updated"}
        except Exception:
            raise HTTPException(status_code=404, detail="Failed database insertion")

    async def delete_order(self, client_id, order_id, session: AsyncSession):
        try:
            await session.execute(delete(Orders).where(Orders.pk == order_id, Orders.client_id == client_id))
            await session.commit()
            return {"message": "Order was deleted"}
        except Exception:
            raise HTTPException(status_code=404, detail="Failed database insertion")
