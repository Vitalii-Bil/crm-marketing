import asyncio
import sys

from pydantic import EmailStr

from db.models.models_base import Admins
from db.session import async_session
from user_management.cognito import CognitoUserManagement


cognito_manager = CognitoUserManagement()


async def create_admin(admin_email, admin_password):
    async with async_session() as session:
        user_sub = await cognito_manager.manager_sign_up(admin_email, admin_password)
        await cognito_manager.manager_confirm_sign_up(admin_email)
        new_manager = Admins(
            id=user_sub,
            email=admin_email,
        )
        session.add(new_manager)
        await session.commit()
        print("Admin registered")


async def main():
    email: EmailStr = EmailStr(sys.argv[1])
    password: str = sys.argv[2]
    try:
        await create_admin(email, password)
    except Exception as ex:
        print(ex, "Admin was not created!")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
