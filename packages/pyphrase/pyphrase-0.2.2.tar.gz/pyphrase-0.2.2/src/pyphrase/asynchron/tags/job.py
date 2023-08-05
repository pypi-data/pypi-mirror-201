from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    ComparedSegmentsDto,
    CreateWebEditorLinkDtoV2,
    FileHandoverDto,
    FileImportSettingsCreateDto,
    FileImportSettingsDto,
    GetBilingualFileDto,
    InputStream,
    JobCreateRequestDto,
    JobExportActionDto,
    JobExportResponseDto,
    JobListDto,
    JobPartDeleteReferences,
    JobPartExtendedDto,
    JobPartPatchBatchDto,
    JobPartPatchResultDto,
    JobPartPatchSingleDto,
    JobPartReadyDeleteTranslationDto,
    JobPartReadyReferences,
    JobPartReferences,
    JobPartsDto,
    JobPartStatusChangesDto,
    JobPartUpdateBatchDto,
    JobPartUpdateSingleDto,
    JobStatusChangeActionDto,
    JobUpdateSourceResponseDto,
    NotifyJobPartsRequestDto,
    PageDtoJobPartReferenceV2,
    PreviewUrlsDto,
    ProjectWorkflowStepDto,
    PseudoTranslateActionDto,
    PseudoTranslateWrapperDto,
    SearchJobsDto,
    SearchJobsRequestDto,
    SearchResponseListTmDtoV3,
    SearchTMByJobRequestDtoV3,
    SegmentListDto,
    SegmentsCountsResponseListDto,
    SplitJobActionDto,
    TargetFileWarningsDto,
    TranslationResourcesDto,
    WebEditorLinkDtoV2,
    WildCardSearchByJobRequestDtoV3,
)


class JobOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def getHandoverFiles(
        self,
        projectUid: str,
        jobUid: List[str] = None,
        phrase_token: Optional[str] = None,
    ) -> bytes:
        """
                Download handover file(s)
                For downloading multiple files as ZIP file provide multiple IDs in query parameters.
        * For example `?jobUid={id1}&jobUid={id2}`
        * When no files matched given IDs error 404 is returned, otherwise ZIP file will include those that were found
                :param projectUid: string (required), path.
                :param jobUid: array (optional), query. JobPart Id of requested handover file.

                :param phrase_token: string (optional) - if not supplied, client will look token from init

                :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/fileHandovers"
        params = {"jobUid": jobUid}

        files = None
        payload = None

        r = await self.client.get_bytestream(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return r

    async def uploadHandoverFile(
        self, projectUid: str, body: InputStream, phrase_token: Optional[str] = None
    ) -> FileHandoverDto:
        """
                Upload handover file
                For following jobs the handover file is not supported:
        * Continuous jobs
        * Jobs from connectors
        * Split jobs
        * Multilingual jobs
                :param projectUid: string (required), path.
                :param body: InputStream (required), body.

                :param phrase_token: string (optional) - if not supplied, client will look token from init

                :return: FileHandoverDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/fileHandovers"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return FileHandoverDto(**r)

    async def deleteHandoverFile(
        self,
        projectUid: str,
        body: JobPartReferences,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete handover file

        :param projectUid: string (required), path.
        :param body: JobPartReferences (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/fileHandovers"
        params = {}

        files = None
        payload = body

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def split(
        self,
        jobUid: str,
        projectUid: str,
        body: SplitJobActionDto,
        phrase_token: Optional[str] = None,
    ) -> JobPartsDto:
        """
                Split job
                Splits job by one of the following methods:
        * **After specific segments** - fill in `segmentOrdinals`
        * **Into X parts** - fill in `partCount`
        * **Into parts with specific size** - fill in `partSize`. partSize represents segment count in each part.
        * **Into parts with specific word count** - fill in `wordCount`
        * **By document parts** - fill in `byDocumentParts`, works only with **PowerPoint** files

        Only one option at a time is allowed.
                :param jobUid: string (required), path.
                :param projectUid: string (required), path.
                :param body: SplitJobActionDto (required), body.

                :param phrase_token: string (optional) - if not supplied, client will look token from init

                :return: JobPartsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/split"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return JobPartsDto(**r)

    async def setStatus(
        self,
        jobUid: str,
        projectUid: str,
        body: JobStatusChangeActionDto,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Edit job status

        :param jobUid: string (required), path.
        :param projectUid: string (required), path.
        :param body: JobStatusChangeActionDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/setStatus"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def getPart(
        self, jobUid: str, projectUid: str, phrase_token: Optional[str] = None
    ) -> JobPartExtendedDto:
        """
        Get job

        :param jobUid: string (required), path.
        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: JobPartExtendedDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return JobPartExtendedDto(**r)

    async def editPart(
        self,
        jobUid: str,
        projectUid: str,
        body: JobPartUpdateSingleDto,
        phrase_token: Optional[str] = None,
    ) -> JobPartExtendedDto:
        """
        Edit job

        :param jobUid: string (required), path.
        :param projectUid: string (required), path.
        :param body: JobPartUpdateSingleDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: JobPartExtendedDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return JobPartExtendedDto(**r)

    async def patchPart(
        self,
        jobUid: str,
        projectUid: str,
        body: JobPartPatchSingleDto,
        phrase_token: Optional[str] = None,
    ) -> JobPartExtendedDto:
        """
        Patch job

        :param jobUid: string (required), path.
        :param projectUid: string (required), path.
        :param body: JobPartPatchSingleDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: JobPartExtendedDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.patch(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return JobPartExtendedDto(**r)

    async def getImportSettings_3(
        self, jobUid: str, projectUid: str, phrase_token: Optional[str] = None
    ) -> FileImportSettingsDto:
        """
        Get import settings for job

        :param jobUid: string (required), path.
        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: FileImportSettingsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/importSettings"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return FileImportSettingsDto(**r)

    async def editJobImportSettings(
        self,
        jobUid: str,
        projectUid: str,
        body: FileImportSettingsCreateDto,
        phrase_token: Optional[str] = None,
    ) -> FileImportSettingsDto:
        """
        Edit job import settings

        :param jobUid: string (required), path.
        :param projectUid: string (required), path.
        :param body: FileImportSettingsCreateDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: FileImportSettingsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/importSettings"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return FileImportSettingsDto(**r)

    async def pseudoTranslateJobPart(
        self,
        jobUid: str,
        projectUid: str,
        body: PseudoTranslateActionDto,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Pseudo-translates job

        :param jobUid: string (required), path.
        :param projectUid: string (required), path.
        :param body: PseudoTranslateActionDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/pseudoTranslate"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def deleteAllTranslations(
        self,
        projectUid: str,
        body: JobPartReadyReferences,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete all translations

        :param projectUid: string (required), path.
        :param body: JobPartReadyReferences (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/translations"
        params = {}

        files = None
        payload = body

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def statusChanges(
        self, jobUid: str, projectUid: str, phrase_token: Optional[str] = None
    ) -> JobPartStatusChangesDto:
        """
        Get status changes

        :param jobUid: string (required), path.
        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: JobPartStatusChangesDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/statusChanges"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return JobPartStatusChangesDto(**r)

    async def copySourceToTarget(
        self,
        projectUid: str,
        body: JobPartReadyReferences,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Copy Source to Target

        :param projectUid: string (required), path.
        :param body: JobPartReadyReferences (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/copySourceToTarget"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def copySourceToTargetJobPart(
        self, jobUid: str, projectUid: str, phrase_token: Optional[str] = None
    ) -> None:
        """
        Copy Source to Target job

        :param jobUid: string (required), path.
        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/copySourceToTarget"
        params = {}

        files = None
        payload = None

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def getTranslationResources(
        self, jobUid: str, projectUid: str, phrase_token: Optional[str] = None
    ) -> TranslationResourcesDto:
        """
        Get translation resources

        :param jobUid: string (required), path.
        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: TranslationResourcesDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/translationResources"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return TranslationResourcesDto(**r)

    async def listSegments(
        self,
        jobUid: str,
        projectUid: str,
        beginIndex: int = "0",
        endIndex: int = "0",
        phrase_token: Optional[str] = None,
    ) -> SegmentListDto:
        """
        Get segments

        :param jobUid: string (required), path.
        :param projectUid: string (required), path.
        :param beginIndex: integer (optional), query.
        :param endIndex: integer (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: SegmentListDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/segments"
        params = {"beginIndex": beginIndex, "endIndex": endIndex}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return SegmentListDto(**r)

    async def getOriginalFile(
        self, jobUid: str, projectUid: str, phrase_token: Optional[str] = None
    ) -> bytes:
        """
        Download original file

        :param jobUid: string (required), path.
        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/original"
        params = {}

        files = None
        payload = None

        r = await self.client.get_bytestream(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return r

    async def filePreviewJob(
        self, jobUid: str, projectUid: str, phrase_token: Optional[str] = None
    ) -> bytes:
        """
        Download preview file

        :param jobUid: string (required), path.
        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/preview"
        params = {}

        files = None
        payload = None

        r = await self.client.get_bytestream(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return r

    async def filePreview(
        self,
        jobUid: str,
        projectUid: str,
        body: InputStream,
        phrase_token: Optional[str] = None,
    ) -> bytes:
        """
        Download preview file
        Takes bilingual file (.mxliff only) as argument. If not passed, data will be taken from database
        :param jobUid: string (required), path.
        :param projectUid: string (required), path.
        :param body: InputStream (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/preview"
        params = {}

        files = None
        payload = body

        r = await self.client.post_bytestream(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return r

    async def getCompletedFileWarnings(
        self, jobUid: str, projectUid: str, phrase_token: Optional[str] = None
    ) -> TargetFileWarningsDto:
        """
        Get target file's warnings
        This call will return target file's warnings. This means even for other jobs that were created via 'split jobs' etc.
        :param jobUid: string (required), path.
        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: TargetFileWarningsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/targetFileWarnings"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return TargetFileWarningsDto(**r)

    async def previewUrls(
        self,
        jobUid: str,
        projectUid: str,
        workflowLevel: int = "1",
        phrase_token: Optional[str] = None,
    ) -> PreviewUrlsDto:
        """
        Get PDF preview

        :param jobUid: string (required), path.
        :param projectUid: string (required), path.
        :param workflowLevel: integer (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PreviewUrlsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/previewUrl"
        params = {"workflowLevel": workflowLevel}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PreviewUrlsDto(**r)

    async def createJob(
        self,
        projectUid: str,
        body: bytes,
        fileName: str,
        metadata: JobCreateRequestDto,
        phrase_token: Optional[str] = None,
    ) -> JobListDto:
        """
                Create job
                Job file can be provided directly in the message body or downloaded from connector.

        Please supply job metadata in `Memsource` header.

        For file in the request body provide also the filename in `Content-Disposition` header.

        Accepted metadata:

          - `targetLangs` - **required**
          - `due` - ISO 8601
          - `workflowSettings` - project with workflow - see examples bellow
          - `assignments` - project without workflows - see examples bellow
          - `importSettings` - re-usable import settings - see [Create import settings](#operation/createImportSettings)
          - `useProjectFileImportSettings` - mutually exclusive with importSettings
          - `callbackUrl` - consumer callback
          - `path` - original destination directory
          - `preTranslate` - set pre translate job after import

          for remote file jobs also `remoteFile` - see examples bellow:
          - `connectorToken` - remote connector token
          - `remoteFolder`
          - `remoteFileName`
          - `continuous` - true for continuous job

        Create and assign job in project without workflow step:
        ```

        {
          "targetLangs": [
            "cs_cz"
          ],
          "callbackUrl": "https://my-shiny-service.com/consumeCallback",
          "importSettings": {
            "uid": "abcd123"
          },
          "due": "2007-12-03T10:15:30.00Z",
          "path": "destination directory",
          "assignments": [
            {
              "targetLang": "cs_cz",
              "providers": [
                {
                  "id": "4321",
                  "type": "USER"
                }
              ]
            }
          ],
          "notifyProvider": {
            "organizationEmailTemplate": {
              "id": "39"
            },
            "notificationIntervalInMinutes": "10"
          }
        }
        ```

        Create job from remote file without workflow steps:
        ```

        {
          "remoteFile": {
            "connectorToken": "948123ef-e1ef-4cd3-a90e-af1617848af3",
            "remoteFolder": "/",
            "remoteFileName": "Few words.docx",
            "continuous": false
          },
          "assignments": [],
          "workflowSettings": [],
          "targetLangs": [
            "cs"
          ]
        }
        ```

        Create and assign job in project with workflow step:
        ```

        {
          "targetLangs": [
            "de"
          ],
          "useProjectFileImportSettings": "true",
          "workflowSettings": [
            {
              "id": "64",
              "due": "2007-12-03T10:15:30.00Z",
              "assignments": [
                {
                  "targetLang": "de",
                  "providers": [
                    {
                      "id": "3",
                      "type": "VENDOR"
                    }
                  ]
                }
              ],
              "notifyProvider": {
                "organizationEmailTemplate": {
                  "id": "39"
                },
                "notificationIntervalInMinutes": "10"
              }
            }
          ]
        }
        ```
                :param projectUid: string (required), path.
                :param body: InputStream (required), body.

                :param phrase_token: string (optional) - if not supplied, client will look token from init

                :return: JobListDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs"
        params = {}
        headers = {
            "Memsource": metadata.json(exclude_none=True),
            "Content-disposition": f"filename*=UTF-8''{fileName}",
        }
        payload = None
        content = body

        files = None

        r = await self.client.post(
            endpoint,
            phrase_token,
            params=params,
            payload=payload,
            content=content,
            files=files,
            headers=headers,
        )

        return JobListDto(**r)

    async def createJobFromAsyncDownloadTask(
        self,
        projectUid: str,
        body: JobCreateRequestDto,
        downloadTaskId: str = None,
        continuous: bool = "False",
        phrase_token: Optional[str] = None,
    ) -> JobListDto:
        """
                Create job from connector asynchronous download task
                Creates the job in project specified by path param projectUid. Source file is defined by downloadTaskId parameter. That is value of finished download async task
        [Connector - Download file (async)](#operation/getFile_1).

        Please supply job metadata in body.

        Accepted metadata:

          - `targetLangs` - **required**
          - `due` - ISO 8601
          - `workflowSettings` - project with workflow - see examples bellow
          - `assignments` - project without workflows - see examples bellow
          - `importSettings` - re-usable import settings - see [Create import settings](#operation/createImportSettings)
          - `useProjectFileImportSettings` - mutually exclusive with importSettings
          - `callbackUrl` - consumer callback
          - `path` - original destination directory
          - `preTranslate` - set pre translate job after import

        Create job simple (without workflow steps, without assignments):
        ```
        {
          "targetLangs": [
            "cs_cz",
            "es_es"
          ]
        }
        ```

        Create and assign job in project without workflow step:
        ```
        {
          "targetLangs": [
            "cs_cz"
          ],
          "callbackUrl": "https://my-shiny-service.com/consumeCallback",
          "importSettings": {
            "uid": "abcd123"
          },
          "due": "2007-12-03T10:15:30.00Z",
          "path": "destination directory",
          "assignments": [
            {
              "targetLang": "cs_cz",
              "providers": [
                {
                  "id": "4321",
                  "type": "USER"
                }
              ]
            }
          ],
          "notifyProvider": {
            "organizationEmailTemplate": {
              "id": "39"
            },
            "notificationIntervalInMinutes": "10"
          }
        }
        ```

        Create and assign job in project with workflow step:
        ```
        {
          "targetLangs": [
            "de"
          ],
          "useProjectFileImportSettings": "true",
          "workflowSettings": [
            {
              "id": "64",
              "due": "2007-12-03T10:15:30.00Z",
              "assignments": [
                {
                  "targetLang": "de",
                  "providers": [
                    {
                      "id": "3",
                      "type": "VENDOR"
                    }
                  ]
                }
              ],
              "notifyProvider": {
                "organizationEmailTemplate": {
                  "id": "39"
                },
                "notificationIntervalInMinutes": "10"
              }
            }
          ]
        }
        ```
                :param projectUid: string (required), path.
                :param body: JobCreateRequestDto (required), body.
                :param downloadTaskId: string (optional), query.
                :param continuous: boolean (optional), query.

                :param phrase_token: string (optional) - if not supplied, client will look token from init

                :return: JobListDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/connectorTask"
        params = {"downloadTaskId": downloadTaskId, "continuous": continuous}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return JobListDto(**r)

    async def updateSource(
        self, projectUid: str, body: InputStream, phrase_token: Optional[str] = None
    ) -> JobUpdateSourceResponseDto:
        """
                Update source
                API updated source file for specified job

        Job file can be provided directly in the message body.

        Please supply jobs in `Memsource` header.

        For file in the request body provide also the filename in `Content-Disposition` header.

        If a job from a multilingual file is updated, all jobs from the same file are update too even if their UIDs aren't
        listed in the jobs field.

        Accepted metadata:

          - `jobs` - **required** - list of jobs UID reference (maximum size `100`)
          - `preTranslate` - pre translate flag (default `false`)
          - `allowAutomaticPostAnalysis` - if automatic post editing analysis should be created. If not specified then value
                                           is taken from the analyse settings of the project
          - `callbackUrl` - consumer callback

        Job restrictions:
          - job must belong to project specified in path (`projectUid`)
          - job `UID` must be from the first workflow step
          - job cannot be split
          - job cannot be continuous
          - job cannot originate in a connector
          - status in any of the job's workflow steps cannot be a final
            status (`COMPLETED_BY_LINGUIST`, `COMPLETED`, `CANCELLED`)
          - job UIDs must be from the same multilingual file if a multilingual file is updated
          - multiple multilingual files or a mixture of multilingual and other jobs cannot be updated in one call

        File restrictions:
          - file cannot be a `.zip` file

        Example:

        ```
        {
          "jobs": [
            {
                "uid": "jobIn1stWfStepAndNonFinalStatusUid"
            }
          ],
          "preTranslate": false,
          "allowAutomaticPostAnalysis": false
          "callbackUrl": "https://my-shiny-service.com/consumeCallback"
        }
        ```
                :param projectUid: string (required), path.
                :param body: InputStream (required), body.

                :param phrase_token: string (optional) - if not supplied, client will look token from init

                :return: JobUpdateSourceResponseDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/source"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return JobUpdateSourceResponseDto(**r)

    async def updateTarget(
        self, projectUid: str, body: InputStream, phrase_token: Optional[str] = None
    ) -> JobUpdateSourceResponseDto:
        """
                Update target
                API update target file for specified job

        Job file can be provided directly in the message body.

        Please supply jobs in `Memsource` header.

        For file in the request body provide also the filename in `Content-Disposition` header.

        Accepted metadata:

          - `jobs` - **required** - list of jobs UID reference (maximum size `1`)
          - `propagateConfirmedToTm` - sets if confirmed segments should be stored in TM (default value: true)
          - `callbackUrl` - consumer callback
          - `targetSegmentationRule` - ID reference to segmentation rule of organization to use for update target
          - `unconfirmChangedSegments` - sets if segments should stay unconfirmed

        Job restrictions:
          - job must belong to project specified in path (`projectUid`)
          - job cannot be split
          - job cannot be continuous
          - job cannot be multilingual
          - job cannot originate in a connector
          - job cannot have different file extension than original file

        File restrictions:
          - file cannot be a `.zip` file
          - update target is not allowed for jobs with file extensions: xliff, po, tbx, tmx, ttx, ts

        Example:

        ```
        {
          "jobs": [
            {
                "uid": "jobUid"
            }
          ],
          "propagateConfirmedToTm": true,
          "targetSegmentationRule": {
                "id": "1"
           },
          "callbackUrl": "https://my-shiny-service.com/consumeCallback"
        }
        ```
                :param projectUid: string (required), path.
                :param body: InputStream (required), body.

                :param phrase_token: string (optional) - if not supplied, client will look token from init

                :return: JobUpdateSourceResponseDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/target"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return JobUpdateSourceResponseDto(**r)

    async def editParts(
        self,
        projectUid: str,
        body: JobPartUpdateBatchDto,
        phrase_token: Optional[str] = None,
    ) -> JobPartsDto:
        """
        Edit jobs (batch)
        Returns only jobs which were updated by the batch operation.
        :param projectUid: string (required), path.
        :param body: JobPartUpdateBatchDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: JobPartsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/batch"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return JobPartsDto(**r)

    async def deleteParts(
        self,
        projectUid: str,
        body: JobPartDeleteReferences,
        purge: bool = "False",
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete job (batch)

        :param projectUid: string (required), path.
        :param body: JobPartDeleteReferences (required), body.
        :param purge: boolean (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/batch"
        params = {"purge": purge}

        files = None
        payload = body

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def notifyAssigned(
        self,
        projectUid: str,
        body: NotifyJobPartsRequestDto,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Notify assigned users

        :param projectUid: string (required), path.
        :param body: NotifyJobPartsRequestDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/notifyAssigned"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def comparePart(
        self,
        projectUid: str,
        body: JobPartReadyReferences,
        atWorkflowLevel: int = "1",
        withWorkflowLevel: int = "1",
        phrase_token: Optional[str] = None,
    ) -> ComparedSegmentsDto:
        """
        Compare jobs on workflow levels

        :param projectUid: string (required), path.
        :param body: JobPartReadyReferences (required), body.
        :param atWorkflowLevel: integer (optional), query.
        :param withWorkflowLevel: integer (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ComparedSegmentsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/compare"
        params = {
            "atWorkflowLevel": atWorkflowLevel,
            "withWorkflowLevel": withWorkflowLevel,
        }

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ComparedSegmentsDto(**r)

    async def getBilingualFile(
        self,
        projectUid: str,
        body: GetBilingualFileDto,
        format: str = "MXLF",
        preview: bool = "True",
        phrase_token: Optional[str] = None,
    ) -> bytes:
        """
        Download bilingual file

        :param projectUid: string (required), path.
        :param body: GetBilingualFileDto (required), body.
        :param format: string (optional), query.
        :param preview: boolean (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/bilingualFile"
        params = {"format": format, "preview": preview}

        files = None
        payload = body

        r = await self.client.post_bytestream(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return r

    async def getPartsWorkflowStep(
        self, jobUid: str, projectUid: str, phrase_token: Optional[str] = None
    ) -> ProjectWorkflowStepDto:
        """
        Get job's workflowStep

        :param jobUid: string (required), path.
        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ProjectWorkflowStepDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/{jobUid}/workflowStep"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ProjectWorkflowStepDto(**r)

    async def searchPartsInProject(
        self,
        projectUid: str,
        body: SearchJobsRequestDto,
        phrase_token: Optional[str] = None,
    ) -> SearchJobsDto:
        """
        Search jobs in project

        :param projectUid: string (required), path.
        :param body: SearchJobsRequestDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: SearchJobsDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/search"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return SearchJobsDto(**r)

    async def getSegmentsCount(
        self,
        projectUid: str,
        body: JobPartReadyReferences,
        phrase_token: Optional[str] = None,
    ) -> SegmentsCountsResponseListDto:
        """
        Get segments count
        Provides segments count (progress data)
        :param projectUid: string (required), path.
        :param body: JobPartReadyReferences (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: SegmentsCountsResponseListDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/jobs/segmentsCount"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return SegmentsCountsResponseListDto(**r)

    async def pseudoTranslate_1(
        self,
        projectUid: str,
        body: PseudoTranslateWrapperDto,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Pseudo-translate job

        :param projectUid: string (required), path.
        :param body: PseudoTranslateWrapperDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v2/projects/{projectUid}/jobs/pseudoTranslate"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def deleteAllTranslations_1(
        self,
        projectUid: str,
        body: JobPartReadyDeleteTranslationDto,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete specific translations

        :param projectUid: string (required), path.
        :param body: JobPartReadyDeleteTranslationDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v2/projects/{projectUid}/jobs/translations"
        params = {}

        files = None
        payload = body

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def completedFile_1(
        self, jobUid: str, projectUid: str, phrase_token: Optional[str] = None
    ) -> Any:
        """
            Download target file (async)
            This call will create async request for downloading target file with translation that can be downloaded when
        finished. This means even for other jobs that were created via 'split jobs' etc.
            :param jobUid: string (required), path.
            :param projectUid: string (required), path.

            :param phrase_token: string (optional) - if not supplied, client will look token from init

            :return:
        """
        endpoint = f"/api2/v2/projects/{projectUid}/jobs/{jobUid}/targetFile"
        params = {}

        files = None
        payload = None

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return r

    async def downloadCompletedFile(
        self,
        asyncRequestId: str,
        jobUid: str,
        projectUid: str,
        format: str = "ORIGINAL",
        phrase_token: Optional[str] = None,
    ) -> bytes:
        """
            Download target file based on async request
            This call will return target file with translation. This means even for other jobs that were created via
        'split jobs' etc.
            :param asyncRequestId: string (required), path.
            :param jobUid: string (required), path.
            :param projectUid: string (required), path.
            :param format: string (optional), query.

            :param phrase_token: string (optional) - if not supplied, client will look token from init

            :return: None
        """
        endpoint = f"/api2/v2/projects/{projectUid}/jobs/{jobUid}/downloadTargetFile/{asyncRequestId}"
        params = {"format": format}

        files = None
        payload = None

        r = await self.client.get_bytestream(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return r

    async def listPartsV2(
        self,
        projectUid: str,
        assignedVendor: int = None,
        targetLang: str = None,
        filename: str = None,
        dueInHours: int = None,
        assignedUser: int = None,
        status: List[str] = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        count: bool = "False",
        workflowLevel: int = "1",
        phrase_token: Optional[str] = None,
    ) -> PageDtoJobPartReferenceV2:
        """
        List jobs

        :param projectUid: string (required), path.
        :param assignedVendor: integer (optional), query.
        :param targetLang: string (optional), query.
        :param filename: string (optional), query.
        :param dueInHours: integer (optional), query.
        :param assignedUser: integer (optional), query.
        :param status: array (optional), query.
        :param pageNumber: integer (optional), query.
        :param pageSize: integer (optional), query.
        :param count: boolean (optional), query.
        :param workflowLevel: integer (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoJobPartReferenceV2
        """
        endpoint = f"/api2/v2/projects/{projectUid}/jobs"
        params = {
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "count": count,
            "workflowLevel": workflowLevel,
            "status": status,
            "assignedUser": assignedUser,
            "dueInHours": dueInHours,
            "filename": filename,
            "targetLang": targetLang,
            "assignedVendor": assignedVendor,
        }

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoJobPartReferenceV2(**r)

    async def webEditorLinkV2(
        self,
        projectUid: str,
        body: CreateWebEditorLinkDtoV2,
        phrase_token: Optional[str] = None,
    ) -> WebEditorLinkDtoV2:
        """
                Get Web Editor URL
                Possible warning codes are:
          - `NOT_ACCEPTED_BY_LINGUIST` - Job is not accepted by linguist
          - `NOT_ASSIGNED_TO_LINGUIST` - Job is not assigned to linguist
          - `PDF` - One of requested jobs is PDF
          - `PREVIOUS_WORKFLOW_NOT_COMPLETED` - Previous workflow step is not completed
          - `PREVIOUS_WORKFLOW_NOT_COMPLETED_STRICT` - Previous workflow step is not completed and project has strictWorkflowFinish set to true
          - `IN_DELIVERED_STATE` - Jobs in DELIVERED state
          - `IN_COMPLETED_STATE` - Jobs in COMPLETED state
          - `IN_REJECTED_STATE` - Jobs in REJECTED state

        Possible error codes are:
          - `ASSIGNED_TO_OTHER_USER` - Job is accepted by other user
          - `NOT_UNIQUE_TARGET_LANG` - Requested jobs contains different target locales
          - `TOO_MANY_SEGMENTS` - Count of requested job's segments is higher than **40000**
          - `TOO_MANY_JOBS` - Count of requested jobs is higher than **290**
          - `COMPLETED_JOINED_WITH_OTHER` - Jobs in COMPLETED state cannot be joined with jobs in other states
          - `DELIVERED_JOINED_WITH_OTHER` - Jobs in DELIVERED state cannot be joined with jobs in other states
          - `REJECTED_JOINED_WITH_OTHER` - Jobs in REJECTED state cannot be joined with jobs in other states

        Warning response example:
        ```
        {
            "warnings": [
                {
                    "message": "Not accepted by linguist",
                    "args": {
                        "jobs": [
                            "abcd1234"
                        ]
                    },
                    "code": "NOT_ACCEPTED_BY_LINGUIST"
                },
                {
                    "message": "Previous workflow step not completed",
                    "args": {
                        "jobs": [
                            "abcd1234"
                        ]
                    },
                    "code": "PREVIOUS_WORKFLOW_NOT_COMPLETED"
                }
            ],
            "url": "/web/job/abcd1234-efgh5678/translate"
        }
        ```

        Error response example:
        Status: `400 Bad Request`
        ```
        {
            "errorCode": "NOT_UNIQUE_TARGET_LANG",
            "errorDescription": "Only files with identical target languages can be joined",
            "errorDetails": [
                {
                    "code": "NOT_UNIQUE_TARGET_LANG",
                    "args": {
                        "targetLocales": [
                            "de",
                            "en"
                        ]
                    },
                    "message": "Only files with identical target languages can be joined"
                },
                {
                    "code": "TOO_MANY_SEGMENTS",
                    "args": {
                        "maxSegments": 40000,
                        "segments": 400009
                    },
                    "message": "Up to 40000 segments can be opened in the Memsource Web Editor, job has 400009 segments"
                }
            ]
        }
        ```
                :param projectUid: string (required), path.
                :param body: CreateWebEditorLinkDtoV2 (required), body.

                :param phrase_token: string (optional) - if not supplied, client will look token from init

                :return: WebEditorLinkDtoV2
        """
        endpoint = f"/api2/v2/projects/{projectUid}/jobs/webEditor"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return WebEditorLinkDtoV2(**r)

    async def patchUpdateJobParts(
        self, body: JobPartPatchBatchDto, phrase_token: Optional[str] = None
    ) -> JobPartPatchResultDto:
        """
        Edit jobs (with possible partial updates)
        Allows partial update, not breaking whole batch if single job fails and returns list of errors
        :param body: JobPartPatchBatchDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: JobPartPatchResultDto
        """
        endpoint = f"/api2/v3/jobs"
        params = {}

        files = None
        payload = body

        r = await self.client.patch(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return JobPartPatchResultDto(**r)

    async def searchByJob3(
        self,
        jobUid: str,
        projectUid: str,
        body: SearchTMByJobRequestDtoV3,
        phrase_token: Optional[str] = None,
    ) -> SearchResponseListTmDtoV3:
        """
        Search job's translation memories

        :param jobUid: string (required), path.
        :param projectUid: string (required), path.
        :param body: SearchTMByJobRequestDtoV3 (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: SearchResponseListTmDtoV3
        """
        endpoint = f"/api2/v3/projects/{projectUid}/jobs/{jobUid}/transMemories/search"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return SearchResponseListTmDtoV3(**r)

    async def wildCardSearchByJob3(
        self,
        jobUid: str,
        projectUid: str,
        body: WildCardSearchByJobRequestDtoV3,
        phrase_token: Optional[str] = None,
    ) -> SearchResponseListTmDtoV3:
        """
        Wildcard search job's translation memories

        :param jobUid: string (required), path.
        :param projectUid: string (required), path.
        :param body: WildCardSearchByJobRequestDtoV3 (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: SearchResponseListTmDtoV3
        """
        endpoint = (
            f"/api2/v3/projects/{projectUid}/jobs/{jobUid}/transMemories/wildCardSearch"
        )
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return SearchResponseListTmDtoV3(**r)

    async def exportToOnlineRepository(
        self,
        projectUid: str,
        body: JobExportActionDto,
        phrase_token: Optional[str] = None,
    ) -> JobExportResponseDto:
        """
        Export jobs to online repository

        :param projectUid: string (required), path.
        :param body: JobExportActionDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: JobExportResponseDto
        """
        endpoint = f"/api2/v3/projects/{projectUid}/jobs/export"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return JobExportResponseDto(**r)
