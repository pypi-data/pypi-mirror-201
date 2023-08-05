from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    AsyncRequestDto,
    AsyncRequestStatusDto,
    PageDtoAsyncRequestDto,
)


class AsyncRequestOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def getAsyncRequest(
        self, asyncRequestId: int, phrase_token: Optional[str] = None
    ) -> AsyncRequestDto:
        """
        Get asynchronous request

        :param asyncRequestId: integer (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AsyncRequestDto
        """
        endpoint = f"/api2/v1/async/{asyncRequestId}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AsyncRequestDto(**r)

    async def listPendingRequests(
        self,
        all: bool = "False",
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoAsyncRequestDto:
        """
        List pending requests

        :param all: boolean (optional), query. Pending requests for organization instead of current user. Only for ADMIN..
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoAsyncRequestDto
        """
        endpoint = f"/api2/v1/async"
        params = {"all": all, "pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoAsyncRequestDto(**r)

    async def getCurrentLimitStatus(
        self, phrase_token: Optional[str] = None
    ) -> AsyncRequestStatusDto:
        """
        Get current limits


        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AsyncRequestStatusDto
        """
        endpoint = f"/api2/v1/async/status"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AsyncRequestStatusDto(**r)
