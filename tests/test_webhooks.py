import uuid
from datetime import datetime, timezone

import pytest

from wistia.webhooks import (
    EventDelivery,
    parse_webhook_event_delivery,
)

example_webhook_json_str = """
{
  "hook": {
    "uuid": "a4ab9eb6-ab82-4dae-86f2-29f744f7d031"
  },
  "events": [
    {
      "uuid": "fc53f8f78b67d04d455029813f8ec1ef",
      "type": "media.failed",
      "payload": {
        "media": {
          "duration": 40.207,
          "id": "vpe2p82q64",
          "name": "Lenny Delivers Video!",
          "thumbnail": {
            "url": "http://embed.wistia.com/deliveries/e96ea382701bc172657d90bf269211beddbf6f7f.jpg?image_crop_resized=200x120"
          },
          "url": "https://harper.wistia.com/medias/vpe2p82q64"
        }
      },
      "metadata": {
        "account_id": "0sxav1wj8o"
      },
      "generated_at": "2020-03-31T21:56:45Z"
    }
  ]
}"""


def test_webhook_models_parse_event_data_from_json_string():
    parsed_event_delivery = parse_webhook_event_delivery(example_webhook_json_str)
    assert parsed_event_delivery.hook.uuid == uuid.UUID(
        "a4ab9eb6-ab82-4dae-86f2-29f744f7d031"
    )
    assert len(parsed_event_delivery.events) == 1
    event = parsed_event_delivery.events[0]
    assert event.uuid == "fc53f8f78b67d04d455029813f8ec1ef"
    assert event.type == "media.failed"
    assert event.payload.media.id == "vpe2p82q64"
    assert event.payload.media.name == "Lenny Delivers Video!"
    assert event.payload.media.duration == 40.207
    assert (
        event.payload.media.thumbnail.url
        == "http://embed.wistia.com/deliveries/e96ea382701bc172657d90bf269211beddbf6f7f.jpg?image_crop_resized=200x120"
    )
    assert event.payload.media.url == "https://harper.wistia.com/medias/vpe2p82q64"
    assert event.metadata["account_id"] == "0sxav1wj8o"
    assert event.generated_at == datetime(2020, 3, 31, 21, 56, 45, tzinfo=timezone.utc)


delivery_template = {
    "hook": {
        "uuid": "a4ab9eb6-ab82-4dae-86f2-29f744f7d031"
    },
    "events": [],
}

media_event_data_template = {
    "uuid": "fc53f8f78b67d04d455029813f8ec1ef",
    "payload": {
        "media": {
            "id": "vpe2p82q64",
            "name": "Lenny Delivers Video!",
            "url": "https://harper.wistia.com/medias/vpe2p82q64",
            "duration": 40.207,
            "thumbnail": {
                "url": "http://embed.wistia.com/deliveries/e96ea382701bc172657d90bf269211beddbf6f7f.jpg?image_crop_resized=200x120"
            },
        }
    },
    "metadata": {"account_id": "0sxav1wj8o"},
    "generated_at": "2020-03-31T21:56:45Z",
}


media_created_event_data = {
    **media_event_data_template,
    "type": "media.created",
}

media_processing_event_data = {
    **media_event_data_template,
    "type": "media.processing",
}

media_ready_event_data = {
    **media_event_data_template,
    "type": "media.ready",
}

media_failed_event_data = {
    **media_event_data_template,
    "type": "media.failed",
}


media_updated_event_data = {
    **media_event_data_template,
    "type": "media.updated",
    "payload": {
        **media_event_data_template['payload'],
        "previous_attributes": {
            "thumbnail": {
                "url": "http://embed.wistia.com/deliveries/e04d7729a8b83f4fdd52e107b980f5594359bb45.jpg?image_crop_resized=200x120"
            }
        },
    },
}


media_deleted_event_data = {
    **media_event_data_template,
    "type": "media.deleted",
    "payload": {"media": {"id": "f5diqltruh"}},
}


