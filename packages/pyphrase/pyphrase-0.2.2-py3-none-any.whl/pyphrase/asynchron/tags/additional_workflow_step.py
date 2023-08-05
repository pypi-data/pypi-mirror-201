from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    AdditionalWorkflowStepDto,
    AdditionalWorkflowStepRequestDto,
    PageDtoAdditionalWorkflowStepDto,
)


class AdditionalWorkflowStepOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def deleteAWFStep(self, id: str, phrase_token: Optional[str] = None) -> None:
        """
        Delete additional workflow step

        :param id: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/additionalWorkflowSteps/{id}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def listAWFSteps(
        self,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoAdditionalWorkflowStepDto:
        """
        List additional workflow steps

        :param name: string (optional), query. Name of the additional workflow step to filter.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoAdditionalWorkflowStepDto
        """
        endpoint = f"/api2/v1/additionalWorkflowSteps"
        params = {"pageNumber": pageNumber, "pageSize": pageSize, "name": name}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoAdditionalWorkflowStepDto(**r)

    async def createAWFStep(
        self, body: AdditionalWorkflowStepRequestDto, phrase_token: Optional[str] = None
    ) -> AdditionalWorkflowStepDto:
        """
        Create additional workflow step

        :param body: AdditionalWorkflowStepRequestDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AdditionalWorkflowStepDto
        """
        endpoint = f"/api2/v1/additionalWorkflowSteps"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AdditionalWorkflowStepDto(**r)
