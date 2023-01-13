import logging
from itertools import count
from typing import Iterable

import requests
from wistia.schema import Media, Project, CaptionTrack

log = logging.getLogger("wistiapy")


class WistiaClient:
    API_BASE_URL = "https://api.wistia.com/v1/"

    def __init__(self, api_password=""):
        # https://wistia.com/support/developers/data-api#authentication
        self.session = requests.Session()
        self.session.headers = {
            "Authorization": f"Bearer {api_password}",
            **self.session.headers
        }

    def request(self, method, rel_path, **kwargs):
        url = f"{self.API_BASE_URL}{rel_path}"
        response = self.session.request(method=method, url=url, **kwargs)
        response.raise_for_status()
        response_data = response.json() if response.text else {}
        return response_data

    def get(self, rel_path: str, params: dict = None):
        return self.request("GET", rel_path, params=params)

    def post(self, rel_path: str, **kwargs):
        return self.request("POST", rel_path, **kwargs)

    def put(self, rel_path: str, **kwargs):
        return self.request("PUT", rel_path, **kwargs)

    def delete(self, rel_path: str):
        return self.request("DELETE", rel_path)

    # Projects

    def list_projects(
        self,
        sort_by=None,  # None:ProjectID,  name, created, or updated
        sort_direction=1,
        page=1,
        per_page=100,
    ) -> Iterable[Project]:
        # https://wistia.com/support/developers/data-api#projects_list
        params = {"page": page, "per_page": per_page}
        if sort_by:
            params["sort_by"] = sort_by
            params["sort_direction"] = sort_direction

        project_list = self.get("projects.json", params=params)
        return [
            Project(project_data, strict=False)
            for project_data in project_list
        ]

    def list_all_projects(self) -> Iterable[Project]:
        log.info("Listing all projects")
        for page in count(start=1):
            next_page_of_projects = self.list_projects(page=page)
            if next_page_of_projects:
                yield from next_page_of_projects
            else:
                return

    def show_project(self, project_hashed_id: str) -> Project:
        # https://wistia.com/support/developers/data-api#projects_show
        rel_path = f"projects/{project_hashed_id}.json"
        project_data = self.get(rel_path)
        return Project(project_data, strict=False)

    # https://wistia.com/support/developers/data-api#projects_create
    # https://wistia.com/support/developers/data-api#projects_update
    # https://wistia.com/support/developers/data-api#projects_delete
    # https://wistia.com/support/developers/data-api#projects_copy

    # Project Sharings
    # https://wistia.com/support/developers/data-api#project_sharings_list
    # https://wistia.com/support/developers/data-api#project_sharings_show
    # https://wistia.com/support/developers/data-api#project_sharings_create
    # https://wistia.com/support/developers/data-api#project_sharings_update
    # https://wistia.com/support/developers/data-api#project_sharings_delete

    # Medias

    def list_medias(
        self,
        sort_by="name",
        sort_direction=1,
        page=1,
        per_page=100,
        project_id=None,
        name=None,
        media_type=None,
    ) -> Iterable[Media]:
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
        if media_type is not None:
            params["type"] = media_type

        medias_list = self.get("medias.json", params=params)

        return [
            Media(media_data, strict=False) for media_data in medias_list
        ]

    def show_media(self, wistia_hashed_id: str) -> Media:
        # https://wistia.com/support/developers/data-api#medias_show
        rel_path = f"medias/{wistia_hashed_id}.json"
        media_data = self.get(rel_path)
        return Media(media_data, strict=False)

    # https://wistia.com/support/developers/data-api#medias_update
    # https://wistia.com/support/developers/data-api#medias_delete
    # https://wistia.com/support/developers/data-api#medias_copy
    # https://wistia.com/support/developers/data-api#medias_stats

    # Account
    # https://wistia.com/support/developers/data-api#account

    # Customizations

    def show_media_customizations(self, wistia_hashed_id: str) -> dict:
        # https://wistia.com/support/developers/data-api#customizations_show
        rel_path = f"medias/{wistia_hashed_id}/customizations.json"
        return self.get(rel_path)

    # https://wistia.com/support/developers/data-api#customizations_create
    # https://wistia.com/support/developers/data-api#customizations_update
    # https://wistia.com/support/developers/data-api#customizations_delete

    # Captions

    def list_captions(self, wistia_hashed_id: str) -> Iterable[CaptionTrack]:
        rel_path = f"medias/{wistia_hashed_id}/captions.json"
        caption_list = self.get(rel_path)
        return [
            CaptionTrack(caption_data, strict=False)
            for caption_data in caption_list
        ]

    def create_captions(
        self,
        wistia_hashed_id: str,
        language_code: str = "eng",
        caption_filename: str = "",
        caption_text: str = "",
    ) -> None:
        # https://wistia.com/support/developers/data-api#captions_create
        # Empty 200: OK; 400: already exist; 404: video DNE
        rel_path = f"medias/{wistia_hashed_id}/captions.json"
        if caption_text:
            self.post(
                rel_path, data={"language": language_code, "caption_file": caption_text}
            )
        elif caption_filename:
            with open(caption_filename, "rb") as caption_file:
                self.post(
                    rel_path,
                    data={"language": language_code},
                    files={"caption_file": caption_file},
                )
        else:
            raise ValueError(
                "create_captions requires subtitle_filename or subtitle_text"
            )

    def show_captions(
        self, wistia_hashed_id, language_code: str = "eng"
    ) -> CaptionTrack:
        # https://wistia.com/support/developers/data-api#captions_show
        rel_path = f"medias/{wistia_hashed_id}/captions/{language_code}.json"
        return CaptionTrack(self.get(rel_path))

    def update_captions(
        self, wistia_hashed_id, language_code, caption_filename="", caption_text=""
    ) -> None:
        # https://wistia.com/support/developers/data-api#captions_update
        rel_path = f"medias/{wistia_hashed_id}/captions/{language_code}.json"
        if caption_text:
            r = self.session.put(rel_path, data={"caption_file": caption_text})
        elif caption_filename:
            with open(caption_filename, "rb") as caption_file:
                r = self.put(rel_path, files={"caption_file": caption_file})
        else:
            raise ValueError(
                "update_captions requires subtitle_filename or subtitle_text"
            )

        r.raise_for_status()

    def delete_captions(
        self, wistia_hashed_id: str, language_code: str = "eng"
    ) -> None:
        # https://wistia.com/support/developers/data-api#captions_delete
        rel_path = f"medias/{wistia_hashed_id}/captions/{language_code}.json"
        self.delete(rel_path)

    def purchase_captions(self, wistia_hashed_id: str) -> None:
        # https://wistia.com/support/developers/data-api#captions_purchase
        rel_path = f"medias/{wistia_hashed_id}/captions/purchase.json"
        self.post(rel_path)

    def enable_captions_for_media(
        self, wistia_hashed_id: str, enabled: bool = True
    ) -> dict:
        # https://wistia.com/support/developers/data-api#customizations_update
        # > If a value is null, then that key will be deleted from the saved customizations.
        # > If it is not null, that value will be set.
        rel_path = f"medias/{wistia_hashed_id}/customizations.json"
        if enabled:
            payload = {"plugin": {"captions-v1": {"onByDefault": False}}}
        else:
            payload = {"plugin": {"captions-v1": None}}

        return self.put(rel_path, json=payload)

    def upload_subtitle_file_to_wistia_video(
        self,
        wistia_hashed_id: str,
        subtitle_file_name: str,
        replace=False,
        language_code: str = "eng",
    ) -> None:
        captions_list = self.list_captions(wistia_hashed_id=wistia_hashed_id)
        replaceable_captions = [
            track for track in captions_list if track.language == language_code
        ]

        if replace and replaceable_captions:
            self.update_captions(
                wistia_hashed_id, language_code, caption_filename=subtitle_file_name
            )
        else:
            self.create_captions(
                wistia_hashed_id, language_code, caption_filename=subtitle_file_name
            )
