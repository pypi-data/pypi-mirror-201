from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    CreateCustomFileTypeDto,
    CustomFileTypeDto,
    DeleteCustomFileTypeDto,
    PageDtoCustomFileTypeDto,
    UpdateCustomFileTypeDto,
)


class CustomFileTypeOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def getAllCustomFileType(
        self,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoCustomFileTypeDto:
        """
        Get All Custom file type

        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoCustomFileTypeDto
        """
        endpoint = f"/api2/v1/customFileTypes"
        params = {"pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoCustomFileTypeDto(**r)

    async def createCustomFileTypes(
        self, body: CreateCustomFileTypeDto, phrase_token: Optional[str] = None
    ) -> CustomFileTypeDto:
        """
        Create custom file type

        :param body: CreateCustomFileTypeDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: CustomFileTypeDto
        """
        endpoint = f"/api2/v1/customFileTypes"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return CustomFileTypeDto(**r)

    async def deleteBatchCustomFileType(
        self, body: DeleteCustomFileTypeDto, phrase_token: Optional[str] = None
    ) -> None:
        """
        Delete multiple Custom file type

        :param body: DeleteCustomFileTypeDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/customFileTypes"
        params = {}

        files = None
        payload = body

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def getCustomFileType(
        self, customFileTypeUid: str, phrase_token: Optional[str] = None
    ) -> CustomFileTypeDto:
        """
        Get Custom file type

        :param customFileTypeUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: CustomFileTypeDto
        """
        endpoint = f"/api2/v1/customFileTypes/{customFileTypeUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return CustomFileTypeDto(**r)

    async def updateCustomFileType(
        self,
        customFileTypeUid: str,
        body: UpdateCustomFileTypeDto,
        phrase_token: Optional[str] = None,
    ) -> CustomFileTypeDto:
        """
        Update Custom file type

        :param customFileTypeUid: string (required), path.
        :param body: UpdateCustomFileTypeDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: CustomFileTypeDto
        """
        endpoint = f"/api2/v1/customFileTypes/{customFileTypeUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return CustomFileTypeDto(**r)

    async def deleteCustomFileType(
        self, customFileTypeUid: str, phrase_token: Optional[str] = None
    ) -> None:
        """
        Delete Custom file type

        :param customFileTypeUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/customFileTypes/{customFileTypeUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return
