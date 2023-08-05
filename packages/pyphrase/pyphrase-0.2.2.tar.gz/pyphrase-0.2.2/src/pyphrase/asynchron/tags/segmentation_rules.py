from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    EditSegmentationRuleDto,
    InputStream,
    PageDtoSegmentationRuleReference,
    SegmentationRuleDto,
)


class SegmentationRulesOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def getListOfSegmentationRules(
        self,
        locales: List[str] = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoSegmentationRuleReference:
        """
        List segmentation rules

        :param locales: array (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoSegmentationRuleReference
        """
        endpoint = f"/api2/v1/segmentationRules"
        params = {"locales": locales, "pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoSegmentationRuleReference(**r)

    async def createSegmentationRule(
        self, body: InputStream, phrase_token: Optional[str] = None
    ) -> SegmentationRuleDto:
        """
        Create segmentation rule
        Creates new Segmentation Rule with file and segRule JSON Object as header parameter. The same object is used for GET action.
        :param body: InputStream (required), body. streamed file.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: SegmentationRuleDto
        """
        endpoint = f"/api2/v1/segmentationRules"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return SegmentationRuleDto(**r)

    async def getSegmentationRule(
        self, segRuleId: int, phrase_token: Optional[str] = None
    ) -> SegmentationRuleDto:
        """
        Get segmentation rule

        :param segRuleId: integer (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: SegmentationRuleDto
        """
        endpoint = f"/api2/v1/segmentationRules/{segRuleId}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return SegmentationRuleDto(**r)

    async def updatesSegmentationRule(
        self,
        segRuleId: int,
        body: EditSegmentationRuleDto,
        phrase_token: Optional[str] = None,
    ) -> SegmentationRuleDto:
        """
        Edit segmentation rule

        :param segRuleId: integer (required), path.
        :param body: EditSegmentationRuleDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: SegmentationRuleDto
        """
        endpoint = f"/api2/v1/segmentationRules/{segRuleId}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return SegmentationRuleDto(**r)

    async def deletesSegmentationRule(
        self, segRuleId: int, phrase_token: Optional[str] = None
    ) -> None:
        """
        Delete segmentation rule

        :param segRuleId: integer (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/segmentationRules/{segRuleId}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return
