import logging
from . import media

try:
	import json
except ImportError:
	import simplejson as json


class Project:
	"""
	Wrapper for project results.
	"""
	def __init__(self, project_dict):
		"""
		A unique numeric identifier for the project within the system.
		"""
		self.id = project_dict['id']
		"""
		The project's display name.
		"""
		self.name = project_dict['name']
		"""
		The number of different medias that have been uploaded to the project. 
		"""
		self.mediaCount = project_dict['mediaCount']
		"""
		The date that the project was originally created.
		"""
		self.created = project_dict['created']
		"""
		The date that the project was last updated
		"""
		self.updated = project_dict['updated']
		"""
		A private hashed id, uniquely identifying the project within the 
		system. Used for playlists and RSS feeds.
		"""
		self.hashedId = project_dict['hashedId']
		"""
		A boolean indicating whether or not anonymous uploads are enabled for the 
		project.
		"""
		self.anonymousCanUpload = project_dict['anonymousCanUpload']
		"""
		A boolean indicating whether or not anonymous downloads are enabled for 
		this project.
		"""
		self.anonymousCanDownload = project_dict['anonymousCanDownload']
		"""
		A boolean indicating whether the project is available for public 
		(anonymous) viewing.
		"""
		self.public = project_dict['public']
		"""
		If the project is public, this field contains a string representing the 
		ID used for referencing the project in public URLs.
		"""
		self.publicId = project_dict['publicId']
		"""
		In the project show, you can get a list of the media associated with
		a project.
		"""
		self.medias = []
		if ("medias" in project_dict):
			for m in project_dict['medias']:
				self.medias.append(media.Media(m))


class ProjectsDecoder(json.JSONDecoder):
	"""
	Creates Projects from a json document.
	"""
	def decode(self, json_string):
		"""
		parse the json, return a list of projects.
		"""
		projects_dict = json.loads(json_string)
		projects = []
		for project in projects_dict:
			projects.append(Project(project))
		return projects


class ProjectDecoder(json.JSONDecoder):
	"""
	creates a single Project from a json document.
	"""
	def decode(self, json_string):
		project_dict = json.loads(json_string)
		project = Project(project_dict)
		return project
