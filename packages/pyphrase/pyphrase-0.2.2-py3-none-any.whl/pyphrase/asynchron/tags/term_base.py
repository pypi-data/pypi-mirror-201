from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    BackgroundTasksTbDto,
    BrowseRequestDto,
    BrowseResponseListDto,
    ConceptDto,
    ConceptEditDto,
    ConceptListReference,
    ConceptListResponseDto,
    ConceptWithMetadataDto,
    CreateTermsDto,
    ImportTermBaseResponseDto,
    InputStream,
    MetadataTbDto,
    PageDtoTermBaseDto,
    SearchInTextResponseList2Dto,
    SearchResponseListTbDto,
    SearchTbByJobRequestDto,
    SearchTbInTextByJobRequestDto,
    SearchTbResponseListDto,
    TermBaseDto,
    TermBaseEditDto,
    TermBaseSearchRequestDto,
    TermCreateDto,
    TermDto,
    TermEditDto,
    TermPairDto,
)


class TermBaseOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def createTermByJob(
        self,
        projectUid: str,
        jobUid: str,
        body: CreateTermsDto,
        phrase_token: Optional[str] = None,
    ) -> TermPairDto:
        """
        Create term in job's term bases
        Create new term in the write term base assigned to the job
        :param projectUid: string (required), path.
        :param jobUid: string (required), path.
        :param body: CreateTermsDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: TermPairDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/termBases/createByJob"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return TermPairDto(**r)

    async def getTermBase(
        self, termBaseUid: str, phrase_token: Optional[str] = None
    ) -> TermBaseDto:
        """
        Get term base

        :param termBaseUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: TermBaseDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return TermBaseDto(**r)

    async def updateTermBase(
        self,
        termBaseUid: str,
        body: TermBaseEditDto,
        phrase_token: Optional[str] = None,
    ) -> TermBaseDto:
        """
        Edit term base
        It is possible to add new languages only
        :param termBaseUid: string (required), path.
        :param body: TermBaseEditDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: TermBaseDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return TermBaseDto(**r)

    async def deleteTermBase(
        self,
        termBaseUid: str,
        purge: bool = "False",
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete term base

        :param termBaseUid: string (required), path.
        :param purge: boolean (optional), query. purge=false - the Termbase is can later be restored,
                    &#34;purge=true - the Termbase is completely deleted and cannot be restored.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}"
        params = {"purge": purge}

        files = None
        payload = None

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def listTermBases(
        self,
        subDomainId: str = None,
        domainId: str = None,
        clientId: str = None,
        lang: List[str] = None,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoTermBaseDto:
        """
        List term bases

        :param subDomainId: string (optional), query.
        :param domainId: string (optional), query.
        :param clientId: string (optional), query.
        :param lang: array (optional), query. Language of the term base.
        :param name: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoTermBaseDto
        """
        endpoint = f"/api2/v1/termBases"
        params = {
            "name": name,
            "lang": lang,
            "clientId": clientId,
            "domainId": domainId,
            "subDomainId": subDomainId,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
        }

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoTermBaseDto(**r)

    async def createTermBase(
        self, body: TermBaseEditDto, phrase_token: Optional[str] = None
    ) -> TermBaseDto:
        """
        Create term base

        :param body: TermBaseEditDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: TermBaseDto
        """
        endpoint = f"/api2/v1/termBases"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return TermBaseDto(**r)

    async def importTermBase(
        self,
        termBaseUid: str,
        body: InputStream,
        charset: str = "UTF-8",
        strictLangMatching: bool = "False",
        updateTerms: bool = "True",
        phrase_token: Optional[str] = None,
    ) -> ImportTermBaseResponseDto:
        """
                Upload term base
                Terms can be imported from XLS/XLSX and TBX file formats into a term base.
        See <a target="_blank" href="https://help.memsource.com/hc/en-us/articles/115003681851-Term-Bases">Memsource Wiki</a>
                :param termBaseUid: string (required), path.
                :param body: InputStream (required), body.
                :param charset: string (optional), query.
                :param strictLangMatching: boolean (optional), query.
                :param updateTerms: boolean (optional), query.

                :param phrase_token: string (optional) - if not supplied, client will look token from init

                :return: ImportTermBaseResponseDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/upload"
        params = {
            "charset": charset,
            "strictLangMatching": strictLangMatching,
            "updateTerms": updateTerms,
        }

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ImportTermBaseResponseDto(**r)

    async def listConcepts(
        self,
        termBaseUid: str,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> ConceptListResponseDto:
        """
        List concepts

        :param termBaseUid: string (required), path.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ConceptListResponseDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/concepts"
        params = {"pageNumber": pageNumber, "pageSize": pageSize}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ConceptListResponseDto(**r)

    async def createConcept(
        self, termBaseUid: str, body: ConceptEditDto, phrase_token: Optional[str] = None
    ) -> ConceptWithMetadataDto:
        """
        Create concept

        :param termBaseUid: string (required), path.
        :param body: ConceptEditDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ConceptWithMetadataDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/concepts"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ConceptWithMetadataDto(**r)

    async def deleteConcepts(
        self,
        termBaseUid: str,
        body: ConceptListReference,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete concepts

        :param termBaseUid: string (required), path.
        :param body: ConceptListReference (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/concepts"
        params = {}

        files = None
        payload = body

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def getConcept(
        self, conceptUid: str, termBaseUid: str, phrase_token: Optional[str] = None
    ) -> ConceptWithMetadataDto:
        """
        Get concept

        :param conceptUid: string (required), path.
        :param termBaseUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ConceptWithMetadataDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/concepts/{conceptUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ConceptWithMetadataDto(**r)

    async def updateConcept(
        self,
        conceptUid: str,
        termBaseUid: str,
        body: ConceptEditDto,
        phrase_token: Optional[str] = None,
    ) -> ConceptWithMetadataDto:
        """
        Update concept

        :param conceptUid: string (required), path.
        :param termBaseUid: string (required), path.
        :param body: ConceptEditDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ConceptWithMetadataDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/concepts/{conceptUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ConceptWithMetadataDto(**r)

    async def createTerm(
        self, termBaseUid: str, body: TermCreateDto, phrase_token: Optional[str] = None
    ) -> TermDto:
        """
        Create term
        Set conceptId to assign the term to an existing concept, otherwise a new concept will be created.
        :param termBaseUid: string (required), path.
        :param body: TermCreateDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: TermDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/terms"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return TermDto(**r)

    async def clearTermBase(
        self, termBaseUid: str, phrase_token: Optional[str] = None
    ) -> None:
        """
        Clear term base
        Deletes all terms
        :param termBaseUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/terms"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def getTerm(
        self, termId: str, termBaseUid: str, phrase_token: Optional[str] = None
    ) -> TermDto:
        """
        Get term

        :param termId: string (required), path.
        :param termBaseUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: TermDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/terms/{termId}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return TermDto(**r)

    async def updateTerm(
        self,
        termId: str,
        termBaseUid: str,
        body: TermEditDto,
        phrase_token: Optional[str] = None,
    ) -> TermDto:
        """
        Edit term

        :param termId: string (required), path.
        :param termBaseUid: string (required), path.
        :param body: TermEditDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: TermDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/terms/{termId}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return TermDto(**r)

    async def deleteTerm(
        self, termId: str, termBaseUid: str, phrase_token: Optional[str] = None
    ) -> None:
        """
        Delete term

        :param termId: string (required), path.
        :param termBaseUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/terms/{termId}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def deleteConcept(
        self, conceptId: str, termBaseUid: str, phrase_token: Optional[str] = None
    ) -> None:
        """
        Delete concept

        :param conceptId: string (required), path.
        :param termBaseUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/concepts/{conceptId}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def listTermsOfConcept(
        self, conceptId: str, termBaseUid: str, phrase_token: Optional[str] = None
    ) -> ConceptDto:
        """
        Get terms of concept

        :param conceptId: string (required), path.
        :param termBaseUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ConceptDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/concepts/{conceptId}/terms"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ConceptDto(**r)

    async def getLastBackgroundTask(
        self, termBaseUid: str, phrase_token: Optional[str] = None
    ) -> BackgroundTasksTbDto:
        """
        Last import status

        :param termBaseUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: BackgroundTasksTbDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/lastBackgroundTask"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return BackgroundTasksTbDto(**r)

    async def browseTerms(
        self,
        termBaseUid: str,
        body: BrowseRequestDto,
        phrase_token: Optional[str] = None,
    ) -> BrowseResponseListDto:
        """
        Browse term base

        :param termBaseUid: string (required), path.
        :param body: BrowseRequestDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: BrowseResponseListDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/browse"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return BrowseResponseListDto(**r)

    async def searchTerms(
        self,
        termBaseUid: str,
        body: TermBaseSearchRequestDto,
        phrase_token: Optional[str] = None,
    ) -> SearchResponseListTbDto:
        """
        Search term base

        :param termBaseUid: string (required), path.
        :param body: TermBaseSearchRequestDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: SearchResponseListTbDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/search"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return SearchResponseListTbDto(**r)

    async def exportTermBase(
        self,
        termBaseUid: str,
        termStatus: str = None,
        format: str = "Tbx",
        charset: str = "UTF-8",
        phrase_token: Optional[str] = None,
    ) -> bytes:
        """
        Export term base

        :param termBaseUid: string (required), path.
        :param termStatus: string (optional), query.
        :param format: string (optional), query.
        :param charset: string (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/export"
        params = {"format": format, "charset": charset, "termStatus": termStatus}

        files = None
        payload = None

        r = await self.client.get_bytestream(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return r

    async def getTermBaseMetadata(
        self, termBaseUid: str, phrase_token: Optional[str] = None
    ) -> MetadataTbDto:
        """
        Get term base metadata

        :param termBaseUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: MetadataTbDto
        """
        endpoint = f"/api2/v1/termBases/{termBaseUid}/metadata"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return MetadataTbDto(**r)

    async def searchTermsByJob_1(
        self,
        projectUid: str,
        jobUid: str,
        body: SearchTbByJobRequestDto,
        phrase_token: Optional[str] = None,
    ) -> SearchTbResponseListDto:
        """
        Search job's term bases
        Search all read term bases assigned to the job
        :param projectUid: string (required), path.
        :param jobUid: string (required), path.
        :param body: SearchTbByJobRequestDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: SearchTbResponseListDto
        """
        endpoint = f"/api2/v2/projects/{projectUid}/jobs/{jobUid}/termBases/searchByJob"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return SearchTbResponseListDto(**r)

    async def searchTermsInTextByJobV2(
        self,
        projectUid: str,
        jobUid: str,
        body: SearchTbInTextByJobRequestDto,
        phrase_token: Optional[str] = None,
    ) -> SearchInTextResponseList2Dto:
        """
        Search terms in text
        Search in text in all read term bases assigned to the job
        :param projectUid: string (required), path.
        :param jobUid: string (required), path.
        :param body: SearchTbInTextByJobRequestDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: SearchInTextResponseList2Dto
        """
        endpoint = (
            f"/api2/v2/projects/{projectUid}/jobs/{jobUid}/termBases/searchInTextByJob"
        )
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return SearchInTextResponseList2Dto(**r)
