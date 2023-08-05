from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    AbstractConnectorDto,
    AsyncFileOpResponseDto,
    ConnectorCreateResponseDto,
    ConnectorDto,
    ConnectorListDto,
    FileListDto,
    GetFileRequestParamsDto,
    InputStreamLength,
    UploadResultDto,
)


class ConnectorOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def getFile(
        self,
        file: str,
        folder: str,
        connectorId: str,
        phrase_token: Optional[str] = None,
    ) -> bytes:
        """
        Download file
        Download a file from a subfolder of the selected connector
        :param file: string (required), path.
        :param folder: string (required), path.
        :param connectorId: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: InputStreamLength
        """
        endpoint = f"/api2/v1/connectors/{connectorId}/folders/{folder}/files/{file}"
        params = {}

        files = None
        payload = None

        r = self.client.get_bytestream(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return r

    def getConnector(
        self,
        connectorId: str,
        phrase_token: Optional[str] = None,
    ) -> ConnectorDto:
        """
        Get a connector

        :param connectorId: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ConnectorDto
        """
        endpoint = f"/api2/v1/connectors/{connectorId}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ConnectorDto(**r)

    def editConnector(
        self,
        connectorId: str,
        body: AbstractConnectorDto,
        connectionTest: bool = None,
        phrase_token: Optional[str] = None,
    ) -> ConnectorCreateResponseDto:
        """
        Edit connector
        Edit selected connector
        :param connectorId: string (required), path.
        :param body: AbstractConnectorDto (required), body.
        :param connectionTest: boolean (optional), query. For running connection test.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ConnectorCreateResponseDto
        """
        endpoint = f"/api2/v1/connectors/{connectorId}"
        params = {"connectionTest": connectionTest}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ConnectorCreateResponseDto(**r)

    def getConnectorList(
        self,
        type: str = None,
        phrase_token: Optional[str] = None,
    ) -> ConnectorListDto:
        """
        List connectors

        :param type: string (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ConnectorListDto
        """
        endpoint = f"/api2/v1/connectors"
        params = {"type": type}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ConnectorListDto(**r)

    def getFolder(
        self,
        folder: str,
        connectorId: str,
        projectUid: str = None,
        fileType: str = "ALL",
        sort: str = "NAME",
        direction: str = "ASCENDING",
        phrase_token: Optional[str] = None,
    ) -> FileListDto:
        """
        List files in a subfolder
        List files in a subfolder of the selected connector
        :param folder: string (required), path.
        :param connectorId: string (required), path.
        :param projectUid: string (optional), query.
        :param fileType: string (optional), query.
        :param sort: string (optional), query.
        :param direction: string (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: FileListDto
        """
        endpoint = f"/api2/v1/connectors/{connectorId}/folders/{folder}"
        params = {
            "projectUid": projectUid,
            "fileType": fileType,
            "sort": sort,
            "direction": direction,
        }

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return FileListDto(**r)

    def uploadFile(
        self,
        folder: str,
        connectorId: str,
        phrase_token: Optional[str] = None,
    ) -> UploadResultDto:
        """
        Upload a file to a subfolder of the selected connector
        Upload a file to a subfolder of the selected connector
        :param folder: string (required), path.
        :param connectorId: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: UploadResultDto
        """
        endpoint = f"/api2/v1/connectors/{connectorId}/folders/{folder}"
        params = {}

        files = None
        payload = None

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return UploadResultDto(**r)

    def getRootFolder(
        self,
        connectorId: str,
        fileType: str = "ALL",
        sort: str = "NAME",
        direction: str = "ASCENDING",
        phrase_token: Optional[str] = None,
    ) -> FileListDto:
        """
        List files in root
        List files in a root folder of the selected connector
        :param connectorId: string (required), path.
        :param fileType: string (optional), query.
        :param sort: string (optional), query.
        :param direction: string (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: FileListDto
        """
        endpoint = f"/api2/v1/connectors/{connectorId}/folders"
        params = {"fileType": fileType, "sort": sort, "direction": direction}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return FileListDto(**r)

    def getFile_1(
        self,
        file: str,
        folder: str,
        connectorId: str,
        body: GetFileRequestParamsDto,
        phrase_token: Optional[str] = None,
    ) -> AsyncFileOpResponseDto:
        """
                Download file (async)
                Create an asynchronous request to download a file from a (sub)folder of the selected connector.
        After a callback with successful response is received, prepared file can be downloaded by [Download prepared file](#operation/getPreparedFile)
        or [Create job from connector asynchronous download task](#operation/createJobFromAsyncDownloadTask).
                :param file: string (required), path.
                :param folder: string (required), path.
                :param connectorId: string (required), path.
                :param body: GetFileRequestParamsDto (required), body.

                :param phrase_token: string (optional) - if not supplied, client will look token from init

                :return: AsyncFileOpResponseDto
        """
        endpoint = f"/api2/v2/connectors/{connectorId}/folders/{folder}/files/{file}"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AsyncFileOpResponseDto(**r)

    def getPreparedFile(
        self,
        taskId: str,
        file: str,
        folder: str,
        connectorId: str,
        phrase_token: Optional[str] = None,
    ) -> bytes:
        """
        Download prepared file
        Download the file by referencing successfully finished async download request [Connector - Download file (async)](#operation/getFile_1).
        :param taskId: string (required), path.
        :param file: string (required), path.
        :param folder: string (required), path.
        :param connectorId: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: InputStreamLength
        """
        endpoint = f"/api2/v2/connectors/{connectorId}/folders/{folder}/files/{file}/tasks/{taskId}"
        params = {}

        files = None
        payload = None

        r = self.client.get_bytestream(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return r

    def uploadFile_1(
        self,
        fileName: str,
        folder: str,
        connectorId: str,
        mimeType: str = None,
        phrase_token: Optional[str] = None,
    ) -> AsyncFileOpResponseDto:
        """
        Upload file (async)
        Upload a file to a subfolder of the selected connector
        :param fileName: string (required), path.
        :param folder: string (required), path.
        :param connectorId: string (required), path.
        :param mimeType: string (optional), query. Mime type of the file to upload.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: AsyncFileOpResponseDto
        """
        endpoint = f"/api2/v2/connectors/{connectorId}/folders/{folder}/files/{fileName}/upload"
        params = {"mimeType": mimeType}

        files = None
        payload = None

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return AsyncFileOpResponseDto(**r)
