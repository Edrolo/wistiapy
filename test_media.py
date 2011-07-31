import logging
import wistia.media 

try:
	import json
except:
	import simplejson as json

log = logging.getLogger("test_wistia")

"""
Laad the JSON.
"""
json_string = open('test_media.json').read()
"""
Create the Asset.
"""
md = wistia.media.MediasDecoder()
medias = md.decode(json_string)
print medias
print medias[0].assets
"""
Make sure all the fields are set.
"""
