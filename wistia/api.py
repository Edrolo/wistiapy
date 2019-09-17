import logging
import urllib.parse
import urllib.request

from . import media

API_BASE_URL = "https://api.wistia.com/v1/"

try:
    import json
except ImportError:
    import simplejson as json

log = logging.getLogger('wistiapy')


class WistiaAPI:
    def __init__(self, user, api_password):
        self.user = user
        self.api_password = api_password

        pm = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        # this creates a password manager
        pm.add_password(None, API_BASE_URL, self.user, self.api_password)
        # because we have put None at the start it will always
        # use this username/password combination for  urls
        # for which `theurl` is a super-url

        authhandler = urllib.request.HTTPBasicAuthHandler(pm)
        # create the AuthHandler

        opener = urllib.request.build_opener(authhandler)

        urllib.request.install_opener(opener)

    def call(self, rel_path, params):
        """
        Handles making HTTP request. Returns parsed JSON.

        Requests will be sent to:
        BASE_API_PATH/rel_path

        Parameters for queries are sent on the query string.

        I'd imagine this will change once/if I implement some of the upload
        features.
        """
        data = urllib.parse.urlencode(params)
        # build the request URL.
        url = self.build_get_url(API_BASE_URL, rel_path, data)
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        json_string = resp.read()

        return json_string

    def build_get_url(self, base_path, rel_path, data):
        """
        Build a URL for queries. For query requests, parameters are sent in the
        query string and not in the POST.
        """
        url = API_BASE_URL
        url += rel_path
        if data is not None:
            url += "?"
            url += data
        return url

    def list_medias(self, sort_by="name", sort_direction=1, page=1,
                    per_page=100, project_id=None, name=None, type=None):
        # convert to parameter dict.
        params = {}
        params['sort_by'] = sort_by
        params['sort_direction'] = sort_direction
        params['page'] = page
        params['per_page'] = per_page
        if project_id is not None:
            params['project_id'] = project_id
        if name is not None:
            params['name'] = name
        if type is not None:
            params['type'] = type

        # call the API.
        json_string = self.call('medias.json', params)

        # return a List of media.
        return media.MediasDecoder().decode(json_string)
