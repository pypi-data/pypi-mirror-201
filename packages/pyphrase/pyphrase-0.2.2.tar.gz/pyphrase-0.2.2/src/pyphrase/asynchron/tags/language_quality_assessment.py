from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient


class LanguageQualityAssessmentOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def downloadLqaReports(
        self, jobParts: str, phrase_token: Optional[str] = None
    ) -> bytes:
        """
                Download LQA Assessment XLSX reports
                Returns a single xlsx report or ZIP archive with multiple reports.
        If any given jobPart is not from LQA workflow step, reports from successive workflow steps may be returned
        If none were found returns 404 error, otherwise returns those that were found.
                :param jobParts: string (required), query. Comma separated list of JobPart UIDs.

                :param phrase_token: string (optional) - if not supplied, client will look token from init

                :return: None
        """
        endpoint = f"/api2/v1/lqa/assessments/reports"
        params = {"jobParts": jobParts}

        files = None
        payload = None

        r = await self.client.get_bytestream(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return r
