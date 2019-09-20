from typing import (
    NamedTuple,
    Iterable,
)

import requests
from wistia.schema import (
    Media,
    CaptionTrack,
    Project,
)

from wistia.api import WistiaClient

import logging

log = logging.getLogger(__name__)


class FakeResponse(NamedTuple):
    status_code: int


class DummyWistiaClient(WistiaClient):
    def __init__(self, user="api", api_password=""):
        super().__init__(user, api_password)
        self.session = (
            None
        )  # Make sure we don't hit the API in methods not yet overridden

        self.medias = {}
        self.projects = {}

    def list_projects(
        self,
        sort_by=None,  # None:ProjectID,  name, created, or updated
        sort_direction=1,
        page=1,
        per_page=100,
    ) -> Iterable[Project]:
        log.info(
            f"WISTIA API CALL: list_projects("
            f"sort_by={sort_by!r}, sort_direction={sort_direction!r}, "
            f"page={page!r}, per_page={per_page!r})"
        )
        return self.projects.values()

    def list_all_projects(self) -> Iterable[Project]:
        log.info(f"WISTIA API CALL: list_all_projects()")
        yield from self.projects.values()

    def show_project(self, project_hashed_id: str) -> Project:
        log.info(f"WISTIA API CALL: show_project({project_hashed_id})")
        return self.projects[project_hashed_id]

    def list_medias(
        self,
        sort_by=None,  # None:ProjectID,  name, created, or updated
        sort_direction=1,
        page=1,
        per_page=100,
        project_id=None,
        name=None,
        media_type=None,
    ) -> Iterable[Media]:
        log.info(
            f"WISTIA API CALL: list_medias("
            f"sort_by={sort_by!r}, sort_direction={sort_direction!r}, "
            f"page={page!r}, per_page={per_page!r}, "
            f"project_id={project_id!r}, name={name!r}, media_type={media_type!r}"
            f")"
        )
        return self.medias.values()

    def show_media(self, wistia_hashed_id: str) -> Media:
        log.info(f"WISTIA API CALL: show_media({wistia_hashed_id})")
        return self.medias[wistia_hashed_id]

    def show_media_customizations(self, wistia_hashed_id: str) -> dict:
        log.info(f"WISTIA API CALL: show_media_customizations({wistia_hashed_id!r})")
        return {}

    def list_captions(self, wistia_hashed_id: str) -> Iterable[CaptionTrack]:
        log.info(f"WISTIA API CALL: list_captions({wistia_hashed_id!r})")
        return self.medias[wistia_hashed_id].captions

    def create_captions(
        self,
        wistia_hashed_id: str,
        language_code: str = "eng",
        caption_filename: str = "",
        caption_text: str = "",
    ) -> None:
        log.info(
            f"WISTIA API CALL: create_captions({wistia_hashed_id!r}, {language_code!r}, "
            f"caption_filename={caption_filename!r}, caption_text={caption_text!r})"
        )
        self.medias[wistia_hashed_id].captions.append(
            CaptionTrack(
                {
                    "language": language_code,
                    "text": caption_text,
                    "english_name": "English"
                    if language_code == "eng"
                    else f'"{language_code}"',
                    "native_name": "English"
                    if language_code == "eng"
                    else f'"{language_code}"',
                    "is_draft": False,
                }
            )
        )

    def show_captions(self, wistia_hashed_id, language_code: str = "eng") -> CaptionTrack:
        log.info(
            f"WISTIA API CALL: show_captions({wistia_hashed_id!r}, language_code={language_code!r})"
        )
        appropriate_captions = [
            track
            for track in self.medias[wistia_hashed_id].captions
            if track.language == language_code
        ]
        if not appropriate_captions:
            raise requests.HTTPError(response=FakeResponse(status_code=404))
        return appropriate_captions[0]

    def update_captions(
        self, wistia_hashed_id, language_code, caption_filename="", caption_text=""
    ) -> None:
        log.info(
            f"WISTIA API CALL: update_captions({wistia_hashed_id!r}, {language_code!r}, "
            f"caption_filename={caption_filename!r}, caption_text={caption_text!r})"
        )
        appropriate_captions = [
            track
            for track in self.medias[wistia_hashed_id].captions
            if track.language == language_code
        ]
        if not appropriate_captions:
            raise requests.HTTPError(response=FakeResponse(status_code=404))
        appropriate_captions[0]["text"] = caption_text

    def delete_captions(self, wistia_hashed_id: str, language_code: str = "eng") -> None:
        log.info(f"WISTIA API CALL: delete_captions({wistia_hashed_id!r})")
        appropriate_captions = [
            track
            for track in self.medias[wistia_hashed_id].captions
            if track.language == language_code
        ]
        if not appropriate_captions:
            raise requests.HTTPError(response=FakeResponse(status_code=404))
        self.medias[wistia_hashed_id]["captions"].remove(appropriate_captions[0])

    def purchase_captions(self, wistia_hashed_id: str) -> None:
        log.info(f"WISTIA API CALL: purchase_captions({wistia_hashed_id!r})")

    def enable_captions_for_media(
        self, wistia_hashed_id: str, enabled: bool = True
    ) -> dict:
        log.info(
            f"WISTIA API CALL: enable_captions_for_media({wistia_hashed_id!r}, enabled={enabled!r})"
        )
        return {}

    def upload_subtitle_file_to_wistia_video(
        self,
        wistia_hashed_id: str,
        subtitle_file_name: str,
        replace=False,
        language_code: str = "eng",
    ) -> None:
        log.info(
            f"WISTIA API CALL: "
            f"upload_subtitle_file_to_wistia_video("
            f"{wistia_hashed_id}, {subtitle_file_name}, replace={replace}, {language_code})"
        )