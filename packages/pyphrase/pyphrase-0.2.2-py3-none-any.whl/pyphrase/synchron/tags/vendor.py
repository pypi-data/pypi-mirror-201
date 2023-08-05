from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import CreateVendorDto, PageDtoVendorDto, VendorDto


class VendorOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def getVendor(
        self,
        vendorUid: str,
        phrase_token: Optional[str] = None,
    ) -> VendorDto:
        """
        Get vendor

        :param vendorUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: VendorDto
        """
        endpoint = f"/api2/v1/vendors/{vendorUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return VendorDto(**r)

    def listVendors(
        self,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoVendorDto:
        """
        List vendors

        :param name: string (optional), query. Name or the vendor, for filtering.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoVendorDto
        """
        endpoint = f"/api2/v1/vendors"
        params = {"pageNumber": pageNumber, "pageSize": pageSize, "name": name}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoVendorDto(**r)

    def createVendor(
        self,
        body: CreateVendorDto,
        phrase_token: Optional[str] = None,
    ) -> VendorDto:
        """
        Create vendor

        :param body: CreateVendorDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: VendorDto
        """
        endpoint = f"/api2/v1/vendors"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return VendorDto(**r)
