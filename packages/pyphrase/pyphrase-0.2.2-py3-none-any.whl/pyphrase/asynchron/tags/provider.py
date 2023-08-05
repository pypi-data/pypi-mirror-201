from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import ProviderListDtoV2


class ProviderOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def listProviders_4(
        self, jobUid: str, projectUid: str, phrase_token: Optional[str] = None
    ) -> ProviderListDtoV2:
        """
        Get suggested providers

        :param jobUid: string (required), path.
        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProviderListDtoV2
        """
        endpoint = f"/api2/v2/projects/{projectUid}/jobs/{jobUid}/providers/suggest"
        params = {}

        files = None
        payload = None

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProviderListDtoV2(**r)
