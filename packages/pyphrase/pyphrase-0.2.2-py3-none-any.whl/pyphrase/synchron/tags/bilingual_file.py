from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import ComparedSegmentsDto, InputStream, JobPartsDto


class BilingualFileOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def convertBilingualFile(
        self, body: InputStream, to: str, frm: str, phrase_token: Optional[str] = None
    ) -> bytes:
        """
        Convert bilingual file

        :param body: InputStream (required), body.
        :param to: string (required), query.
        :param frm: string (required), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/bilingualFiles/convert"
        params = {"from": frm, "to": to}

        files = None
        payload = body

        r = self.client.post_bytestream(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return r

    def uploadBilingualFile(
        self,
        body: InputStream,
        format: str = "MXLF",
        saveToTransMemory: str = "Confirmed",
        setCompleted: bool = "False",
        phrase_token: Optional[str] = None,
    ) -> JobPartsDto:
        """
        Upload bilingual file
        Returns updated job parts
        :param body: InputStream (required), body.
        :param format: string (optional), query.
        :param saveToTransMemory: string (optional), query.
        :param setCompleted: boolean (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: JobPartsDto
        """
        endpoint = f"/api2/v1/bilingualFiles"
        params = {
            "format": format,
            "saveToTransMemory": saveToTransMemory,
            "setCompleted": setCompleted,
        }

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return JobPartsDto(**r)

    def compareBilingualFile(
        self,
        body: InputStream,
        workflowLevel: int = "1",
        phrase_token: Optional[str] = None,
    ) -> ComparedSegmentsDto:
        """
        Compare bilingual file
        Compares bilingual file to job state. Returns list of compared segments.
        :param body: InputStream (required), body.
        :param workflowLevel: integer (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ComparedSegmentsDto
        """
        endpoint = f"/api2/v1/bilingualFiles/compare"
        params = {"workflowLevel": workflowLevel}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ComparedSegmentsDto(**r)

    def getPreviewFile(
        self, body: InputStream, phrase_token: Optional[str] = None
    ) -> bytes:
        """
        Download preview
        Supports mxliff format
        :param body: InputStream (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/bilingualFiles/preview"
        params = {}

        files = None
        payload = body

        r = self.client.post_bytestream(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return r
