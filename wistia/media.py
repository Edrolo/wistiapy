from . import asset


class Media:
    """
    Wrapper for Wistia Media results. Because Dicts are cool, but so are data
    attributes. right?
    """

    def __init__(self, media_dict):
        """
        A unique numeric identifier for the media within the system.
        """
        self.id = media_dict["id"]
        """
        The display name of the media.
        """
        self.name = media_dict["name"]
        """
        An object representing information about the project in which the media
        resides. It has 2 fields: the numeric id of the project, and the name
        of the project.
        """
        self.project = media_dict["project"]
        """
        A string representing what type of media this is. Valid values are "Video",
        "Image", "Audio", "Swf", "MicrosoftOfficeDocument", "PdfDocument", or
        "UnknownType".
        """
        self.type = media_dict["type"]
        """
        (optional) After a file has been uploaded to Wistia, it needs to be
        processed before it is available for online viewing. This field is
        a floating point value between 0 and 1 that indicates the progress of
        that processing.
        """
        self.progress = media_dict["progress"]
        """
        (optional) The title of the section in which the media appears.
        This attribute is omitted if the media is not in a section (default).
        """
        self.section = media_dict.get("section")
        """
        An object representing the thumbnail for this media. The attributes are
        URL, width, and height.
        """
        self.thumbnail = media_dict["thumbnail"]
        """
        (optional) For Audio or Video files, this field specifies the length
        (in seconds). For Document files, this field specifies the number of
        pages in the document. For other types of media, or if the duration
        is unknown, this field is omitted.
        """
        self.duration = media_dict["duration"]
        """
        The date when the media was originally uploaded.
        """
        self.created = media_dict["created"]
        """
        The date when the media was last changed.
        """
        self.updated = media_dict["updated"]
        """
        An array of the assets available for this media. See the table below
        for a description the fields in each asset object.
        """
        self.assets = [asset.Asset(asset_dict) for asset_dict in media_dict["assets"]]

        """
        The HTML code that would be used for embedding the media into a web page.
        Please note that in JSON format, all quotes are escaped with a
        backslash (\\) character. In XML, angle brackets (< and >) and
        ampersands (&) are converted to their equivalent XML entities
        ("&lt;", "&gt;", and "&amp;" respectively) to prevent XML parser errors.
        """
        self.embedCode = media_dict["embedCode"]
