from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    CreateLqaProfileDto,
    LqaProfileDetailDto,
    LqaProfileReferenceDto,
    PageDtoLqaProfileReferenceDto,
    QualityAssuranceBatchRunDtoV3,
    QualityAssuranceChecksDtoV2,
    QualityAssuranceResponseDto,
    QualityAssuranceRunDtoV3,
    QualityAssuranceSegmentsRunDtoV3,
    UpdateIgnoredChecksDto,
    UpdateIgnoredWarningsDto,
    UpdateLqaProfileDto,
)


class QualityAssuranceOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def makeDefault(
        self,
        profileUid: str,
        phrase_token: Optional[str] = None,
    ) -> LqaProfileReferenceDto:
        """
        Make LQA profile default

        :param profileUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: LqaProfileReferenceDto
        """
        endpoint = f"/api2/v1/lqa/profiles/{profileUid}/default"
        params = {}

        files = None
        payload = None

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return LqaProfileReferenceDto(**r)

    def getLqaProfile(
        self,
        profileUid: str,
        phrase_token: Optional[str] = None,
    ) -> LqaProfileDetailDto:
        """
        Get LQA profile details

        :param profileUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: LqaProfileDetailDto
        """
        endpoint = f"/api2/v1/lqa/profiles/{profileUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return LqaProfileDetailDto(**r)

    def updateLqaProfile(
        self,
        profileUid: str,
        body: UpdateLqaProfileDto,
        phrase_token: Optional[str] = None,
    ) -> LqaProfileDetailDto:
        """
        Update LQA profile

        :param profileUid: string (required), path.
        :param body: UpdateLqaProfileDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: LqaProfileDetailDto
        """
        endpoint = f"/api2/v1/lqa/profiles/{profileUid}"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return LqaProfileDetailDto(**r)

    def deleteLqaProfile(
        self,
        profileUid: str,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete LQA profile

        :param profileUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/lqa/profiles/{profileUid}"
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def getLqaProfiles(
        self,
        order: List[str] = None,
        sort: List[str] = None,
        dateCreated: str = None,
        createdBy: str = None,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "20",
        phrase_token: Optional[str] = None,
    ) -> PageDtoLqaProfileReferenceDto:
        """
        GET list LQA profiles

        :param order: array (optional), query.
        :param sort: array (optional), query.
        :param dateCreated: string (optional), query. It is used for filter the list by date created.
        :param createdBy: string (optional), query. It is used for filter the list by who created the profile.
        :param name: string (optional), query. Name of LQA profiles, it is used for filter the list by name.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 20.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoLqaProfileReferenceDto
        """
        endpoint = f"/api2/v1/lqa/profiles"
        params = {
            "name": name,
            "createdBy": createdBy,
            "dateCreated": dateCreated,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "sort": sort,
            "order": order,
        }

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoLqaProfileReferenceDto(**r)

    def createLqaProfile(
        self,
        body: CreateLqaProfileDto,
        phrase_token: Optional[str] = None,
    ) -> LqaProfileDetailDto:
        """
        Create LQA profile

        :param body: CreateLqaProfileDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: LqaProfileDetailDto
        """
        endpoint = f"/api2/v1/lqa/profiles"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return LqaProfileDetailDto(**r)

    def duplicateProfile(
        self,
        profileUid: str,
        phrase_token: Optional[str] = None,
    ) -> LqaProfileReferenceDto:
        """
        Duplicate LQA profile

        :param profileUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: LqaProfileReferenceDto
        """
        endpoint = f"/api2/v1/lqa/profiles/{profileUid}/duplicate"
        params = {}

        files = None
        payload = None

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return LqaProfileReferenceDto(**r)

    def getLqaProfileAuthors(
        self,
        phrase_token: Optional[str] = None,
    ) -> Any:
        """
        Get list of LQA profile authors


        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return:
        """
        endpoint = f"/api2/v1/lqa/profiles/authors"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return r

    def updateIgnoredChecks(
        self,
        jobUid: str,
        projectUid: str,
        body: UpdateIgnoredChecksDto,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Edit ignored checks

        :param jobUid: string (required), path.
        :param projectUid: string (required), path.
        :param body: UpdateIgnoredChecksDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/qualityAssurances/ignoreChecks"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def addIgnoredWarnings(
        self,
        jobUid: str,
        projectUid: str,
        body: UpdateIgnoredWarningsDto,
        phrase_token: Optional[str] = None,
    ) -> UpdateIgnoredWarningsDto:
        """
        Add ignored warnings

        :param jobUid: string (required), path.
        :param projectUid: string (required), path.
        :param body: UpdateIgnoredWarningsDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: UpdateIgnoredWarningsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/qualityAssurances/ignoredWarnings"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return UpdateIgnoredWarningsDto(**r)

    def deleteIgnoredWarnings(
        self,
        jobUid: str,
        projectUid: str,
        body: UpdateIgnoredWarningsDto,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete ignored warnings

        :param jobUid: string (required), path.
        :param projectUid: string (required), path.
        :param body: UpdateIgnoredWarningsDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/qualityAssurances/ignoredWarnings"
        params = {}

        files = None
        payload = body

        r = self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def enabledQualityChecksForJob(
        self,
        jobUid: str,
        projectUid: str,
        phrase_token: Optional[str] = None,
    ) -> QualityAssuranceChecksDtoV2:
        """
        Get QA settings for job
        Returns enabled quality assurance checks and settings for job.
        :param jobUid: string (required), path.
        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: QualityAssuranceChecksDtoV2
        """
        endpoint = (
            f"/api2/v2/projects/{projectUid}/jobs/{jobUid}/qualityAssurances/settings"
        )
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return QualityAssuranceChecksDtoV2(**r)

    def enabledQualityChecksForJob_1(
        self,
        projectUid: str,
        phrase_token: Optional[str] = None,
    ) -> QualityAssuranceChecksDtoV2:
        """
        Get QA settings
        Returns enabled quality assurance checks and settings.
        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: QualityAssuranceChecksDtoV2
        """
        endpoint = f"/api2/v2/projects/{projectUid}/jobs/qualityAssurances/settings"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return QualityAssuranceChecksDtoV2(**r)

    def runQaForJobPartV3(
        self,
        jobUid: str,
        projectUid: str,
        body: QualityAssuranceRunDtoV3,
        phrase_token: Optional[str] = None,
    ) -> QualityAssuranceResponseDto:
        """
        Run quality assurance
        Call "Get QA settings" endpoint to get the list of enabled QA checks
        :param jobUid: string (required), path.
        :param projectUid: string (required), path.
        :param body: QualityAssuranceRunDtoV3 (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: QualityAssuranceResponseDto
        """
        endpoint = f"/api2/v3/projects/{projectUid}/jobs/{jobUid}/qualityAssurances/run"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return QualityAssuranceResponseDto(**r)

    def runQaForJobPartsV3(
        self,
        projectUid: str,
        body: QualityAssuranceBatchRunDtoV3,
        phrase_token: Optional[str] = None,
    ) -> QualityAssuranceResponseDto:
        """
        Run quality assurance (batch)
        Call "Get QA settings" endpoint to get the list of enabled QA checks
        :param projectUid: string (required), path.
        :param body: QualityAssuranceBatchRunDtoV3 (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: QualityAssuranceResponseDto
        """
        endpoint = f"/api2/v3/projects/{projectUid}/jobs/qualityAssurances/run"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return QualityAssuranceResponseDto(**r)

    def runQaForSegmentsV3(
        self,
        projectUid: str,
        body: QualityAssuranceSegmentsRunDtoV3,
        phrase_token: Optional[str] = None,
    ) -> QualityAssuranceResponseDto:
        """
        Run quality assurance on selected segments
        By default runs only fast running checks. Source and target language of jobs have to match.
        :param projectUid: string (required), path.
        :param body: QualityAssuranceSegmentsRunDtoV3 (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: QualityAssuranceResponseDto
        """
        endpoint = f"/api2/v3/projects/{projectUid}/jobs/qualityAssurances/segments/run"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return QualityAssuranceResponseDto(**r)
