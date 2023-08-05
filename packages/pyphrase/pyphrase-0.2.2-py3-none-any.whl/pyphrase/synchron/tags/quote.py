from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

if TYPE_CHECKING:
    from ..client import SyncPhraseTMSClient

from ...models.phrase_models import (
    EmailQuotesRequestDto,
    EmailQuotesResponseDto,
    QuoteCreateV2Dto,
    QuoteDto,
    QuoteV2Dto,
)


class QuoteOperations:
    def __init__(self, client: SyncPhraseTMSClient):
        self.client = client

    def get_2(
        self,
        quoteUid: str,
        phrase_token: Optional[str] = None,
    ) -> QuoteDto:
        """
        Get quote

        :param quoteUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: QuoteDto
        """
        endpoint = f"/api2/v1/quotes/{quoteUid}"
        params = {}

        files = None
        payload = None

        r = self.client.get(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return QuoteDto(**r)

    def deleteQuote(
        self,
        quoteUid: str,
        phrase_token: Optional[str] = None,
    ) -> None:
        """
        Delete quote

        :param quoteUid: string (required), path.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: None
        """
        endpoint = f"/api2/v1/quotes/{quoteUid}"
        params = {}

        files = None
        payload = None

        r = self.client.delete(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return

    def emailQuotes(
        self,
        body: EmailQuotesRequestDto,
        phrase_token: Optional[str] = None,
    ) -> EmailQuotesResponseDto:
        """
        Email quotes

        :param body: EmailQuotesRequestDto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: EmailQuotesResponseDto
        """
        endpoint = f"/api2/v1/quotes/email"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return EmailQuotesResponseDto(**r)

    def createQuoteV2(
        self,
        body: QuoteCreateV2Dto,
        phrase_token: Optional[str] = None,
    ) -> QuoteV2Dto:
        """
        Create quote
        Either WorkflowSettings or Units must be sent for billingUnit "Hour".
        :param body: QuoteCreateV2Dto (required), body.

        :param phrase_token: string (optional) - if not supplied, client will look token from init

        :return: QuoteV2Dto
        """
        endpoint = f"/api2/v2/quotes"
        params = {}

        files = None
        payload = body

        r = self.client.post(
            endpoint, phrase_token, params=params, payload=payload, files=files
        )

        return QuoteV2Dto(**r)
