class Asset:
    """
    Wrapper for asset objects (embedded in Media objects) for results from
    the Wistia API
    """

    def __init__(self, dict):
        """A direct-access URL to the content of the asset."""
        self.url = dict["url"]
        """(optional) The width of this specific asset, if applicable."""
        self.width = dict["width"]
        """(optional) The height of this specific asset, if applicable."""
        self.height = dict["height"]
        """The size of the asset file that's referenced by url, measured in bytes."""
        self.file_size = dict["fileSize"]
        """The asset's content type."""
        self.content_type = dict["contentType"]
        """
        The internal type of the asset, describing how the asset should be used.
        Valid values are "OriginalFile", 
        "FlashVideoFile", "MdFlashVideoFile", "HdFlashVideoFile", 
        "Mp4VideoFile", "MdMp4VideoFile, "HdMp4VideoFile", 
        "IPhoneVideoFile", "StillImageFile", "SwfFile", 
        "Mp3AudioFile", and "LargeImageFile".
        """
        self.type = dict["type"]


class Media:
    """
    Wrapper for Wistia Media results. Because Dicts are cool, but so are data
    attributes. right?
    """

    def __init__(self, media_dict):
        """A unique numeric identifier for the media within the system."""
        self.id = media_dict["id"]
        """The display name of the media."""
        self.name = media_dict["name"]
        """A unique alphanumeric identifier for this media."""
        self.hashed_id = media_dict["hashed_id"]
        """	
        A description for the media which usually appears near the top of the
        sidebar on the media’s page.
        """
        self.description = media_dict["description"]
        """
        An object representing information about the project in which the media
        resides. It has 2 fields: the numeric id of the project, and the name
        of the project.
        """
        project = media_dict.get("project")
        self.project = ProjectReference(project) if project else None
        """
        A string representing what type of media this is. Valid values are "Video",
        "Image", "Audio", "Swf", "MicrosoftOfficeDocument", "PdfDocument", or
        "UnknownType".
        """
        self.type = media_dict["type"]
        """
        Post upload processing status. There are four statuses: 
        "queued", "processing", "ready", and "failed".
        """
        self.status = media_dict.get("status", "ready")
        """
        (optional) After a file has been uploaded to Wistia, it needs to be
        processed before it is available for online viewing. This field is
        a floating point value between 0 and 1 that indicates the progress of
        that processing.
        """
        self.progress = media_dict.get("progress", 1.0)
        """
        (optional) The title of the section in which the media appears.
        This attribute is omitted if the media is not in a section (default).
        """
        self.section = media_dict.get("section")
        """
        An object representing the thumbnail for this media.
        """
        self.thumbnail = Thumbnail(media_dict["thumbnail"])
        """
        (optional) For Audio or Video files, this field specifies the length
        (in seconds). For Document files, this field specifies the number of
        pages in the document. For other types of media, or if the duration
        is unknown, this field is omitted.
        """
        self.duration = media_dict["duration"]
        """The date when the media was originally uploaded."""
        self.created = media_dict["created"]
        """The date when the media was last changed."""
        self.updated = media_dict["updated"]
        """
        An array of the assets available for this media. See the table below
        for a description the fields in each asset object.
        """
        self.assets = [Asset(asset_dict) for asset_dict in media_dict["assets"]]
        r"""
        DEPRECATED
        The HTML code that would be used for embedding the media into a web page.
        Please note that in JSON format, all quotes are escaped with a
        backslash (\) character. In XML, angle brackets (< and >) and
        ampersands (&) are converted to their equivalent XML entities
        ("&lt;", "&gt;", and "&amp;" respectively) to prevent XML parser errors.
        """
        self.embed_code = media_dict["embedCode"]


class Thumbnail:
    def __init__(self, thumbnail_dict):
        self.url = thumbnail_dict["url"]
        self.width = thumbnail_dict["width"]
        self.height = thumbnail_dict["height"]


class ProjectReference:
    def __init__(self, project_reference_dict):
        self.id = project_reference_dict["id"]
        self.name = project_reference_dict["name"]
        self.hashed_id = project_reference_dict["hashed_id"]


class Project:
    """Wrapper for project results."""

    def __init__(self, project_dict):
        """A unique numeric identifier for the project within the system."""
        self.id = project_dict["id"]
        """The project's display name."""
        self.name = project_dict["name"]
        """The number of different medias that have been uploaded to the project."""
        self.media_count = project_dict["mediaCount"]
        """The date that the project was originally created."""
        self.created = project_dict["created"]
        """The date that the project was last updated"""
        self.updated = project_dict["updated"]
        """
        A private hashed id, uniquely identifying the project within the
        system. Used for playlists and RSS feeds.
        """
        self.hashed_id = project_dict["hashedId"]
        """
        A boolean indicating whether or not anonymous uploads are enabled for the
        project.
        """
        self.anonymous_can_upload = project_dict["anonymousCanUpload"]
        """
        A boolean indicating whether or not anonymous downloads are enabled for
        this project.
        """
        self.anonymous_can_download = project_dict["anonymousCanDownload"]
        """
        A boolean indicating whether the project is available for public
        (anonymous) viewing.
        """
        self.public = project_dict["public"]
        """
        If the project is public, this field contains a string representing the
        ID used for referencing the project in public URLs.
        """
        self.public_id = project_dict["publicId"]
        """
        In the project show, you can get a list of the media associated with
        a project.
        """
        self.medias = [Media(m) for m in project_dict.get("medias", [])]


class CaptionTrack:
    def __init__(self, captions_dict):

        """A 3 character language code as specified by ISO-639–2."""
        self.language: str = captions_dict["language"]
        """The text of the captions for the specified language in SRT format."""
        self.text: str = captions_dict["text"]
        """The English name of the language"""
        self.english_name: str = captions_dict["text"]
        """The native name of the language"""
        self.native_name: str = captions_dict["native_name"]
        """Presumably for internal use only"""
        self.is_draft: bool = captions_dict["is_draft"]
