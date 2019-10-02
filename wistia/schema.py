from schematics import types, models

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


class Asset(models.Model):
    """
    Wrapper for asset objects (embedded in Media objects) for results from
    the Wistia API
    """

    url = types.URLType(
        required=True,
        metadata=dict(description="A direct-access URL to the content of the asset"),
    )
    width = types.IntType(
        required=True,
        metadata=dict(
            description="(optional) The width of this specific asset, if applicable"
        ),
    )
    height = types.IntType(
        required=True,
        metadata=dict(
            description="(optional) The height of this specific asset, if applicable"
        ),
    )
    file_size = types.IntType(
        serialized_name="fileSize",
        required=True,
        metadata=dict(
            description="The size of the asset file that's referenced by url, measured in bytes"
        ),
    )
    content_type = types.StringType(
        serialized_name="contentType",
        required=True,
        metadata=dict(description="The asset's content type"),
    )
    type = types.StringType(
        required=True,
        metadata=dict(
            description="The internal type of the asset, describing how the asset should be used"
        ),
        choices=[
            "OriginalFile",
            "FlashVideoFile",
            "MdFlashVideoFile",
            "HdFlashVideoFile",
            "Mp4VideoFile",
            "MdMp4VideoFile",
            "HdMp4VideoFile",
            "HlsVideoFile",
            "IphoneVideoFile",
            "StoryboardFile",
            "StillImageFile",
            "SwfFile",
            "Mp3AudioFile",
            "LargeImageFile",
        ],
    )


class ProjectReference(models.Model):
    id = types.IntType(required=True, metadata=dict(description=""))
    name = types.StringType(required=True, metadata=dict(description=""))
    hashed_id = types.StringType(required=True, metadata=dict(description=""))


class Thumbnail(models.Model):
    url = types.URLType(required=True, metadata=dict(description=""))
    width = types.IntType(required=True, metadata=dict(description=""))
    height = types.IntType(required=True, metadata=dict(description=""))


class Media(models.Model):
    """ Wrapper for Wistia Media results """

    id = types.IntType(
        required=True,
        metadata=dict(
            description="A unique numeric identifier for the media within the system."
        ),
    )
    name = types.StringType(
        required=True, metadata=dict(description="The display name of the media.")
    )
    hashed_id = types.StringType(
        required=True,
        metadata=dict(description="A unique alphanumeric identifier for this media."),
    )
    description = types.StringType(
        required=True,
        metadata=dict(
            description=(
                "A description for the media which usually appears near the top of the"
                "sidebar on the media’s page"
            )
        ),
    )
    project = types.ModelType(
        ProjectReference,
        required=False,
        metadata=dict(
            description="Information about the project in which the media resides"
        ),
    )
    type = types.StringType(
        required=True,
        metadata=dict(description="A string representing what type of media this is"),
        choices=[
            "Video",
            "Image",
            "Audio",
            "Swf",
            "MicrosoftOfficeDocument",
            "PdfDocument",
            "UnknownType",
        ],
    )
    status = types.StringType(
        required=True,
        default="ready",
        metadata=dict(description="Post upload processing status"),
        choices=["queued", "processing", "ready", "failed"],
    )
    progress = types.FloatType(
        required=False,
        default=1.0,
        metadata=dict(
            description=(
                "(optional) After a file has been uploaded to Wistia, it needs to be"
                "processed before it is available for online viewing. This field is"
                "a floating point value between 0 and 1 that indicates the progress of"
                "that processing."
            )
        ),
    )
    section = types.StringType(
        required=False,
        serialize_when_none=False,
        metadata=dict(
            description=(
                "(optional) The title of the section in which the media appears."
                "This attribute is omitted if the media is not in a section (default)."
            )
        ),
    )
    thumbnail = types.ModelType(
        Thumbnail,
        required=True,
        metadata=dict(
            description="An object representing the thumbnail for this media"
        ),
    )
    duration = types.FloatType(
        required=False,
        metadata=dict(
            description=(
                "(optional) For Audio or Video files, this field specifies the length"
                "(in seconds). For Document files, this field specifies the number of"
                "pages in the document. For other types of media, or if the duration"
                "is unknown, this field is omitted."
            )
        ),
    )
    created = types.DateTimeType(
        required=True,
        serialized_format=DATETIME_FORMAT,
        metadata=dict(description="The date when the media was originally uploaded."),
    )
    updated = types.DateTimeType(
        required=True,
        serialized_format=DATETIME_FORMAT,
        metadata=dict(description="The date when the media was last changed."),
    )
    assets = types.ListType(
        types.ModelType(Asset),
        required=False,
        metadata=dict(description="An array of the assets available for this media"),
    )
    embed_code = types.StringType(
        serialized_name="embedCode",
        required=False,
        metadata=dict(
            description=r"""
            DEPRECATED
            The HTML code that would be used for embedding the media into a web page.
            Please note that in JSON format, all quotes are escaped with a
            backslash (\) character. In XML, angle brackets (< and >) and
            ampersands (&) are converted to their equivalent XML entities
            ("&lt;", "&gt;", and "&amp;" respectively) to prevent XML parser errors.
            """
        ),
    )

    # Undocumented "transcript" field
    # transcript = types.DictType(required=False)


