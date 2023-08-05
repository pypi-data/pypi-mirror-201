from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import Response, WorkflowChangesDto


class WorkflowChangesOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def downloadWorkflowChanges(
        self, body: WorkflowChangesDto, phrase_token: Optional[str] = None
    ) -> Response:
        """
        Download workflow changes report

        :param body: WorkflowChangesDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: Response
        """
        endpoint = f"/api2/v2/jobs/workflowChanges"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return Response(**r)
