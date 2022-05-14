from fastapi import APIRouter, Depends, HTTPException, Header, Body, Security
from sqlalchemy.ext.asyncio import AsyncSession

from controllers import admin
from db.session import get_session
from user_management import cognito
from pydantic_models.common import SignInRequest

router = APIRouter()
admin_controller = admin.AdminController()
cognito_manager = cognito.CognitoUserManagement()


async def get_sub_security(access_token: str = Header(...)):
    async def get_sub():
        try:
            return await cognito_manager.get_user_sub_from_token(access_token)
        except Exception:
            raise HTTPException(status_code=404, detail="Access token was not validated")
    return await get_sub()


@router.post("/admin/sign_in/", tags=["admin"])
async def sign_in(sign_in_data: SignInRequest = Body(...)):
    return await admin_controller.admin_sign_in(sign_in_data)


@router.get("/admin/managers/", tags=["admin"])
async def get_managers_list(_=Security(get_sub_security), session: AsyncSession = Depends(get_session)):
    return await admin_controller.get_managers_list(session)


@router.get("/admin/manager/", tags=["admin"])
async def get_manager_by_id(manager_id: str, _=Security(get_sub_security), session: AsyncSession = Depends(get_session)):
    return await admin_controller.get_manager_by_id(manager_id, session)


@router.get("/admin/clients/", tags=["admin"])
async def get_clients_list(_=Security(get_sub_security), session: AsyncSession = Depends(get_session)):
    return await admin_controller.get_clients_list(session)


@router.get("/admin/client/", tags=["admin"])
async def get_client_by_id(client_id: str, _=Security(get_sub_security), session: AsyncSession = Depends(get_session)):
    return await admin_controller.get_client_by_id(client_id, session)


@router.put("/admin/manager/", tags=["admin"])
async def change_manager_status(manager_id: str, status: bool, _=Security(get_sub_security), session: AsyncSession = Depends(get_session)):
    return await admin_controller.update_manager_status(manager_id, status, session)
