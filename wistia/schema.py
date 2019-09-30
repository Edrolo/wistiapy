import typesystem


class Asset(typesystem.Schema):
    """
    Wrapper for asset objects (embedded in Media objects) for results from
    the Wistia API
    """

    url = typesystem.String(
        format="url", description="A direct-access URL to the content of the asset"
    )
    width = typesystem.Integer(
        description="(optional) The width of this specific asset, if applicable"
    )
    height = typesystem.Integer(
        description="(optional) The height of this specific asset, if applicable"
    )
    file_size = typesystem.Integer(
        description="The size of the asset file that's referenced by url, measured in bytes"
    )
    content_type = typesystem.String(description="The asset's content type")
    type = typesystem.Choice(
        description="The internal type of the asset, describing how the asset should be used",
        choices=[
            "OriginalFile",
            "FlashVideoFile",
            "MdFlashVideoFile",
            "HdFlashVideoFile",
            "Mp4VideoFile",
            "MdMp4VideoFile",
            "HdMp4VideoFile",
            "IPhoneVideoFile",
            "StillImageFile",
            "SwfFile",
            "Mp3AudioFile",
            "LargeImageFile",
        ],
    )


class ProjectReference(typesystem.Schema):
    id = typesystem.Integer(description="")
    name = typesystem.String(description="")
    hashed_id = typesystem.String(description="")


class Thumbnail(typesystem.Schema):
    url = typesystem.String(format="url", description="")
    width = typesystem.Integer(description="")
    height = typesystem.Integer(description="")


class Media(typesystem.Schema):
    """ Wrapper for Wistia Media results """

    id = typesystem.Integer(
        description="A unique numeric identifier for the media within the system."
    )
    name = typesystem.String(description="The display name of the media.")
    hashed_id = typesystem.String(
        description="A unique alphanumeric identifier for this media."
    )
    description = typesystem.String(
        description=(
            "A description for the media which usually appears near the top of the"
            "sidebar on the media’s page"
        )
    )
    project = typesystem.Reference(
        to=ProjectReference,
        allow_null=True,
        description="Information about the project in which the media resides",
    )
    type = typesystem.Choice(
        description="A string representing what type of media this is",
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
    status = typesystem.Choice(
        description="Post upload processing status",
        choices=["queued", "processing", "ready", "failed"],
    )
    progress = typesystem.Float(
        description=(
            "(optional) After a file has been uploaded to Wistia, it needs to be"
            "processed before it is available for online viewing. This field is"
            "a floating point value between 0 and 1 that indicates the progress of"
            "that processing."
        )
    )
    section = typesystem.String(
        allow_null=True,
        description=(
            "(optional) The title of the section in which the media appears."
            "This attribute is omitted if the media is not in a section (default)."
        )
    )
    thumbnail = typesystem.Reference(
        to=Thumbnail, description="An object representing the thumbnail for this media"
    )
    duration = typesystem.Float(
        description=(
            "(optional) For Audio or Video files, this field specifies the length"
            "(in seconds). For Document files, this field specifies the number of"
            "pages in the document. For other types of media, or if the duration"
            "is unknown, this field is omitted."
        )
    )
    created = typesystem.DateTime(
        description="The date when the media was originally uploaded."
    )
    updated = typesystem.DateTime(
        description="The date when the media was last changed."
    )
    assets = typesystem.Array(
        items=typesystem.Reference(to=Asset),
        description="An array of the assets available for this media",
    )
    embed_code = typesystem.String(
        allow_null=True,
        description=r"""
            DEPRECATED
            The HTML code that would be used for embedding the media into a web page.
            Please note that in JSON format, all quotes are escaped with a
            backslash (\) character. In XML, angle brackets (< and >) and
            ampersands (&) are converted to their equivalent XML entities
            ("&lt;", "&gt;", and "&amp;" respectively) to prevent XML parser errors.
        """
    )


class Project(typesystem.Schema):
    """Wrapper for project results."""

    id = typesystem.Integer(
        description="A unique numeric identifier for the project within the system."
    )
    name = typesystem.String(description="The project's display name.")
    hashed_id = typesystem.String(
        description=(
            "A private hashed id, uniquely identifying the project within the"
            "system. Used for playlists and RSS feeds"
        )
    )
    media_count = typesystem.Integer(
        description="The number of different medias that have been uploaded to the project."
    )
    created = typesystem.DateTime(
        description="The date that the project was originally created."
    )
    updated = typesystem.DateTime(
        description="The date that the project was last updated"
    )
    anonymous_can_upload = typesystem.Boolean(
        description=(
            "A boolean indicating whether or not anonymous uploads are enabled for the project"
        )
    )
    anonymous_can_download = typesystem.Boolean(
        description=(
            "A boolean indicating whether or not anonymous downloads are enabled for this project"
        )
    )
    public = typesystem.Boolean(
        description=(
            "A boolean indicating whether the project is available for public (anonymous) viewing"
        )
    )
    public_id = typesystem.String(
        description=(
            "If the project is public, this field contains a string representing the "
            "ID used for referencing the project in public URLs"
        )
    )
    medias = typesystem.Array(
        items=typesystem.Reference(to=Media),
        description="A list of the media associated with a project",
    )


class CaptionTrack(typesystem.Schema):
    language = typesystem.String(
        description="A 3 character language code as specified by ISO-639–2"
    )
    text = typesystem.String(
        description="The text of the captions for the specified language in SRT format"
    )
    english_name = typesystem.String(description="The English name of the language")
    native_name = typesystem.String(description="The native name of the language")
    is_draft = typesystem.Boolean(description="Presumably for internal use only")
