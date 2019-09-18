class Asset:
    """
    Wrapper for asset objects (embedded in Media objects) for results from
    the Wistia API
    """

    def __init__(self, dict):
        """
        A direct-access URL to the content of the asset.
        """
        self.url = dict["url"]
        """
        (optional) The width of this specific asset, if applicable.
        """
        self.width = dict["width"]
        """
        (optional) The height of this specific asset, if applicable.
        """
        self.height = dict["height"]
        """
        The size of the asset file that's referenced by url, measured in bytes.
        """
        self.fileSize = dict["fileSize"]
        """
        The asset's content type.
        """
        self.contentType = dict["contentType"]
        """
        The internal type of the asset, describing how the asset should be used.
        Valid values are "OriginalFile", "FlashVideoFile", "Mp4VideoFile",
        "IPhoneVideoFile", "StillImageFile", "SwfFile", "Mp3AudioFile",
        and "LargeImageFile"
        """
        self.type = dict["type"]
