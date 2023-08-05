from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    AnalyseJobDto,
    AnalyseLanguagePartDto,
    AnalyseRecalculateRequestDto,
    AnalyseRecalculateResponseDto,
    AnalysesV2Dto,
    AnalyseV2Dto,
    AnalyseV3Dto,
    AsyncAnalyseListResponseDto,
    AsyncAnalyseListResponseV2Dto,
    BulkDeleteAnalyseDto,
    BulkEditAnalyseV2Dto,
    CreateAnalyseAsyncV2Dto,
    CreateAnalyseListAsyncDto,
    EditAnalyseV2Dto,
    PageDtoAnalyseJobDto,
    PageDtoAnalyseReference,
)


class AnalysisOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def delete(
        self,
        analyseUid: str,
        purge: bool = None,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete analysis

        :param analyseUid: string (required), path.
        :param purge: boolean (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/analyses/{analyseUid}"
        params = {"purge": purge}

        files = None
        payload = None

        r = self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def bulkDeleteAnalyses(
        self,
        body: BulkDeleteAnalyseDto,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete analyses (batch)

        :param body: BulkDeleteAnalyseDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/analyses/bulk"
        params = {}

        files = None
        payload = body

        r = self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def recalculate(
        self,
        body: AnalyseRecalculateRequestDto,
        phrase_token: Optional[str] = None,
    ) -> AnalyseRecalculateResponseDto:
        """
        Recalculate analysis

        :param body: AnalyseRecalculateRequestDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AnalyseRecalculateResponseDto
        """
        endpoint = f"/api2/v1/analyses/recalculate"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AnalyseRecalculateResponseDto(**r)

    def downloadAnalyse(
        self, analyseUid: str, format: str, phrase_token: Optional[str] = None
    ) -> bytes:
        """
        Download analysis

        :param analyseUid: string (required), path.
        :param format: string (required), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/analyses/{analyseUid}/download"
        params = {"format": format}

        files = None
        payload = None

        r = self.client.get_bytestream(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return r

    def createAnalysesForProviders(
        self,
        body: CreateAnalyseListAsyncDto,
        phrase_token: Optional[str] = None,
    ) -> AsyncAnalyseListResponseDto:
        """
        Create analyses by providers

        :param body: CreateAnalyseListAsyncDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AsyncAnalyseListResponseDto
        """
        endpoint = f"/api2/v1/analyses/byProviders"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AsyncAnalyseListResponseDto(**r)

    def createAnalysesForLangs(
        self,
        body: CreateAnalyseListAsyncDto,
        phrase_token: Optional[str] = None,
    ) -> AsyncAnalyseListResponseDto:
        """
        Create analyses by languages

        :param body: CreateAnalyseListAsyncDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AsyncAnalyseListResponseDto
        """
        endpoint = f"/api2/v1/analyses/byLanguages"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AsyncAnalyseListResponseDto(**r)

    def listJobParts(
        self,
        analyseLanguagePartId: int,
        analyseUid: str,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoAnalyseJobDto:
        """
        List jobs of analyses
        Returns list of job's analyses
        :param analyseLanguagePartId: integer (required), path.
        :param analyseUid: string (required), path.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoAnalyseJobDto
        """
        endpoint = f"/api2/v1/analyses/{analyseUid}/analyseLanguageParts/{analyseLanguagePartId}/jobs"
        params = {"pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoAnalyseJobDto(**r)

    def getAnalyseLanguagePart(
        self,
        analyseLanguagePartId: int,
        analyseUid: str,
        phrase_token: Optional[str] = None,
    ) -> AnalyseLanguagePartDto:
        """
        Get analysis language part
        Returns analysis language pair
        :param analyseLanguagePartId: integer (required), path.
        :param analyseUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AnalyseLanguagePartDto
        """
        endpoint = f"/api2/v1/analyses/{analyseUid}/analyseLanguageParts/{analyseLanguagePartId}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AnalyseLanguagePartDto(**r)

    def getJobPartAnalyse(
        self,
        jobUid: str,
        analyseUid: str,
        phrase_token: Optional[str] = None,
    ) -> AnalyseJobDto:
        """
        Get jobs analysis
        Returns job's analyse
        :param jobUid: string (required), path.
        :param analyseUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AnalyseJobDto
        """
        endpoint = f"/api2/v1/analyses/{analyseUid}/jobs/{jobUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AnalyseJobDto(**r)

    def editAnalysis(
        self,
        analyseUid: str,
        body: EditAnalyseV2Dto,
        phrase_token: Optional[str] = None,
    ) -> AnalyseV2Dto:
        """
                Edit analysis
                If no netRateScheme is provided in
        request, then netRateScheme associated with provider will be used if it exists, otherwise it will remain the same
        as it was.
                :param analyseUid: string (required), path.
                :param body: EditAnalyseV2Dto (required), body.

                :param phrase_token: string (optional) - if not supplied, client will look token from init

                :return: AnalyseV2Dto
        """
        endpoint = f"/api2/v2/analyses/{analyseUid}"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AnalyseV2Dto(**r)

    def createAnalyseAsync_1(
        self,
        body: CreateAnalyseAsyncV2Dto,
        phrase_token: Optional[str] = None,
    ) -> AsyncAnalyseListResponseV2Dto:
        """
        Create analysis
        Returns created analyses - batching analyses by number of segments (api.segment.count.approximation, default 100000), in case request contains more segments than maximum (api.segment.max.count, default 300000), returns 400 bad request.
        :param body: CreateAnalyseAsyncV2Dto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AsyncAnalyseListResponseV2Dto
        """
        endpoint = f"/api2/v2/analyses"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AsyncAnalyseListResponseV2Dto(**r)

    def analyses_batchEdit_v2(
        self,
        body: BulkEditAnalyseV2Dto,
        phrase_token: Optional[str] = None,
    ) -> AnalysesV2Dto:
        """
                Edit analyses (batch)
                If no netRateScheme is provided in request, then netRateScheme associated with provider will
        be used if it exists, otherwise it will remain the same as it was.
                :param body: BulkEditAnalyseV2Dto (required), body.

                :param phrase_token: string (optional) - if not supplied, client will look token from init

                :return: AnalysesV2Dto
        """
        endpoint = f"/api2/v2/analyses/bulk"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AnalysesV2Dto(**r)

    def getAnalyseV3(
        self,
        analyseUid: str,
        phrase_token: Optional[str] = None,
    ) -> AnalyseV3Dto:
        """
        Get analysis

        :param analyseUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AnalyseV3Dto
        """
        endpoint = f"/api2/v3/analyses/{analyseUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AnalyseV3Dto(**r)

    def listPartAnalyseV3(
        self,
        jobUid: str,
        projectUid: str,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoAnalyseReference:
        """
        List analyses

        :param jobUid: string (required), path.
        :param projectUid: string (required), path.
        :param pageNumber: integer (optional), query.
        :param pageSize: integer (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoAnalyseReference
        """
        endpoint = f"/api2/v3/projects/{projectUid}/jobs/{jobUid}/analyses"
        params = {"pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoAnalyseReference(**r)