class Project(models.Model):
    """Wrapper for project results."""

    id = types.IntType(
        required=True,
        metadata=dict(
            description="A unique numeric identifier for the project within the system."
        ),
    )
    name = types.StringType(
        required=True, metadata=dict(description="The project's display name.")
    )
    hashed_id = types.StringType(
        required=True,
        metadata=dict(
            description=(
                "A private hashed id, uniquely identifying the project within the"
                "system. Used for playlists and RSS feeds"
            )
        ),
    )
    media_count = types.IntType(
        required=True,
        default=0,
        serialized_name="mediaCount",
        metadata=dict(
            description="The number of different medias that have been uploaded to the project."
        ),
    )
    created = types.DateTimeType(
        required=True,
        serialized_format=DATETIME_FORMAT,
        metadata=dict(description="The date that the project was originally created."),
    )
    updated = types.DateTimeType(
        required=True,
        serialized_format=DATETIME_FORMAT,
        metadata=dict(description="The date that the project was last updated"),
    )
    anonymous_can_upload = types.BooleanType(
        required=True,
        serialized_name="anonymousCanUpload",
        metadata=dict(
            description=(
                "A boolean indicating whether or not anonymous uploads are enabled for the project"
            )
        ),
    )
    anonymous_can_download = types.BooleanType(
        required=True,
        serialized_name="anonymousCanDownload",
        metadata=dict(
            description=(
                "A boolean indicating whether or not anonymous downloads are enabled for this project"
            )
        ),
    )
    public = types.BooleanType(
        required=True,
        metadata=dict(
            description=(
                "A boolean indicating whether the project is available for public (anonymous) viewing"
            )
        ),
    )
    public_id = types.StringType(
        required=False,
        serialized_name="publicId",
        metadata=dict(
            description=(
                "If the project is public, this field contains a string representing the "
                "ID used for referencing the project in public URLs"
            )
        ),
    )
    medias = types.ListType(
        types.ModelType(Media),
        required=False,  # Not present in lists of Projects
        serialize_when_none=False,
        metadata=dict(description="A list of the media associated with a project"),
    )


class CaptionTrack(models.Model):
    language = types.StringType(
        required=True,
        metadata=dict(
            description="A 3 character language code as specified by ISO-639–2"
        ),
    )
    text = types.StringType(
        required=True,
        metadata=dict(
            description="The text of the captions for the specified language in SRT format"
        ),
    )
    english_name = types.StringType(
        required=True, metadata=dict(description="The English name of the language")
    )
    native_name = types.StringType(
        required=True, metadata=dict(description="The native name of the language")
    )
    is_draft = types.BooleanType(
        required=False, metadata=dict(description="Presumably for internal use only")
    )
