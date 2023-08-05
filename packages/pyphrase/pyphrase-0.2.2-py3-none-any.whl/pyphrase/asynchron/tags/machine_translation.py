from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    MachineTranslateResponse,
    TranslationRequestExtendedDto,
)


class MachineTranslationOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def machineTranslation(
        self,
        mtSettingsUid: str,
        body: TranslationRequestExtendedDto,
        phrase_token: Optional[str] = None,
    ) -> MachineTranslateResponse:
        """
        Translate with MT

        :param mtSettingsUid: string (required), path.
        :param body: TranslationRequestExtendedDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: MachineTranslateResponse
        """
        endpoint = f"/api2/v1/machineTranslations/{mtSettingsUid}/translate"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return MachineTranslateResponse(**r)
