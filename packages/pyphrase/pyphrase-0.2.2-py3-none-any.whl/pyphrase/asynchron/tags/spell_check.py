from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    DictionaryItemDto,
    SpellCheckRequestDto,
    SpellCheckResponseDto,
    SuggestRequestDto,
    SuggestResponseDto,
)


class SpellCheckOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def check(
        self, body: SpellCheckRequestDto, phrase_token: Optional[str] = None
    ) -> SpellCheckResponseDto:
        """
        Spell check
        Spell check using the settings of the user's organization
        :param body: SpellCheckRequestDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: SpellCheckResponseDto
        """
        endpoint = f"/api2/v1/spellCheck/check"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return SpellCheckResponseDto(**r)

    async def checkByJob(
        self,
        jobUid: str,
        body: SpellCheckRequestDto,
        phrase_token: Optional[str] = None,
    ) -> SpellCheckResponseDto:
        """
        Spell check for job
        Spell check using the settings from the project of the job
        :param jobUid: string (required), path.
        :param body: SpellCheckRequestDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: SpellCheckResponseDto
        """
        endpoint = f"/api2/v1/spellCheck/check/{jobUid}"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return SpellCheckResponseDto(**r)

    async def addWord(
        self, body: DictionaryItemDto, phrase_token: Optional[str] = None
    ) -> None:
        """
        Add word to dictionary

        :param body: DictionaryItemDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/spellCheck/words"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def suggest(
        self, body: SuggestRequestDto, phrase_token: Optional[str] = None
    ) -> SuggestResponseDto:
        """
        Suggest a word
        Spell check suggest using the users's spell check dictionary
        :param body: SuggestRequestDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: SuggestResponseDto
        """
        endpoint = f"/api2/v1/spellCheck/suggest"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return SuggestResponseDto(**r)
