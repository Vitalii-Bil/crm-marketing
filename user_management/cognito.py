import hmac
import base64
import hashlib
import aioboto3
from fastapi import HTTPException

from config import (
    COGNITO_POOL_CLIENT_ID,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    COGNITO_POOL_CLIENT_SECRET,
    COGNITO_USER_POOL_ID,
)


class CognitoUserManagement:
    def __init__(self):
        self.session = aioboto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

    def _manager_get_secret_hash(self, username):
        message = username + COGNITO_POOL_CLIENT_ID
        dig = hmac.new(
            str(COGNITO_POOL_CLIENT_SECRET).encode("utf-8"), msg=message.encode("UTF-8"), digestmod=hashlib.sha256
        ).digest()
        return base64.b64encode(dig).decode()

    async def manager_sign_up(self, user_email, user_password):
        try:
            cognito_client = self.session.client("cognito-idp", region_name=AWS_REGION)
            async with cognito_client as client:
                cognito_response = await client.sign_up(
                    ClientId=COGNITO_POOL_CLIENT_ID,
                    SecretHash=self._manager_get_secret_hash(user_email),
                    Username=user_email,
                    Password=user_password,
                    UserAttributes=[{"Name": "email", "Value": user_email}],
                )
                return cognito_response["UserSub"]
        except client.exceptions.ClientError as ex:
            print(f"Failed user authentication: {repr(ex)}")
            raise HTTPException(
                status_code=404,
                detail="Failed user signing up. Note that password should have at least 1 letter, 1 symbol, 1 number, 1 upper and lower case letter",
            )

    async def manager_confirm_sign_up(self, user_email):
        try:
            cognito_client = self.session.client("cognito-idp", region_name=AWS_REGION)
            async with cognito_client as client:
                await client.admin_confirm_sign_up(
                    UserPoolId=COGNITO_USER_POOL_ID,
                    Username=user_email,
                )
        except client.exceptions.ClientError as ex:
            print(f"Failed user authentication: {repr(ex)}")
            raise HTTPException(status_code=404, detail="Failed user confirmation.")

    async def manager_sign_in(self, user_email, user_password):
        try:
            cognito_client = self.session.client("cognito-idp", region_name=AWS_REGION)
            async with cognito_client as client:
                response = await client.admin_initiate_auth(
                    UserPoolId=COGNITO_USER_POOL_ID,
                    ClientId=COGNITO_POOL_CLIENT_ID,
                    AuthFlow="ADMIN_USER_PASSWORD_AUTH",
                    AuthParameters={
                        "USERNAME": user_email,
                        "PASSWORD": user_password,
                        "SECRET_HASH": self._manager_get_secret_hash(user_email),
                    },
                )
                print(response)
                access_token = response["AuthenticationResult"]["AccessToken"]
                return access_token
        except client.exceptions.ClientError as ex:
            print(f"Failed user authentication: {repr(ex)}")
            raise HTTPException(status_code=404, detail="Failed user signing in.")

    async def get_user_sub_from_token(self, access_token):
        cognito_client = self.session.client("cognito-idp", region_name=AWS_REGION)
        async with cognito_client as client:
            response = await client.get_user(AccessToken=access_token)
            user_sub = response["UserAttributes"][0]["Value"]
            return user_sub
