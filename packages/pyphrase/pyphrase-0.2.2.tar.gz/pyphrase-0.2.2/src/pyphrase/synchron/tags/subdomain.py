from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import PageDtoSubDomainDto, SubDomainDto, SubDomainEditDto


class SubdomainOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def listSubDomains(
        self,
        createdBy: str = None,
        name: str = None,
        sort: str = "NAME",
        order: str = "ASC",
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoSubDomainDto:
        """
        List subdomains

        :param createdBy: string (optional), query. Uid of user.
        :param name: string (optional), query.
        :param sort: string (optional), query.
        :param order: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoSubDomainDto
        """
        endpoint = f"/api2/v1/subDomains"
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

        return PageDtoSubDomainDto(**r)

    def createSubDomain(
        self,
        body: SubDomainEditDto,
        phrase_token: Optional[str] = None,
    ) -> SubDomainDto:
        """
        Create subdomain

        :param body: SubDomainEditDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: SubDomainDto
        """
        endpoint = f"/api2/v1/subDomains"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return SubDomainDto(**r)

    def getSubDomain(
        self,
        subDomainUid: str,
        phrase_token: Optional[str] = None,
    ) -> SubDomainDto:
        """
        Get subdomain

        :param subDomainUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: SubDomainDto
        """
        endpoint = f"/api2/v1/subDomains/{subDomainUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return SubDomainDto(**r)

    def updateSubDomain(
        self,
        subDomainUid: str,
        body: SubDomainEditDto,
        phrase_token: Optional[str] = None,
    ) -> SubDomainDto:
        """
        Edit subdomain

        :param subDomainUid: string (required), path.
        :param body: SubDomainEditDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: SubDomainDto
        """
        endpoint = f"/api2/v1/subDomains/{subDomainUid}"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return SubDomainDto(**r)

    def deleteSubDomain(
        self,
        subDomainUid: str,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete subdomain

        :param subDomainUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/subDomains/{subDomainUid}"
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return
