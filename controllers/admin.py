from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

import db.models.models_base as models_base
from pydantic_models.common import SignInRequest
from user_management.cognito import CognitoUserManagement

router = APIRouter()


class AdminController:
    _cognito_manager = CognitoUserManagement()

    async def admin_sign_in(self, sign_in_data: SignInRequest):
        access_token = await self._cognito_manager.manager_sign_in(sign_in_data.email, sign_in_data.password)
        return {"access_token": access_token}

    async def get_managers_list(self, session: AsyncSession):
        try:
            result = await session.execute(select(models_base.Managers))
            response = result.scalars().all()
            if not response:
                return {"message": "No managers found"}
            return response
        except Exception:
            raise HTTPException(status_code=404, detail="Failed database selection")

    async def get_manager_by_id(self, manager_id, session: AsyncSession):
        try:
            result = await session.execute(select(models_base.Managers).where(models_base.Managers.id == manager_id))
            response = result.scalars().all()
            if not response:
                return {"message": "Manager was not found"}
            return response
        except Exception:
            raise HTTPException(status_code=404, detail="Failed database selection")

    async def get_clients_list(self, session: AsyncSession):
        try:
            result = await session.execute(select(models_base.Clients))
            response = result.scalars().all()
            if not response:
                return {"message": "No clients found"}
            return response
        except Exception:
            raise HTTPException(status_code=404, detail="Failed database selection")

    async def get_client_by_id(self, client_id, session: AsyncSession):
        try:
            result = await session.execute(select(models_base.Clients).where(models_base.Clients.id == client_id))
            response = result.scalars().all()
            if not response:
                return {"message": "Client was not found"}
            return response
        except Exception:
            raise HTTPException(status_code=404, detail="Failed database selection")

    async def update_manager_status(self, manager_id, status, session: AsyncSession):
        try:
            await session.execute(
                update(models_base.Managers)
                .where(
                    models_base.Managers.id == manager_id,
                )
                .values({"status": status})
            )
            await session.commit()
            return {"message": "Manager status updated"}
        except Exception:
            raise HTTPException(status_code=404, detail="Failed database insertion")
