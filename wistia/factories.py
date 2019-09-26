import random
from datetime import datetime

import factory.fuzzy
import factory
from wistia import schema


class AssetFactory(factory.Factory):
    class Meta:
        model = schema.Asset

    """ "Mp4VideoFile", "MdMp4VideoFile, "HdMp4VideoFile", 
    """

    url = ""
    width = "640"
    height = "360"
    file_size = "123456"
    content_type = "video/mp4"
    type = "Mp4VideoFile"
    embed_code = ""

    class Params:
        size = "small"  # or "medium" or "large"


class ThumbnailFactory(factory.Factory):
    class Meta:
        model = schema.Thumbnail

    url = factory.Faker("image_url")
    width = factory.Faker("pyint", min_value=100, max_value=1000)
    height = factory.Faker("pyint", min_value=100, max_value=1000)


class MediaFactory(factory.Factory):
    class Meta:
        model = schema.Media

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("sentence", nb_words=5, locale="en_US")
    project = ""

    type = factory.fuzzy.FuzzyChoice(
        [
            "Video",
            "Image",
            "Audio",
            "Swf",
            "MicrosoftOfficeDocument",
            "PdfDocument",
            "UnknownType",
        ]
    )
    progress = 1
    section = None
    thumbnail = factory.SubFactory(ThumbnailFactory)
    duration = factory.Faker("pyint", min_value=5, max_value=1000)
    created = factory.LazyFunction(datetime.now)
    updated = factory.LazyFunction(datetime.now)
    assets = factory.RelatedFactoryList(AssetFactory, size=lambda: random.randint(1, 6))


class ProjectFactory(factory.Factory):
    class Meta:
        model = schema.Project

    id = ""
    name = ""
    media_count = ""
    created = ""
    updated = ""
    hashed_id = ""
    anonymous_can_upload = ""
    anonymous_can_download = ""
    public = ""
    public_id = ""
    medias = ""


class CaptionTrackFactory(factory.Factory):
    class Meta:
        model = schema.CaptionTrack

    language = ""
    text = ""
    english_name = ""
    native_name = ""
    is_draft = ""
