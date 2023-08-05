from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import AsyncPhraseTMSClient

from ...models.phrase_models import (
    ConversationListDto,
    EditPlainConversationDto,
    FindConversationsDto,
    LQAConversationDto,
    LQAConversationsListDto,
    PlainConversationDto,
    PlainConversationsListDto,
)


class ConversationsOperations:
    def __init__(self, client: AsyncPhraseTMSClient):
        self.client = client

    async def listAllConversations(
        self,
        jobUid: str,
        since: str = None,
        includeDeleted: bool = "False",
        phrase_token: Optional[str] = None,
    ) -> ConversationListDto:
        """
        List all conversations

        :param jobUid: string (required), path.
        :param since: string (optional), query.
        :param includeDeleted: boolean (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ConversationListDto
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations"
        params = {"includeDeleted": includeDeleted, "since": since}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ConversationListDto(**r)

    async def findConversations(
        self, body: FindConversationsDto, phrase_token: Optional[str] = None
    ) -> ConversationListDto:
        """
        Find all conversation

        :param body: FindConversationsDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: ConversationListDto
        """
        endpoint = f"/api2/v1/jobs/conversations/find"
        params = {}

        files = None
        payload = body

        r = await self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return ConversationListDto(**r)

    async def deleteLQAComment(
        self,
        commentId: str,
        conversationId: str,
        jobUid: str,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete LQA comment

        :param commentId: string (required), path.
        :param conversationId: string (required), path.
        :param jobUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/lqas/{conversationId}/comments/{commentId}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def getLQAConversation(
        self, conversationId: str, jobUid: str, phrase_token: Optional[str] = None
    ) -> LQAConversationDto:
        """
        Get LQA conversation

        :param conversationId: string (required), path.
        :param jobUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: LQAConversationDto
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/lqas/{conversationId}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return LQAConversationDto(**r)

    async def deleteLQAConversation(
        self, conversationId: str, jobUid: str, phrase_token: Optional[str] = None
    ) -> None:
        """
        Delete LQA conversation

        :param conversationId: string (required), path.
        :param jobUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/lqas/{conversationId}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def listLQAConversations(
        self,
        jobUid: str,
        since: str = None,
        includeDeleted: bool = "False",
        phrase_token: Optional[str] = None,
    ) -> LQAConversationsListDto:
        """
        List LQA conversations

        :param jobUid: string (required), path.
        :param since: string (optional), query.
        :param includeDeleted: boolean (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: LQAConversationsListDto
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/lqas"
        params = {"includeDeleted": includeDeleted, "since": since}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return LQAConversationsListDto(**r)

    async def getPlainConversation(
        self, conversationId: str, jobUid: str, phrase_token: Optional[str] = None
    ) -> PlainConversationDto:
        """
        Get plain conversation

        :param conversationId: string (required), path.
        :param jobUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PlainConversationDto
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/plains/{conversationId}"
        params = {}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PlainConversationDto(**r)

    async def updatePlainConversation(
        self,
        conversationId: str,
        jobUid: str,
        body: EditPlainConversationDto,
        phrase_token: Optional[str] = None,
    ) -> PlainConversationDto:
        """
        Edit plain conversation

        :param conversationId: string (required), path.
        :param jobUid: string (required), path.
        :param body: EditPlainConversationDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PlainConversationDto
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/plains/{conversationId}"
        params = {}

        files = None
        payload = body

        r = await self.client.put(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PlainConversationDto(**r)

    async def deletePlainConversation(
        self, conversationId: str, jobUid: str, phrase_token: Optional[str] = None
    ) -> None:
        """
        Delete plain conversation

        :param conversationId: string (required), path.
        :param jobUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/plains/{conversationId}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    async def listPlainConversations(
        self,
        jobUid: str,
        since: str = None,
        includeDeleted: bool = "False",
        phrase_token: Optional[str] = None,
    ) -> PlainConversationsListDto:
        """
        List plain conversations

        :param jobUid: string (required), path.
        :param since: string (optional), query.
        :param includeDeleted: boolean (optional), query.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: PlainConversationsListDto
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/plains"
        params = {"includeDeleted": includeDeleted, "since": since}

        files = None
        payload = None

        r = await self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return PlainConversationsListDto(**r)

    async def deletePlainComment(
        self,
        commentId: str,
        conversationId: str,
        jobUid: str,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete plain comment

        :param commentId: string (required), path.
        :param conversationId: string (required), path.
        :param jobUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/jobs/{jobUid}/conversations/plains/{conversationId}/comments/{commentId}"
        params = {}

        files = None
        payload = None

        r = await self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return
