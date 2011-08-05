#!/usr/bin/env python
# encoding: utf-8
import sys, os.path, logging, optparse
import urllib2, urllib

# simple CLI for wistia.
import wistia.api
try:
	import json
except:
	import simplejson as json

log = logging.getLogger('wistiapy')

DESC = "Wistia python-based command line client."

if len(sys.argv) < 2:
	sys.argv.append('-h')

parser = optparse.OptionParser(usage="wistia.py [options]",
		description=DESC)

parser.add_option("-c","--cred", dest="cred", help="your API key", 
		action="store")
parser.add_option("-p","--projects", dest="list_projects", 
		help="list all projects", action="store_true")

(options, args) = parser.parse_args()

if (options.cred is None):
	raise Exception('Please supply your credentials with -c KEY')

# list projects.
w = wistia.api.WistiaAPI("api", options.cred)
if (options.list_projects):
	projects_json = w.list_projects()
	projects = json.loads(projects_json)
	for p in projects:
		print "%s \"%s\" %s" % (p['id'], p['name'], p['mediaCount'])
	
# list all medias for a project.

# create an embed code for media.
