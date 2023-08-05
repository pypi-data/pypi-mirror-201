from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import ClientDto, ClientEditDto, PageDtoClientDto


class ClientOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def getClient(
        self,
        clientUid: str,
        phrase_token: Optional[str] = None,
    ) -> ClientDto:
        """
        Get client

        :param clientUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ClientDto
        """
        endpoint = f"/api2/v1/clients/{clientUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ClientDto(**r)

    def updateClient(
        self,
        clientUid: str,
        body: ClientEditDto,
        phrase_token: Optional[str] = None,
    ) -> ClientDto:
        """
        Edit client

        :param clientUid: string (required), path.
        :param body: ClientEditDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ClientDto
        """
        endpoint = f"/api2/v1/clients/{clientUid}"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ClientDto(**r)

    def deleteClient(
        self,
        clientUid: str,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete client

        :param clientUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/clients/{clientUid}"
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def listClients(
        self,
        createdBy: str = None,
        name: str = None,
        sort: str = "NAME",
        order: str = "ASC",
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoClientDto:
        """
        List clients

        :param createdBy: string (optional), query. Uid of user.
        :param name: string (optional), query. Unique name of the Client.
        :param sort: string (optional), query.
        :param order: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoClientDto
        """
        endpoint = f"/api2/v1/clients"
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

        return PageDtoClientDto(**r)

    def createClient(
        self,
        body: ClientEditDto,
        phrase_token: Optional[str] = None,
    ) -> ClientDto:
        """
        Create client

        :param body: ClientEditDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ClientDto
        """
        endpoint = f"/api2/v1/clients"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ClientDto(**r)
