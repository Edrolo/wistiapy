import logging
from os import path

import pytest
import json

from wistia.media import Media

log = logging.getLogger("test_wistia")


@pytest.fixture
def media_list():
    json_string = open(path.join(path.dirname(__file__), "test_media.json")).read()
    return json.loads(json_string)


def test_media_parsing(media_list):
    medias = [Media(media_data) for media_data in media_list]
    assert len(medias) == 2
    assert len(medias[0].assets) == 3
