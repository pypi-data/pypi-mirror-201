from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    CreateWorkflowStepDto,
    EditWorkflowStepDto,
    PageDtoWorkflowStepDto,
    WorkflowStepDto,
)


class WorkflowStepOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def listWFSteps(
        self,
        abbr: str = None,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoWorkflowStepDto:
        """
        List workflow steps

        :param abbr: string (optional), query. Abbreviation of workflow step.
        :param name: string (optional), query. Name of the workflow step.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoWorkflowStepDto
        """
        endpoint = f"/api2/v1/workflowSteps"
        params = {
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "name": name,
            "abbr": abbr,
        }

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoWorkflowStepDto(**r)

    def createWFStep(
        self,
        body: CreateWorkflowStepDto,
        phrase_token: Optional[str] = None,
    ) -> WorkflowStepDto:
        """
        Create workflow step

        :param body: CreateWorkflowStepDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: WorkflowStepDto
        """
        endpoint = f"/api2/v1/workflowSteps"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return WorkflowStepDto(**r)

    def editWFStep(
        self,
        workflowStepUid: str,
        body: EditWorkflowStepDto,
        phrase_token: Optional[str] = None,
    ) -> WorkflowStepDto:
        """
        Edit workflow step

        :param workflowStepUid: string (required), path.
        :param body: EditWorkflowStepDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: WorkflowStepDto
        """
        endpoint = f"/api2/v1/workflowSteps/{workflowStepUid}"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return WorkflowStepDto(**r)
