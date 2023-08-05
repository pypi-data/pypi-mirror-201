from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from pyphrase.client import AsyncPhraseTMSClient

from pyphrase.models.phrase_models import (
    WEBHOOK_TOKEN,
    AutomatedProjectCreationDtoV2,
    CreateEditAutomatedProjectCreationDtoV2,
    PageDtoAutomatedProjectCreationSimpleDto,
)


class AutomationsOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def checkNowAutomatedProjectCreation(
        self, phrase_token: str, settingsId: str
    ) -> None:
        """
        Check remote service status for automated project settings

        :param phrase_token: string (required) - token to authenticate
        :param settingsId: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/automatedProjects/{settingsId}/checkNow"
        params = {}

        files = None
        payload = None

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def forceImportAutomatedProjectCreation(
        self, phrase_token: str, settingsId: str
    ) -> None:
        """
        Call force import for automated project settings

        :param phrase_token: string (required) - token to authenticate
        :param settingsId: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/automatedProjects/{settingsId}/forceImport"
        params = {}

        files = None
        payload = None

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def getAutomatedProjectCreationWebhook(
        self,
        phrase_token: str,
    ) -> WEBHOOK_TOKEN:
        """
        Generate run-APC webhook

        :param phrase_token: string (required) - token to authenticate

        :return: WEBHOOK_TOKEN
        """
        endpoint = f"/api2/v1/automatedProjects/generateWebhook"
        params = {}

        files = None
        payload = None

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return WEBHOOK_TOKEN(**r)

    async def executeAutomatedProjectCreationWebhook(
        self, phrase_token: str, webhookToken: str
    ) -> WEBHOOK_TOKEN:
        """
        Webhook to trigger APC run

        :param phrase_token: string (required) - token to authenticate
        :param webhookToken: string (required), path.

        :return: WEBHOOK_TOKEN
        """
        endpoint = f"/api2/v1/automatedProjects/webhooks/{webhookToken}"
        params = {}

        files = None
        payload = None

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return WEBHOOK_TOKEN(**r)

    async def getAutomatedProjectCreationList(
        self, phrase_token: str, pageNumber: int = "0", pageSize: int = "50"
    ) -> PageDtoAutomatedProjectCreationSimpleDto:
        """
        List automated project creation settings

        :param phrase_token: string (required) - token to authenticate
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :return: PageDtoAutomatedProjectCreationSimpleDto
        """
        endpoint = f"/api2/v1/automatedProjects"
        params = {"pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return PageDtoAutomatedProjectCreationSimpleDto(**r)

    async def deleteAutomatedProjectCreation(
        self, phrase_token: str, settingsId: str
    ) -> None:
        """
        Delete automated project settings

        :param phrase_token: string (required) - token to authenticate
        :param settingsId: string (required), path.

        :return: None
        """
        endpoint = f"/api2/v1/automatedProjects/{settingsId}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return

    async def getAutomatedProjectCreation_1(
        self, phrase_token: str, settingsId: str
    ) -> AutomatedProjectCreationDtoV2:
        """
        Get automated project creation settings by ID

        :param phrase_token: string (required) - token to authenticate
        :param settingsId: string (required), path.

        :return: AutomatedProjectCreationDtoV2
        """
        endpoint = f"/api2/v2/automatedProjects/{settingsId}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AutomatedProjectCreationDtoV2(**r)

    async def updateAutomatedProjectCreation_1(
        self,
        phrase_token: str,
        settingsId: str,
        body: CreateEditAutomatedProjectCreationDtoV2,
    ) -> AutomatedProjectCreationDtoV2:
        """
        Update automated project settings

        :param phrase_token: string (required) - token to authenticate
        :param settingsId: string (required), path.
        :param body: CreateEditAutomatedProjectCreationDtoV2 (required), body.

        :return: AutomatedProjectCreationDtoV2
        """
        endpoint = f"/api2/v2/automatedProjects/{settingsId}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AutomatedProjectCreationDtoV2(**r)

    async def createAutomatedProjectCreation_1(
        self, phrase_token: str, body: CreateEditAutomatedProjectCreationDtoV2
    ) -> AutomatedProjectCreationDtoV2:
        """
        Create automated project settings

        :param phrase_token: string (required) - token to authenticate
        :param body: CreateEditAutomatedProjectCreationDtoV2 (required), body.

        :return: AutomatedProjectCreationDtoV2
        """
        endpoint = f"/api2/v2/automatedProjects"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            phrase_token, endpoint, params=params, payload=payload, files=files
        )

        return AutomatedProjectCreationDtoV2(**r)
