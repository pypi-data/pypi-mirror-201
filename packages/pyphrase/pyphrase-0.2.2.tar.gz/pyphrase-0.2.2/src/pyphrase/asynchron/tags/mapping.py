from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import TaskMappingDto


class MappingOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def getMappingForTask(
        self, id: str, workflowLevel: int = "1", phrase_token: Optional[str] = None
    ) -> TaskMappingDto:
        """
        Returns mapping for taskId (mxliff)

        :param id: string (required), path.
        :param workflowLevel: integer (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: TaskMappingDto
        """
        endpoint = f"/api2/v1/mappings/tasks/{id}"
        params = {"workflowLevel": workflowLevel}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return TaskMappingDto(**r)
