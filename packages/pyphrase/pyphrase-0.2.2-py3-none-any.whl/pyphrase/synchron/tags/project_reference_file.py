from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    CreateReferenceFileNoteDto,
    ProjectReferenceFilesRequestDto,
    ReferenceFilePageDto,
    ReferenceFileReference,
)


class ProjectReferenceFileOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def listReferenceFiles(
        self,
        projectUid: str,
        createdBy: str = None,
        dateCreatedSince: str = None,
        filename: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        sort: str = "DATE_CREATED",
        order: str = "DESC",
        phrase_token: Optional[str] = None,
    ) -> ReferenceFilePageDto:
        """
        List project reference files

        :param projectUid: string (required), path.
        :param createdBy: string (optional), query. UID of user.
        :param dateCreatedSince: string (optional), query. date time in ISO 8601 UTC format.
        :param filename: string (optional), query.
        :param pageNumber: integer (optional), query.
        :param pageSize: integer (optional), query.
        :param sort: string (optional), query.
        :param order: string (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ReferenceFilePageDto
        """
        endpoint = f"/api2/v1/projects/{projectUid}/references"
        params = {
            "filename": filename,
            "dateCreatedSince": dateCreatedSince,
            "createdBy": createdBy,
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

        return ReferenceFilePageDto(**r)

    def createNoteRef(
        self,
        projectUid: str,
        body: CreateReferenceFileNoteDto,
        phrase_token: Optional[str] = None,
    ) -> ReferenceFileReference:
        """
        Create project reference file
        Accepts `application/octet-stream` or `application/json`.<br>
                       - `application/json` - `note` field will be converted to .txt.<br>
                       - `application/octet-stream` - `Content-Disposition` header is required
        :param projectUid: string (required), path.
        :param body: CreateReferenceFileNoteDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ReferenceFileReference
        """
        endpoint = f"/api2/v1/projects/{projectUid}/references"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ReferenceFileReference(**r)

    def batchDeleteReferenceFiles(
        self,
        projectUid: str,
        body: ProjectReferenceFilesRequestDto,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete project reference files (batch)

        :param projectUid: string (required), path.
        :param body: ProjectReferenceFilesRequestDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/references"
        params = {}

        files = None
        payload = body

        r = self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def downloadReference(
        self, referenceFileId: str, projectUid: str, phrase_token: Optional[str] = None
    ) -> bytes:
        """
        Download project reference file

        :param referenceFileId: string (required), path.
        :param projectUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/references/{referenceFileId}"
        params = {}

        files = None
        payload = None

        r = self.client.get_bytestream(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return r

    def batchDownloadReferenceFiles(
        self,
        projectUid: str,
        body: ProjectReferenceFilesRequestDto,
        phrase_token: Optional[str] = None,
    ) -> bytes:
        """
        Download project reference files (batch)

        :param projectUid: string (required), path.
        :param body: ProjectReferenceFilesRequestDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/projects/{projectUid}/references/download"
        params = {}

        files = None
        payload = body

        r = self.client.post_bytestream(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return r
