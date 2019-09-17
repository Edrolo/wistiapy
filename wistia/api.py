import logging
import requests

from . import media


log = logging.getLogger("wistiapy")


class WistiaAPI:
    API_BASE_URL = "https://api.wistia.com/v1/"

    def __init__(self, user="api", api_password=""):
        # https://wistia.com/support/developers/data-api#authentication
        self.session = requests.Session()
        self.session.auth = (user, api_password)

    def get(self, rel_path, params):
        url = f"{self.API_BASE_URL}{rel_path}"
        response = self.session.get(url)
        response.raise_for_status()
        response_data = response.json()
        return response_data

    def list_medias(
        self,
        sort_by="name",
        sort_direction=1,
        page=1,
        per_page=100,
        project_id=None,
        name=None,
        type=None,
    ):
        # https://wistia.com/support/developers/data-api#medias_list
        params = {
            "sort_by": sort_by,
            "sort_direction": sort_direction,
            "page": page,
            "per_page": per_page,
        }
        if project_id:
            params["project_id"] = project_id
        if name is not None:
            params["name"] = name
        if type is not None:
            params["type"] = type

        medias_list = self.get("medias.json", params=params)

        return [media.Media(media_data) for media_data in medias_list]
