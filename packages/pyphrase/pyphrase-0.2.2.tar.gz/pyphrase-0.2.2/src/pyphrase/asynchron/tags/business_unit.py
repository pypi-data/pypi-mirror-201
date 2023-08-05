from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    BusinessUnitDto,
    BusinessUnitEditDto,
    PageDtoBusinessUnitDto,
)


class BusinessUnitOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def getBusinessUnit(
        self, businessUnitUid: str, phrase_token: Optional[str] = None
    ) -> BusinessUnitDto:
        """
        Get business unit

        :param businessUnitUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: BusinessUnitDto
        """
        endpoint = f"/api2/v1/businessUnits/{businessUnitUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return BusinessUnitDto(**r)

    async def updateBusinessUnit(
        self,
        businessUnitUid: str,
        body: BusinessUnitEditDto,
        phrase_token: Optional[str] = None,
    ) -> BusinessUnitDto:
        """
        Edit business unit

        :param businessUnitUid: string (required), path.
        :param body: BusinessUnitEditDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: BusinessUnitDto
        """
        endpoint = f"/api2/v1/businessUnits/{businessUnitUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return BusinessUnitDto(**r)

    async def deleteBusinessUnit(
        self, businessUnitUid: str, phrase_token: Optional[str] = None
    ) -> None:
        """
        Delete business unit

        :param businessUnitUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/businessUnits/{businessUnitUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def listBusinessUnits(
        self,
        createdBy: str = None,
        name: str = None,
        sort: str = "NAME",
        order: str = "ASC",
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoBusinessUnitDto:
        """
        List business units

        :param createdBy: string (optional), query. Uid of user.
        :param name: string (optional), query. Unique name of the business unit.
        :param sort: string (optional), query.
        :param order: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoBusinessUnitDto
        """
        endpoint = f"/api2/v1/businessUnits"
        params = {
            "name": name,
            "createdBy": createdBy,
            "sort": sort,
            "order": order,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
        }

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoBusinessUnitDto(**r)

    async def createBusinessUnit(
        self, body: BusinessUnitEditDto, phrase_token: Optional[str] = None
    ) -> BusinessUnitDto:
        """
        Create business unit

        :param body: BusinessUnitEditDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: BusinessUnitDto
        """
        endpoint = f"/api2/v1/businessUnits"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return BusinessUnitDto(**r)
