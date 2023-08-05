from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    AsyncExportTMByQueryResponseDto,
    AsyncExportTMResponseDto,
    AsyncRequestWrapperDto,
    AsyncRequestWrapperV2Dto,
    BackgroundTasksTmDto,
    CleanedTransMemoriesDto,
    ExportByQueryDto,
    ExportTMDto,
    InputStream,
    MetadataResponse,
    PageDtoAbstractProjectDto,
    PageDtoTransMemoryDto,
    SearchRequestDto,
    SearchResponseListTmDto,
    SearchTMByJobRequestDto,
    SegmentDto,
    TargetLanguageDto,
    TranslationDto,
    TransMemoryCreateDto,
    TransMemoryDto,
    TransMemoryEditDto,
    WildCardSearchRequestDto,
)


class TranslationMemoryOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def searchSegmentByJob(
        self,
        jobUid: str,
        projectUid: str,
        body: SearchTMByJobRequestDto,
        phrase_token: Optional[str] = None,
    ) -> SearchResponseListTmDto:
        """
        Search translation memory for segment by job
        Returns at most <i>maxSegments</i>
            records with <i>score >= scoreThreshold</i> and at most <i>maxSubsegments</i> records which are subsegment,
            i.e. the source text is substring of the query text.
        :param jobUid: string (required), path.
        :param projectUid: string (required), path.
        :param body: SearchTMByJobRequestDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: SearchResponseListTmDto
        """
        endpoint = (
            f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/transMemories/searchSegment"
        )
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return SearchResponseListTmDto(**r)

    def search(
        self,
        transMemoryUid: str,
        body: SearchRequestDto,
        phrase_token: Optional[str] = None,
    ) -> SearchResponseListTmDto:
        """
        Search translation memory (sync)

        :param transMemoryUid: string (required), path.
        :param body: SearchRequestDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: SearchResponseListTmDto
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}/search"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return SearchResponseListTmDto(**r)

    def listTransMemories(
        self,
        businessUnitId: str = None,
        subDomainId: str = None,
        domainId: str = None,
        clientId: str = None,
        targetLang: str = None,
        sourceLang: str = None,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoTransMemoryDto:
        """
        List translation memories

        :param businessUnitId: string (optional), query.
        :param subDomainId: string (optional), query.
        :param domainId: string (optional), query.
        :param clientId: string (optional), query.
        :param targetLang: string (optional), query.
        :param sourceLang: string (optional), query.
        :param name: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoTransMemoryDto
        """
        endpoint = f"/api2/v1/transMemories"
        params = {
            "name": name,
            "sourceLang": sourceLang,
            "targetLang": targetLang,
            "clientId": clientId,
            "domainId": domainId,
            "subDomainId": subDomainId,
            "businessUnitId": businessUnitId,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
        }

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoTransMemoryDto(**r)

    def createTransMemory(
        self,
        body: TransMemoryCreateDto,
        phrase_token: Optional[str] = None,
    ) -> TransMemoryDto:
        """
        Create translation memory

        :param body: TransMemoryCreateDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: TransMemoryDto
        """
        endpoint = f"/api2/v1/transMemories"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return TransMemoryDto(**r)

    def exportCleanedTMs(
        self,
        body: CleanedTransMemoriesDto,
        phrase_token: Optional[str] = None,
    ) -> AsyncRequestWrapperDto:
        """
        Extract cleaned translation memory
        Returns a ZIP file containing the cleaned translation memories in the specified outputFormat.
        :param body: CleanedTransMemoriesDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AsyncRequestWrapperDto
        """
        endpoint = f"/api2/v1/transMemories/extractCleaned"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AsyncRequestWrapperDto(**r)

    def getTransMemory(
        self,
        transMemoryUid: str,
        phrase_token: Optional[str] = None,
    ) -> TransMemoryDto:
        """
        Get translation memory

        :param transMemoryUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: TransMemoryDto
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return TransMemoryDto(**r)

    def editTransMemory(
        self,
        transMemoryUid: str,
        body: TransMemoryEditDto,
        phrase_token: Optional[str] = None,
    ) -> TransMemoryDto:
        """
        Edit translation memory

        :param transMemoryUid: string (required), path.
        :param body: TransMemoryEditDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: TransMemoryDto
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return TransMemoryDto(**r)

    def deleteTransMemory(
        self,
        transMemoryUid: str,
        purge: bool = "False",
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete translation memory

        :param transMemoryUid: string (required), path.
        :param purge: boolean (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}"
        params = {"purge": purge}

        files = None
        payload = None

        r = self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def addTargetLangToTransMemory(
        self,
        transMemoryUid: str,
        body: TargetLanguageDto,
        phrase_token: Optional[str] = None,
    ) -> TransMemoryDto:
        """
        Add target language to translation memory

        :param transMemoryUid: string (required), path.
        :param body: TargetLanguageDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: TransMemoryDto
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}/targetLanguages"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return TransMemoryDto(**r)

    def downloadCleanedTM(
        self, asyncRequestId: str, phrase_token: Optional[str] = None
    ) -> bytes:
        """
        Download cleaned TM

        :param asyncRequestId: string (required), path. Request ID.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/transMemories/downloadCleaned/{asyncRequestId}"
        params = {}

        files = None
        payload = None

        r = self.client.get_bytestream(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return r

    def insertToTransMemory(
        self,
        transMemoryUid: str,
        body: SegmentDto,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Insert segment

        :param transMemoryUid: string (required), path.
        :param body: SegmentDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}/segments"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def clearTransMemory(
        self,
        transMemoryUid: str,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete all segments

        :param transMemoryUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}/segments"
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def getRelatedProjects(
        self,
        transMemoryUid: str,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoAbstractProjectDto:
        """
        List related projects

        :param transMemoryUid: string (required), path.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoAbstractProjectDto
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}/relatedProjects"
        params = {"pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoAbstractProjectDto(**r)

    def getMetadata(
        self,
        transMemoryUid: str,
        byLanguage: bool = "False",
        phrase_token: Optional[str] = None,
    ) -> MetadataResponse:
        """
        Get translation memory metadata

        :param transMemoryUid: string (required), path.
        :param byLanguage: boolean (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: MetadataResponse
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}/metadata"
        params = {"byLanguage": byLanguage}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return MetadataResponse(**r)

    def updateTranslation(
        self,
        segmentId: str,
        transMemoryUid: str,
        body: TranslationDto,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Edit segment

        :param segmentId: string (required), path.
        :param transMemoryUid: string (required), path.
        :param body: TranslationDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}/segments/{segmentId}"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def deleteSourceAndTranslations(
        self,
        segmentId: str,
        transMemoryUid: str,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete both source and translation
        Not recommended for bulk removal of segments
        :param segmentId: string (required), path.
        :param transMemoryUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}/segments/{segmentId}"
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def deleteTranslation(
        self,
        lang: str,
        segmentId: str,
        transMemoryUid: str,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete segment of given language
        Not recommended for bulk removal of segments
        :param lang: string (required), path.
        :param segmentId: string (required), path.
        :param transMemoryUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = (
            f"/api2/v1/transMemories/{transMemoryUid}/segments/{segmentId}/lang/{lang}"
        )
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def getBackgroundTasks_1(
        self,
        transMemoryUid: str,
        phrase_token: Optional[str] = None,
    ) -> BackgroundTasksTmDto:
        """
        Get last task information

        :param transMemoryUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: BackgroundTasksTmDto
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}/lastBackgroundTask"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return BackgroundTasksTmDto(**r)

    def wildcardSearch(
        self,
        transMemoryUid: str,
        body: WildCardSearchRequestDto,
        phrase_token: Optional[str] = None,
    ) -> SearchResponseListTmDto:
        """
        Wildcard search

        :param transMemoryUid: string (required), path.
        :param body: WildCardSearchRequestDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: SearchResponseListTmDto
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}/wildCardSearch"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return SearchResponseListTmDto(**r)

    def downloadSearchResult(
        self,
        asyncRequestId: str,
        fields: List[str] = None,
        format: str = "TMX",
        phrase_token: Optional[str] = None,
    ) -> bytes:
        """
        Download export

        :param asyncRequestId: string (required), path. Request ID.
        :param fields: array (optional), query. Fields to include in exported XLSX.
        :param format: string (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/transMemories/downloadExport/{asyncRequestId}"
        params = {"format": format, "fields": fields}

        files = None
        payload = None

        r = self.client.get_bytestream(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return r

    def exportByQueryAsync(
        self,
        transMemoryUid: str,
        body: ExportByQueryDto,
        phrase_token: Optional[str] = None,
    ) -> AsyncExportTMByQueryResponseDto:
        """
        Search translation memory
        Use [this API](#operation/downloadSearchResult) to download result
        :param transMemoryUid: string (required), path.
        :param body: ExportByQueryDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AsyncExportTMByQueryResponseDto
        """
        endpoint = f"/api2/v1/transMemories/{transMemoryUid}/exportByQueryAsync"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AsyncExportTMByQueryResponseDto(**r)

    def clearTransMemoryV2(
        self,
        transMemoryUid: str,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete all segments.
        This call is **asynchronous**, use [this API](#operation/getAsyncRequest) to check the result
        :param transMemoryUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v2/transMemories/{transMemoryUid}/segments"
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def importTransMemoryV2(
        self,
        transMemoryUid: str,
        body: InputStream,
        strictLangMatching: bool = "False",
        stripNativeCodes: bool = "True",
        phrase_token: Optional[str] = None,
    ) -> AsyncRequestWrapperV2Dto:
        """
        Import TMX

        :param transMemoryUid: string (required), path.
        :param body: InputStream (required), body.
        :param strictLangMatching: boolean (optional), query.
        :param stripNativeCodes: boolean (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AsyncRequestWrapperV2Dto
        """
        endpoint = f"/api2/v2/transMemories/{transMemoryUid}/import"
        params = {
            "strictLangMatching": strictLangMatching,
            "stripNativeCodes": stripNativeCodes,
        }

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AsyncRequestWrapperV2Dto(**r)

    def exportV2(
        self,
        transMemoryUid: str,
        body: ExportTMDto,
        phrase_token: Optional[str] = None,
    ) -> AsyncExportTMResponseDto:
        """
        Export translation memory
        Use [this API](#operation/downloadSearchResult) to download result
        :param transMemoryUid: string (required), path.
        :param body: ExportTMDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AsyncExportTMResponseDto
        """
        endpoint = f"/api2/v2/transMemories/{transMemoryUid}/export"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AsyncExportTMResponseDto(**r)
