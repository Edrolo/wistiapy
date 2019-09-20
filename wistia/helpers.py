from os import environ

from wistia.client import WistiaClient
from wistia.dummy import DummyWistiaClient

import logging

log = logging.getLogger(__name__)


def get_wistia_client(password: str = None, client_cls=None) -> WistiaClient:
    # Calling with password='' will get you a DummyWistiaClient
    try:
        # If we're running Django, pull WISTIA_CLIENT_CLASS from settings
        from django.conf import settings

        if client_cls is None:
            client_class_name = getattr(settings, "WISTIA_CLIENT_CLASS", "WistiaClient")
            client_cls = globals()[client_class_name]

        password = password or getattr(settings, "WISTIA_API_PASSWORD", None)
    except ImportError:
        pass

    if password is None:
        password = environ.get("WISTIA_API_PASSWORD")

    if client_cls is None:
        if password is None or password == "":
            log.info("No api password found for wistia client - using dummy client")
            client_cls = DummyWistiaClient
        else:
            client_cls = WistiaClient

    return client_cls(api_password=password)
