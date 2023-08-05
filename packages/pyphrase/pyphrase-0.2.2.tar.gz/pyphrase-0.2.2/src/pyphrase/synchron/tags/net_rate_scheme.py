from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    DiscountSchemeCreateDto,
    NetRateScheme,
    NetRateSchemeEdit,
    NetRateSchemeWorkflowStep,
    NetRateSchemeWorkflowStepEdit,
    PageDtoNetRateSchemeReference,
    PageDtoNetRateSchemeWorkflowStepReference,
)


class NetRateSchemeOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def getDiscountScheme(
        self,
        netRateSchemeUid: str,
        phrase_token: Optional[str] = None,
    ) -> NetRateScheme:
        """
        Get net rate scheme

        :param netRateSchemeUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: NetRateScheme
        """
        endpoint = f"/api2/v1/netRateSchemes/{netRateSchemeUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return NetRateScheme(**r)

    def updateDiscountScheme(
        self,
        netRateSchemeUid: str,
        body: NetRateSchemeEdit,
        phrase_token: Optional[str] = None,
    ) -> NetRateScheme:
        """
        Edit net rate scheme

        :param netRateSchemeUid: string (required), path.
        :param body: NetRateSchemeEdit (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: NetRateScheme
        """
        endpoint = f"/api2/v1/netRateSchemes/{netRateSchemeUid}"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return NetRateScheme(**r)

    def getDiscountSchemes(
        self,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoNetRateSchemeReference:
        """
        List net rate schemes

        :param pageNumber: integer (optional), query.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoNetRateSchemeReference
        """
        endpoint = f"/api2/v1/netRateSchemes"
        params = {"pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoNetRateSchemeReference(**r)

    def createDiscountScheme(
        self,
        body: DiscountSchemeCreateDto,
        phrase_token: Optional[str] = None,
    ) -> NetRateScheme:
        """
        Create net rate scheme

        :param body: DiscountSchemeCreateDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: NetRateScheme
        """
        endpoint = f"/api2/v1/netRateSchemes"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return NetRateScheme(**r)

    def getDiscountSchemeWorkflowStep(
        self,
        netRateSchemeWorkflowStepId: int,
        netRateSchemeUid: str,
        phrase_token: Optional[str] = None,
    ) -> NetRateSchemeWorkflowStep:
        """
        Get scheme for workflow step

        :param netRateSchemeWorkflowStepId: integer (required), path.
        :param netRateSchemeUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: NetRateSchemeWorkflowStep
        """
        endpoint = f"/api2/v1/netRateSchemes/{netRateSchemeUid}/workflowStepNetSchemes/{netRateSchemeWorkflowStepId}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return NetRateSchemeWorkflowStep(**r)

    def editDiscountSchemeWorkflowStep(
        self,
        netRateSchemeWorkflowStepId: int,
        netRateSchemeUid: str,
        body: NetRateSchemeWorkflowStepEdit,
        phrase_token: Optional[str] = None,
    ) -> NetRateSchemeWorkflowStep:
        """
        Edit scheme for workflow step

        :param netRateSchemeWorkflowStepId: integer (required), path.
        :param netRateSchemeUid: string (required), path.
        :param body: NetRateSchemeWorkflowStepEdit (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: NetRateSchemeWorkflowStep
        """
        endpoint = f"/api2/v1/netRateSchemes/{netRateSchemeUid}/workflowStepNetSchemes/{netRateSchemeWorkflowStepId}"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return NetRateSchemeWorkflowStep(**r)

    def getDiscountSchemeWorkflowSteps(
        self,
        netRateSchemeUid: str,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoNetRateSchemeWorkflowStepReference:
        """
        List schemes for workflow step

        :param netRateSchemeUid: string (required), path.
        :param pageNumber: integer (optional), query.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoNetRateSchemeWorkflowStepReference
        """
        endpoint = f"/api2/v1/netRateSchemes/{netRateSchemeUid}/workflowStepNetSchemes"
        params = {"pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoNetRateSchemeWorkflowStepReference(**r)
