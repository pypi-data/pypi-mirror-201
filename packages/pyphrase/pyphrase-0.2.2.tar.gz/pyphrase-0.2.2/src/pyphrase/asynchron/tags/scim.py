from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    ScimResourceSchema,
    ScimResourceTypeSchema,
    ScimUserCoreDto,
    ServiceProviderConfigDto,
)


class ScimOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def getSchemas(
        self, phrase_token: Optional[str] = None
    ) -> ScimResourceSchema:
        """
        Get supported SCIM Schemas


        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ScimResourceSchema
        """
        endpoint = f"/api2/v1/scim/Schemas"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ScimResourceSchema(**r)

    async def getSchemaByUrn(
        self, schemaUrn: str, phrase_token: Optional[str] = None
    ) -> ScimResourceSchema:
        """
        Get supported SCIM Schema by urn

        :param schemaUrn: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ScimResourceSchema
        """
        endpoint = f"/api2/v1/scim/Schemas/{schemaUrn}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ScimResourceSchema(**r)

    async def getServiceProviderConfigDto(
        self, phrase_token: Optional[str] = None
    ) -> ServiceProviderConfigDto:
        """
        Retrieve the Service Provider's Configuration


        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ServiceProviderConfigDto
        """
        endpoint = f"/api2/v1/scim/ServiceProviderConfig"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ServiceProviderConfigDto(**r)

    async def getResourceTypes(
        self, phrase_token: Optional[str] = None
    ) -> ScimResourceTypeSchema:
        """
        List the types of SCIM Resources available


        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ScimResourceTypeSchema
        """
        endpoint = f"/api2/v1/scim/ResourceTypes"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ScimResourceTypeSchema(**r)

    async def getScimUser(
        self, userId: int, phrase_token: Optional[str] = None
    ) -> ScimUserCoreDto:
        """
        Get user

        :param userId: integer (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ScimUserCoreDto
        """
        endpoint = f"/api2/v1/scim/Users/{userId}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ScimUserCoreDto(**r)

    async def editUser(
        self, userId: int, body: ScimUserCoreDto, phrase_token: Optional[str] = None
    ) -> ScimUserCoreDto:
        """
        Edit user using SCIM

        :param userId: integer (required), path.
        :param body: ScimUserCoreDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ScimUserCoreDto
        """
        endpoint = f"/api2/v1/scim/Users/{userId}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ScimUserCoreDto(**r)

    async def deleteUser(self, userId: int, phrase_token: Optional[str] = None) -> None:
        """
        Delete user using SCIM

        :param userId: integer (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/scim/Users/{userId}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def patchUser(
        self, userId: int, body: Any, phrase_token: Optional[str] = None
    ) -> ScimUserCoreDto:
        """
        Patch user using SCIM

        :param userId: integer (required), path.
        :param body: Any (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ScimUserCoreDto
        """
        endpoint = f"/api2/v1/scim/Users/{userId}"
        params = {}

        files = None
        payload = body

        r = await self.client.patch(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ScimUserCoreDto(**r)

    async def searchUsers(
        self,
        sortBy: str = None,
        attributes: str = None,
        filter: str = None,
        sortOrder: str = "ascending",
        startIndex: int = "1",
        count: int = "50",
        phrase_token: Optional[str] = None,
    ) -> Any:
        """
                Search users
                This operation supports <a href="http://ldapwiki.com/wiki/SCIM%20Filtering" target="_blank">SCIM Filter</a>,
        <a href="http://ldapwiki.com/wiki/SCIM%20Search%20Request" target="_blank">SCIM attributes</a> and
        <a href="http://ldapwiki.com/wiki/SCIM%20Sorting" target="_blank">SCIM sort</a>

        Supported attributes:
          - `id`
          - `active`
          - `userName`
          - `name.givenName`
          - `name.familyName`
          - `emails.value`
          - `meta.created`
                :param sortBy: string (optional), query. See method description.
                :param attributes: string (optional), query. See method description.
                :param filter: string (optional), query. See method description.
                :param sortOrder: string (optional), query. See method description.
                :param startIndex: integer (optional), query. The 1-based index of the first search result. Default 1.
                :param count: integer (optional), query. Non-negative Integer. Specifies the desired maximum number of search results per page; e.g., 10..

                :param phrase_token: string (optional) - if not supplied, client will look token from init

                :return:
        """
        endpoint = f"/api2/v1/scim/Users"
        params = {
            "filter": filter,
            "attributes": attributes,
            "sortBy": sortBy,
            "sortOrder": sortOrder,
            "startIndex": startIndex,
            "count": count,
        }

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return r

    async def createUserSCIM(
        self, body: ScimUserCoreDto, phrase_token: Optional[str] = None
    ) -> ScimUserCoreDto:
        """
                Create user using SCIM
                Supported schema: `"urn:ietf:params:scim:schemas:core:2.0:User"`

        Create active user:
        ```
        {
            "schemas": [
                "urn:ietf:params:scim:schemas:core:2.0:User"
            ],
            "active": true,
            "userName": "john.doe",
            "emails": [
                {
                    "primary": true,
                    "value": "john.doe@example.com",
                    "type": "work"
                }
            ],
            "name": {
                "givenName": "John",
                "familyName": "Doe"
            }
        }
        ```
                :param body: ScimUserCoreDto (required), body.

                :param phrase_token: string (optional) - if not supplied, client will look token from init

                :return: ScimUserCoreDto
        """
        endpoint = f"/api2/v1/scim/Users"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ScimUserCoreDto(**r)
