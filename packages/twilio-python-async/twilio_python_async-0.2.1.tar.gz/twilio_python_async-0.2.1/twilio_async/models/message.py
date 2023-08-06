from datetime import datetime
from typing import List, Union

from pydantic import BaseModel, Field, validator


class SubresouceUris(BaseModel):
    media: str


class MessageResponse(BaseModel):
    body: str
    num_segments: int
    direction: str
    from_: Union[str, None] = Field(None, alias="field")
    date_updated: datetime
    price: Union[float, None] = None
    error_message: Union[str, None] = None
    uri: str
    account_sid: str
    num_media: int
    to: str
    date_created: datetime
    status: str
    sid: str
    date_sent: Union[datetime, None] = None
    error_code: Union[int, None] = None
    price_unit: Union[str, None] = None
    api_version: str
    subresource_uris: SubresouceUris
    messaging_service_sid: Union[str, None] = None

    @validator("date_updated", pre=True)
    def parse_date_updated(cls, v: str) -> datetime:
        return _to_datetime(v)

    @validator("date_created", pre=True)
    def parse_date_created(cls, v: str) -> datetime:
        return _to_datetime(v)

    @validator("date_sent", pre=True)
    def parse_date_sent(cls, v: Union[str, None]) -> Union[datetime, None]:
        if not v:
            return None

        return _to_datetime(v)


class MessageLogs(BaseModel):
    first_page_uri: str
    end: int
    previous_page_uri: Union[str, None] = None
    messages: List[MessageResponse]
    uri: str
    page_size: int
    start: int
    next_page_uri: Union[str, None] = None
    page: int


class MessageSend(BaseModel):
    body: str
    to: str
    from_: Union[str, None] = None
    messaging_service_sid: Union[str, None] = None


def _to_datetime(value: str) -> datetime:
    return datetime.strptime(value, "%a, %d %b %Y %H:%M:%S %z")
