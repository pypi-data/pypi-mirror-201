from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import DomainDto, DomainEditDto, PageDtoDomainDto


class DomainOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def getDomain(
        self,
        domainUid: str,
        phrase_token: Optional[str] = None,
    ) -> DomainDto:
        """
        Get domain

        :param domainUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: DomainDto
        """
        endpoint = f"/api2/v1/domains/{domainUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return DomainDto(**r)

    def updateDomain(
        self,
        domainUid: str,
        body: DomainEditDto,
        phrase_token: Optional[str] = None,
    ) -> DomainDto:
        """
        Edit domain

        :param domainUid: string (required), path.
        :param body: DomainEditDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: DomainDto
        """
        endpoint = f"/api2/v1/domains/{domainUid}"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return DomainDto(**r)

    def deleteDomain(
        self,
        domainUid: str,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete domain

        :param domainUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/domains/{domainUid}"
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def listDomains(
        self,
        createdBy: str = None,
        name: str = None,
        sort: str = "NAME",
        order: str = "ASC",
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoDomainDto:
        """
        List of domains

        :param createdBy: string (optional), query. Uid of user.
        :param name: string (optional), query.
        :param sort: string (optional), query.
        :param order: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoDomainDto
        """
        endpoint = f"/api2/v1/domains"
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

        return PageDtoDomainDto(**r)

    def createDomain(
        self,
        body: DomainEditDto,
        phrase_token: Optional[str] = None,
    ) -> DomainDto:
        """
        Create domain

        :param body: DomainEditDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: DomainDto
        """
        endpoint = f"/api2/v1/domains"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return DomainDto(**r)
