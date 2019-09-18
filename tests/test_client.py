import base64

import responses
import pytest

from wistia.api import WistiaAPI


def generate_http_basic_auth_string(username, password):
    encoded_string = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('ascii')
    return f'Basic {encoded_string}'


@pytest.fixture
def wistia_client():
    password = 'letmein'
    return WistiaAPI(api_password=password)


@responses.activate
def test_authentication_set_correctly_in_header(wistia_client):
    # Given
    expected_url = f'https://api.wistia.com/v1/medias.json'
    responses.add(responses.GET, url=expected_url, json={}, status=200)

    # When
    wistia_client.list_medias()

    # Then
    expected_auth_header = generate_http_basic_auth_string('api', 'letmein')
    assert expected_auth_header == responses.calls[0].request.headers['Authorization']


@responses.activate
def test_purchase_captions_hits_correct_endpoint(wistia_client):
    media_hashed_id = '12345'
    expected_url = f'https://api.wistia.com/v1/medias/{media_hashed_id}/captions/purchase.json'
    responses.add(responses.POST, url=expected_url, json={}, status=200)

    wistia_client.purchase_captions(media_hashed_id)
    assert expected_url == responses.calls[0].request.url
