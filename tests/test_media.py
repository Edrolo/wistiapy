import logging
from os import path

import pytest
import json

import responses

from wistia import WistiaClient
from wistia.schema import Media

log = logging.getLogger("test_wistia")


@pytest.fixture
def media_list():
    json_string = open(path.join(path.dirname(__file__), "test_media.json")).read()
    return json.loads(json_string)


def test_media_parsing(media_list):
    medias = [Media(media_data) for media_data in media_list]
    assert len(medias) == 2
    assert len(medias[0].assets) == 3


def test_direct_instantiation_of_schema_is_deep(media_list):
    medias = [Media(media_data) for media_data in media_list]
    assert medias[0].thumbnail.url == media_list[0]["thumbnail"]["url"]


@responses.activate
def test_authentication_set_correctly_in_header():
    # Given
    password = "let-me-in"
    client = WistiaClient(api_password=password)
    expected_url = "https://api.wistia.com/v1/medias.json"
    responses.add(responses.GET, url=expected_url, json=[], status=200)

    # When
    client.list_medias()

    # Then
    expected_auth_header = f"Bearer {password}"
    request, response = responses.calls[0]
    observed_auth_header = request.headers["Authorization"]
    assert observed_auth_header == expected_auth_header


@responses.activate
def test_purchase_captions_hits_correct_endpoint():
    media_hashed_id = "12345"
    expected_url = (
        f"https://api.wistia.com/v1/medias/{media_hashed_id}/captions/purchase.json"
    )
    responses.add(responses.POST, url=expected_url, json={}, status=200)

    WistiaClient().purchase_captions(media_hashed_id)
    request, response = responses.calls[0]
    assert request.url == expected_url
    assert request.method == "POST"
    assert request.body is None
