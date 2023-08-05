from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    AppleTokenResponseDto,
    LoginDto,
    LoginOtherDto,
    LoginOtherV3Dto,
    LoginResponseDto,
    LoginResponseV3Dto,
    LoginToSessionDto,
    LoginToSessionResponseDto,
    LoginToSessionResponseV3Dto,
    LoginToSessionV3Dto,
    LoginUserDto,
    LoginV3Dto,
    LoginWithAppleDto,
    LoginWithGoogleDto,
)


class AuthenticationOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def login(
        self, body: LoginDto, phrase_token: Optional[str] = None
    ) -> LoginResponseDto:
        """
        Login

        :param body: LoginDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: LoginResponseDto
        """
        endpoint = f"/api2/v1/auth/login"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return LoginResponseDto(**r)

    async def logout(
        self, token: str = None, phrase_token: Optional[str] = None
    ) -> None:
        """
        Logout

        :param token: string (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/auth/logout"
        params = {"token": token}

        files = None
        payload = None

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def loginToSession(
        self, body: LoginToSessionDto, phrase_token: Optional[str] = None
    ) -> LoginToSessionResponseDto:
        """
        Login to session

        :param body: LoginToSessionDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: LoginToSessionResponseDto
        """
        endpoint = f"/api2/v1/auth/loginToSession"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return LoginToSessionResponseDto(**r)

    async def loginOther(
        self, body: LoginOtherDto, phrase_token: Optional[str] = None
    ) -> LoginResponseDto:
        """
        Login as another user
        Available only for admin
        :param body: LoginOtherDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: LoginResponseDto
        """
        endpoint = f"/api2/v1/auth/loginOther"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return LoginResponseDto(**r)

    async def whoAmI(self, phrase_token: Optional[str] = None) -> LoginUserDto:
        """
        Who am I


        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: LoginUserDto
        """
        endpoint = f"/api2/v1/auth/whoAmI"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return LoginUserDto(**r)

    async def loginByGoogle(
        self, body: LoginWithGoogleDto, phrase_token: Optional[str] = None
    ) -> LoginResponseDto:
        """
        Login with Google

        :param body: LoginWithGoogleDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: LoginResponseDto
        """
        endpoint = f"/api2/v1/auth/loginWithGoogle"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return LoginResponseDto(**r)

    async def loginByAppleWithRefreshToken(
        self, body: LoginWithAppleDto, phrase_token: Optional[str] = None
    ) -> LoginResponseDto:
        """
        Login with Apple refresh token

        :param body: LoginWithAppleDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: LoginResponseDto
        """
        endpoint = f"/api2/v1/auth/loginWithApple/refreshToken"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return LoginResponseDto(**r)

    async def loginByAppleWithCode(
        self,
        body: LoginWithAppleDto,
        native: bool = None,
        phrase_token: Optional[str] = None,
    ) -> LoginResponseDto:
        """
        Login with Apple with code

        :param body: LoginWithAppleDto (required), body.
        :param native: boolean (optional), query. For sign in with code from native device.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: LoginResponseDto
        """
        endpoint = f"/api2/v1/auth/loginWithApple/code"
        params = {"native": native}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return LoginResponseDto(**r)

    async def refreshAppleToken(
        self, token: str = None, phrase_token: Optional[str] = None
    ) -> AppleTokenResponseDto:
        """
        refresh apple token

        :param token: string (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AppleTokenResponseDto
        """
        endpoint = f"/api2/v1/auth/refreshAppleToken"
        params = {"token": token}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AppleTokenResponseDto(**r)

    async def login_1(
        self, body: LoginV3Dto, phrase_token: Optional[str] = None
    ) -> LoginResponseV3Dto:
        """
        Login

        :param body: LoginV3Dto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: LoginResponseV3Dto
        """
        endpoint = f"/api2/v3/auth/login"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return LoginResponseV3Dto(**r)

    async def loginToSession_2(
        self, body: LoginToSessionV3Dto, phrase_token: Optional[str] = None
    ) -> LoginToSessionResponseV3Dto:
        """
        Login to session

        :param body: LoginToSessionV3Dto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: LoginToSessionResponseV3Dto
        """
        endpoint = f"/api2/v3/auth/loginToSession"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return LoginToSessionResponseV3Dto(**r)

    async def loginOther_1(
        self, body: LoginOtherV3Dto, phrase_token: Optional[str] = None
    ) -> LoginResponseV3Dto:
        """
        Login as another user
        Available only for admin
        :param body: LoginOtherV3Dto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: LoginResponseV3Dto
        """
        endpoint = f"/api2/v3/auth/loginOther"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return LoginResponseV3Dto(**r)