def test_media_created_event():
    media_created_event_delivery_data = {**delivery_template, "events": [media_created_event_data]}
    delivery = EventDelivery(**media_created_event_delivery_data)
    assert delivery.hook.uuid == uuid.UUID(delivery_template['hook']['uuid'])
    event = delivery.events[0]
    assert event.type == "media.created"
    assert event.uuid == media_created_event_data['uuid']
    assert event.payload.media.id == media_created_event_data['payload']['media']['id']
    assert event.metadata['account_id'] == media_created_event_data['metadata']['account_id']
    assert event.generated_at == datetime.strptime(
        media_created_event_data['generated_at'], "%Y-%m-%dT%H:%M:%SZ"
    ).replace(tzinfo=timezone.utc)


@pytest.mark.parametrize("test_event_data,expected_event_type", [
    (media_created_event_data, "media.created"),
    (media_processing_event_data, "media.processing"),
    (media_ready_event_data, "media.ready"),
    (media_failed_event_data, "media.failed"),
    (media_updated_event_data, "media.updated"),
    (media_deleted_event_data, "media.deleted"),
])
def test_event_parsing(test_event_data, expected_event_type):
    event_delivery_data = {**delivery_template, "events": [test_event_data]}
    delivery = parse_webhook_event_delivery(event_delivery_data)
    assert delivery.events[0].type == expected_event_type


"""
hook=HookInfo(uuid=UUID('a4ab9eb6-ab82-4dae-86f2-29f744f7d031'))
events=[
    MediaCreatedEvent(
        type='media.created', 
        uuid='fc53f8f78b67d04d455029813f8ec1ef', 
        payload=MediaPayload(
            media=MediaInfo(
                id='vpe2p82q64', 
                name='Lenny Delivers Video!', 
                url='https://harper.wistia.com/medias/vpe2p82q64', 
                duration=40.207, 
                thumbnail=Thumbnail(
                    url='http://embed.wistia.com/deliveries/e96ea382701bc172657d90bf269211beddbf6f7f.jpg?image_crop_resized=200x120'
                )
            )
        ),
        metadata={'account_id': '0sxav1wj8o'}, 
        generated_at=datetime.datetime(2020, 3, 31, 21, 56, 45, tzinfo=datetime.timezone.utc)
    )
]
"""


viewing_session_event_data_template = {
    "uuid": "09e7b27100b3a000",
    "type": "viewing_session.play",
    "payload": {
        "visitor": {"id": "v20150227_c651bc81-8ec8-445b-b8a0-878d19278d35"},
        "viewing_session": {"id": "v20150225_e17a7db7-da7d-4d56-b5a8-ce6a9b62a800"},
        "media": {
            "id": "l9dqljgtfy",
            "name": "Lenny Eating Peanuts",
            "url": "http://dave.wistia.com/medias/l9dqljgtfy",
            "duration": 71.912,
            "thumbnail": {
                "url": "http://embed.wistia.com/deliveries/e04d7729a8b83f4fdd52e107b980f5594359bb45.jpg?image_crop_resized=200x120"
            },
        },
    },
    "metadata": {"account_id": "8lq25o0p9c"},
    "generated_at": "2016-03-31T13:59:22Z",
}

viewing_session_play_event_data = {
    **viewing_session_event_data_template,
    "type": "viewing_session.play",
}

viewing_session_percent_watched_event_data = {
    **viewing_session_event_data_template,
    "type": "viewing_session.percent_watched",
    "payload": {
        **viewing_session_event_data_template['payload'],
        "percent_watched": 25,
    },
}

viewing_session_turnstile_converted_event_data = {
    **viewing_session_event_data_template,
    "type": "viewing_session.turnstile.converted",
    "payload": {
        **viewing_session_event_data_template['payload'],
        "name": "Lenny Lavigne",
        "email": "lenny@wistia.com",
    },
}

viewing_session_call_to_action_converted_event_data = {
    **viewing_session_event_data_template,
    "type": "viewing_session.call_to_action.converted",
}

viewing_session_annotation_converted_event_data = {
    **viewing_session_event_data_template,
    "type": "viewing_session.annotation.converted",
}
