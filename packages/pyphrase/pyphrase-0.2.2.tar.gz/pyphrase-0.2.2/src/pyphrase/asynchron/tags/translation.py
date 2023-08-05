from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    AsyncRequestWrapperDto,
    AsyncRequestWrapperV2Dto,
    HumanTranslateJobsDto,
    MachineTranslateResponse,
    PreTranslateJobsV2Dto,
    TranslationRequestDto,
)


class TranslationOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def humanTranslate(
        self,
        projectUid: str,
        body: HumanTranslateJobsDto,
        phrase_token: Optional[str] = None,
    ) -> AsyncRequestWrapperDto:
        """
        Human translate (Gengo or Unbabel)

        :param projectUid: string (required), path.
        :param body: HumanTranslateJobsDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AsyncRequestWrapperDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/humanTranslate"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AsyncRequestWrapperDto(**r)

    async def machineTranslationJob(
        self,
        jobUid: str,
        projectUid: str,
        body: TranslationRequestDto,
        phrase_token: Optional[str] = None,
    ) -> MachineTranslateResponse:
        """
        Translate using machine translation
        Configured machine translate settings is used
        :param jobUid: string (required), path.
        :param projectUid: string (required), path.
        :param body: TranslationRequestDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: MachineTranslateResponse
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/translations/translateWithMachineTranslation"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return MachineTranslateResponse(**r)

    async def preTranslate_1(
        self,
        projectUid: str,
        body: PreTranslateJobsV2Dto,
        phrase_token: Optional[str] = None,
    ) -> AsyncRequestWrapperV2Dto:
        """
        Pre-translate job

        :param projectUid: string (required), path.
        :param body: PreTranslateJobsV2Dto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AsyncRequestWrapperV2Dto
        """
        endpoint = f"/api2/v2/projects/{projectUid}/jobs/preTranslate"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AsyncRequestWrapperV2Dto(**r)
