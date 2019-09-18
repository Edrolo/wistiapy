from . import media


class Project:
    """
    Wrapper for project results.
    """

    def __init__(self, project_dict):
        """
        A unique numeric identifier for the project within the system.
        """
        self.id = project_dict["id"]
        """
        The project's display name.
        """
        self.name = project_dict["name"]
        """
        The number of different medias that have been uploaded to the project.
        """
        self.mediaCount = project_dict["mediaCount"]
        """
        The date that the project was originally created.
        """
        self.created = project_dict["created"]
        """
        The date that the project was last updated
        """
        self.updated = project_dict["updated"]
        """
        A private hashed id, uniquely identifying the project within the
        system. Used for playlists and RSS feeds.
        """
        self.hashedId = project_dict["hashedId"]
        """
        A boolean indicating whether or not anonymous uploads are enabled for the
        project.
        """
        self.anonymousCanUpload = project_dict["anonymousCanUpload"]
        """
        A boolean indicating whether or not anonymous downloads are enabled for
        this project.
        """
        self.anonymousCanDownload = project_dict["anonymousCanDownload"]
        """
        A boolean indicating whether the project is available for public
        (anonymous) viewing.
        """
        self.public = project_dict["public"]
        """
        If the project is public, this field contains a string representing the
        ID used for referencing the project in public URLs.
        """
        self.publicId = project_dict["publicId"]
        """
        In the project show, you can get a list of the media associated with
        a project.
        """
        self.medias = [media.Media(m) for m in project_dict.get("medias", [])]
