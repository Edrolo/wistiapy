import hashlib
import hmac
from datetime import datetime
from typing_extensions import Annotated, Literal
from typing import List, Union

import uuid as uuid
from pydantic import BaseModel, Field


media_event_type_names = Literal[
    "media.created",
    "media.processing",
    "media.ready",
    "media.failed",
    "media.updated",
    "media.deleted",
]


viewing_event_type_names = Literal[
    "viewing_session.play",
    "viewing_session.percent_watched",
    "viewing_session.turnstile.converted",
    "viewing_session.call_to_action.converted",
    "viewing_session.annotation.converted",
]


class Thumbnail(BaseModel):
    url: str


class MediaInfo(BaseModel):
    id: str
    name: str
    url: str
    duration: float
    thumbnail: Thumbnail


class MediaReference(BaseModel):
    id: str


class MediaPayload(BaseModel):
    media: MediaInfo


class MediaDeletedPayload(MediaPayload):
    media: MediaReference


class MediaUpdatedPayload(BaseModel):
    media: MediaInfo
    previous_attributes: dict


class MediaEvent(BaseModel):
    type: media_event_type_names
    uuid: str
    payload: Union[MediaPayload, MediaUpdatedPayload, MediaDeletedPayload]
    metadata: dict
    generated_at: datetime


class MediaCreatedEvent(MediaEvent):
    type: Literal["media.created"]
    payload: MediaPayload


class MediaProcessingEvent(MediaEvent):
    type: Literal["media.processing"]
    payload: MediaPayload


class MediaReadyEvent(MediaEvent):
    type: Literal["media.ready"]
    payload: MediaPayload


class MediaFailedEvent(MediaEvent):
    type: Literal["media.failed"]
    payload: MediaPayload


class MediaUpdatedEvent(MediaEvent):
    type: Literal["media.updated"]
    payload: MediaUpdatedPayload


class MediaDeletedEvent(MediaEvent):
    type: Literal["media.deleted"]
    payload: MediaDeletedPayload


MediaEvent = Annotated[
    Union[
        MediaCreatedEvent,
        MediaProcessingEvent,
        MediaReadyEvent,
        MediaFailedEvent,
        MediaUpdatedEvent,
        MediaDeletedEvent,
    ],
    Field(discriminator="type"),
]


class HookInfo(BaseModel):
    uuid: uuid.UUID


class EventDelivery(BaseModel):
    hook: HookInfo
    events: List[MediaEvent]


def parse_webhook_event_delivery(event_data: Union[str, bytes, dict]) -> EventDelivery:
    """
    Parse the event data from a Wistia webhook request.
    :param event_data: May be a JSON string, a bytes object, or a dict.
    :return: EventDelivery
    """
    if isinstance(event_data, dict):
        return EventDelivery(**event_data)
    else:
        return EventDelivery.parse_raw(event_data)


def compute_signature_hash(request_body: bytes, webhook_secret_key: str) -> str:
    """
    Parse the signature included in the request header and compute the hash of the request body.

    Usage:
    if request.META.get('HTTP_X_WISTIA_SIGNATURE') == compute_signature(
        request_body=request.body,
        secret_key=settings.WISTIA_WEBHOOK_SECRET_KEY,
    ):
        # Authenticated
    """
    return hmac.new(
        key=webhook_secret_key.encode(), msg=request_body, digestmod=hashlib.sha256
    ).hexdigest()
