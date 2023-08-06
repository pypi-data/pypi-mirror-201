from __future__ import annotations

import asyncio
import os
from types import TracebackType
from typing import Type

from httpx import AsyncClient as HttpxAsyncClient

from twilio_async.models.message import MessageLogs, MessageResponse, MessageSend


class AsyncClient:
    """A client for interacting with the Twilio API."""

    def __init__(
        self,
        account_sid: str | None = None,
        token: str | None = None,
        *,
        timeout: int | None = None,
    ) -> None:
        """Class initializer.

        Args:
            account_sid: Account SID. If `None` will attempt to read from the `TWILIO_ACCOUNT_SID`
                envoronment variable.
            token: Authentication token. If `None` will attempt to read from `TWILIO_AUTH_TOKEN`.
            timeout: The amount of time in seconds that the client will wait for a response before
                timing out. Defaults to None.
        """

        self.account_sid = account_sid or os.getenv("TWILIO_ACCOUNT_SID", None)

        if not self.account_sid:
            raise ValueError("No account_sid found")

        self.token = token or os.getenv("TWILIO_AUTH_TOKEN", None)

        if not self.token:
            raise ValueError("No account_sid found")

        self._http_client = HttpxAsyncClient(
            base_url=f"https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}/",
            timeout=timeout,
            auth=(self.account_sid, self.token),
        )

    async def __aenter__(self) -> AsyncClient:
        return self

    async def __aexit__(
        self,
        et: Type[BaseException] | None,
        ev: Type[BaseException] | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        """Closes the client.

        This only needs to be used if the client was not created with a context manager.
        """
        await self._http_client.aclose()

    async def get_message_logs(self, page_size: int = 100) -> MessageLogs:
        """Retrieve message logs.

        Args:
            page_size: The number of log records to retrieve per page. 1000 is the maximum allowed
                by Twilio. When sending a number greater than 1000 the API will cap the request at
                1000.

        Returns:
            The log information

        Examples:
            >>> from twilio_async import AsyncClient
            >>>
            >>>
            >>> async with AsyncClient() as client:
            >>>     response = await client.get_message_logs()
        """
        response = await self._http_client.get(f"Messages.json?PageSize={page_size}")
        response.raise_for_status

        return MessageLogs(**response.json())

    async def message_create(
        self,
        body: str,
        to: str,
        *,
        from_: str | None = None,
        messaging_service_sid: str | None = None,
    ) -> MessageResponse:
        """Sends a message.

        Args:
            body: Message body.
            to: The phone number to send the message to.
            from_: The phone number to send the message from. Defaults to `None`

        Returns:
            Message response information.

        Examples:
            >>> from twilio_async import AsyncClient
            >>>
            >>>
            >>> async with AsyncClient() as client:
            >>>     response = await client.message_create(
            >>>         "My message",
            >>>         "+15018675309",
            >>>     )
        """
        sid = messaging_service_sid or os.getenv("TWILIO_MESSAGING_SERVICE_SID", None)

        if not sid and not from_:
            raise ValueError("A messaging_service_sid or from_ is required")

        payload = {
            "Body": body,
            "To": to,
        }

        if sid:
            payload["MessagingServiceSid"] = sid

        if from_:
            payload["From"] = from_

        response = await self._http_client.post(
            url="Messages.json",
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()

        return MessageResponse(**response.json())

    async def batch_message_create(
        self,
        message_info: list[MessageSend],
    ) -> list[MessageResponse]:
        """Sends a message.

        Args:
            message_info: A list of messages to send.

        Returns:
            A list of message response information.

        Examples:
            >>> from twilio_async import AsyncClient
            >>> from twilio_async.models.message import MessageSend
            >>>
            >>>
            >>> message_info = [
            >>>     MessageSend(body="Message 1", to="+15018675309),
            >>>     MessageSend(body="Message 2", to="+15019035768"),
            >>> ]
            >>> async with AsyncClient() as client:
            >>>     response = await client.message_create(message_info)
        """
        tasks = []
        for message in message_info:
            tasks.append(
                asyncio.create_task(
                    self.message_create(
                        body=message.body,
                        to=message.to,
                        from_=message.from_,
                        messaging_service_sid=message.messaging_service_sid,
                    )
                )
            )

        return await asyncio.gather(*tasks)
