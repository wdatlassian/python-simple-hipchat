from urllib.parse import urljoin
from urllib.parse import urlencode
import urllib.request, urllib.error, urllib.parse
import json


API_URL_DEFAULT = 'https://api.hipchat.com/v1/'
FORMAT_DEFAULT = 'json'


class HipChat(object):
    def __init__(self, token=None, url=API_URL_DEFAULT, format=FORMAT_DEFAULT):
        self.url = url
        self.token = token
        self.format = format
        self.opener = urllib.request.build_opener(urllib.request.HTTPSHandler())

    class RequestWithMethod(urllib.request.Request):
        def __init__(self, url, data=None, headers={}, origin_req_host=None, unverifiable=False, http_method=None):
            urllib.request.Request.__init__(self, url, data, headers, origin_req_host, unverifiable)
            if http_method:
                self.method = http_method

        def get_method(self):
            if self.method:
                return self.method
            return urllib.request.Request.get_method(self)

    def method(self, url, method="GET", parameters=None, timeout=None):
        method_url = urljoin(self.url, url)

        if method == "GET":
            if not parameters:
                parameters = dict()

            parameters['format'] = self.format
            parameters['auth_token'] = self.token

            query_string = urlencode(parameters)
            request_data = None
        else:
            query_parameters = dict()
            query_parameters['auth_token'] = self.token

            query_string = urlencode(query_parameters)

            if parameters:
                request_data = urlencode(parameters)
            else:
                request_data = None

        method_url = method_url + '?' + query_string

        if method == "POST":
            req = self.RequestWithMethod(method_url, http_method=method, data=request_data.encode('utf-8'))
        if method == "GET":
            req = self.RequestWithMethod(method_url, http_method=method, data=request_data)
        response = self.opener.open(req, None, timeout).read()

        return json.loads(response.decode('utf-8'))

    def list_rooms(self):
        return self.method('rooms/list')

    def message_room(self, room_id='', message_from='', message='', message_format='text', color='', notify=False):
        parameters = dict()
        parameters['room_id'] = room_id
        parameters['from'] = message_from[:15]
        parameters['message'] = message
        parameters['message_format'] = message_format
        parameters['color'] = color

        if notify:
            parameters['notify'] = 1
        else:
            parameters['notify'] = 0

        return self.method('rooms/message', 'POST', parameters)
