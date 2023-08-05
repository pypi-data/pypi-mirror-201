from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    CostCenterDto,
    CostCenterEditDto,
    PageDtoCostCenterDto,
)


class CostCenterOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def getCostCenter(
        self,
        costCenterUid: str,
        phrase_token: Optional[str] = None,
    ) -> CostCenterDto:
        """
        Get cost center

        :param costCenterUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: CostCenterDto
        """
        endpoint = f"/api2/v1/costCenters/{costCenterUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return CostCenterDto(**r)

    def updateCostCenter(
        self,
        costCenterUid: str,
        body: CostCenterEditDto,
        phrase_token: Optional[str] = None,
    ) -> CostCenterDto:
        """
        Edit cost center

        :param costCenterUid: string (required), path.
        :param body: CostCenterEditDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: CostCenterDto
        """
        endpoint = f"/api2/v1/costCenters/{costCenterUid}"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return CostCenterDto(**r)

    def deleteCostCenter(
        self,
        costCenterUid: str,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete cost center

        :param costCenterUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/costCenters/{costCenterUid}"
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def listCostCenters(
        self,
        createdBy: str = None,
        name: str = None,
        sort: str = "NAME",
        order: str = "ASC",
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoCostCenterDto:
        """
        List of cost centers

        :param createdBy: string (optional), query. Uid of user.
        :param name: string (optional), query.
        :param sort: string (optional), query.
        :param order: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoCostCenterDto
        """
        endpoint = f"/api2/v1/costCenters"
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

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoCostCenterDto(**r)

    def createCostCenter(
        self,
        body: CostCenterEditDto,
        phrase_token: Optional[str] = None,
    ) -> CostCenterDto:
        """
        Create cost center

        :param body: CostCenterEditDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: CostCenterDto
        """
        endpoint = f"/api2/v1/costCenters"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return CostCenterDto(**r)
