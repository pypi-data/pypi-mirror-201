from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    OrganizationEmailTemplateDto,
    PageDtoOrganizationEmailTemplateDto,
)


class EmailTemplateOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def getOrgEmailTemplate(
        self, templateUid: str, phrase_token: Optional[str] = None
    ) -> OrganizationEmailTemplateDto:
        """
        Get email template

        :param templateUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: OrganizationEmailTemplateDto
        """
        endpoint = f"/api2/v1/emailTemplates/{templateUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return OrganizationEmailTemplateDto(**r)

    async def listOrgEmailTemplates(
        self,
        type: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoOrganizationEmailTemplateDto:
        """
        List email templates

        :param type: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoOrganizationEmailTemplateDto
        """
        endpoint = f"/api2/v1/emailTemplates"
        params = {"type": type, "pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoOrganizationEmailTemplateDto(**r)
