from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    GlossaryActivationDto,
    GlossaryDto,
    GlossaryEditDto,
    PageDtoGlossaryDto,
)


class GlossaryOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def getGlossary(
        self,
        glossaryUid: str,
        phrase_token: Optional[str] = None,
    ) -> GlossaryDto:
        """
        Get glossary

        :param glossaryUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: GlossaryDto
        """
        endpoint = f"/api2/v1/glossaries/{glossaryUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return GlossaryDto(**r)

    def updateGlossary(
        self,
        glossaryUid: str,
        body: GlossaryEditDto,
        phrase_token: Optional[str] = None,
    ) -> GlossaryDto:
        """
        Edit glossary
        Languages can only be added, their removal is not supported
        :param glossaryUid: string (required), path.
        :param body: GlossaryEditDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: GlossaryDto
        """
        endpoint = f"/api2/v1/glossaries/{glossaryUid}"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return GlossaryDto(**r)

    def deleteGlossary(
        self,
        glossaryUid: str,
        purge: bool = "False",
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete glossary

        :param glossaryUid: string (required), path.
        :param purge: boolean (optional), query. purge=false - the Glossary can later be restored,
                    &#39;purge=true - the Glossary is completely deleted and cannot be restored.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/glossaries/{glossaryUid}"
        params = {"purge": purge}

        files = None
        payload = None

        r = self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def listGlossaries(
        self,
        lang: List[str] = None,
        name: str = None,
        pageNumber: int = "0",
        pageSize: int = "50",
        phrase_token: Optional[str] = None,
    ) -> PageDtoGlossaryDto:
        """
        List glossaries

        :param lang: array (optional), query. Language of the glossary.
        :param name: string (optional), query.
        :param pageNumber: integer (optional), query. Page number, starting with 0, default 0.
        :param pageSize: integer (optional), query. Page size, accepts values between 1 and 50, default 50.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PageDtoGlossaryDto
        """
        endpoint = f"/api2/v1/glossaries"
        params = {
            "name": name,
            "lang": lang,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
        }

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PageDtoGlossaryDto(**r)

    def createGlossary(
        self,
        body: GlossaryEditDto,
        phrase_token: Optional[str] = None,
    ) -> GlossaryDto:
        """
        Create glossary

        :param body: GlossaryEditDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: GlossaryDto
        """
        endpoint = f"/api2/v1/glossaries"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return GlossaryDto(**r)

    def activateGlossary(
        self,
        glossaryUid: str,
        body: GlossaryActivationDto,
        phrase_token: Optional[str] = None,
    ) -> GlossaryDto:
        """
        Activate/Deactivate glossary

        :param glossaryUid: string (required), path.
        :param body: GlossaryActivationDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: GlossaryDto
        """
        endpoint = f"/api2/v1/glossaries/{glossaryUid}/activate"
        params = {}

        files = None
        payload = body

        r = self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return GlossaryDto(**r)
