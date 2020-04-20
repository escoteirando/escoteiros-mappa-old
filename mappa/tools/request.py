import json
from time import sleep, time

import requests

from cache_gs import CacheGS
from cache_gs.utils.logging import get_logger
from mappa.tools.http_response import HTTPResponse


class HTTP:
    OK = 200
    UNAUTHORIZED = 401
    SERVER_ERROR = 500

    def __init__(self, cache: CacheGS, gzipped: bool = False):
        self._url = "http://mappa.escoteiros.org.br"
        self._authorization = None
        self.logger = get_logger()
        self._cache = cache
        self._gzipped = gzipped
        if not cache:
            raise ValueError('cache not informed')

    def set_authorization(self, authorization: str, valid_until: int):
        self._authorization = authorization
        self._auth_valid_until = valid_until

    def auth_header(self):
        header = {
            "authorization": self._authorization,
            "User-Agent": "okhttp/3.4.1"
        }
        if self._gzipped:
            header["Accept-Encoding"] = "gzip"
        return header

    def get(self, url: str, params: dict = None, description: str = None, no_cache: bool = False, max_age: int = 172800) -> HTTPResponse:
        ''' HTTP GET

        :param url:
        :param params:
        :param description:
        :param no_cache:
        :param max_age:

        :return: tuple (http_code, content)
        '''
        description = url if not description else description
        if not self._authorization:
            return HTTP.UNAUTHORIZED, 'UNAUTHORIZED'

        cache_key = url + str(self._authorization)
        if not no_cache:
            cached = self._cache.get_value('mappa', cache_key, None)
            if cached:
                return HTTPResponse(HTTP.OK, cached)

        count = 0
        exceptions = []
        http_code = 0

        while count < 5 and not http_code:
            count += 1
            try:
                ret = requests.get(
                    self._url+url, json=params, headers=self.auth_header())
                if ret.status_code == HTTP.OK:
                    content = ret.content.decode('utf-8')
                    self._cache.set_value(
                        section='mappa',
                        key=cache_key,
                        value=content,
                        ttl=max_age)

                    http_code = HTTP.OK
                    content = json.loads(content)
                else:
                    http_code = ret.status_code
                    content = json.loads(ret.text)
            except Exception as e:
                if str(e) not in exceptions:
                    exceptions.append(str(e))
                if count < 5:
                    sleep(1)
                else:
                    http_code = HTTP.SERVER_ERROR
                    content = exceptions[0]

        return HTTPResponse(http_code, content)

    def post(self, url: str, params: dict) -> HTTPResponse:
        """ Send POST request to MAPPA API.

        :param url: url path (p.ex '/login')
        :param params: json body
        :returns: (status_code, dict/str)
        """
        try:
            _headers = {
                "User-Agent": "okhttp/3.4.1"
            }
            ret = requests.post(self._url+url, json=params, headers=_headers)
            if ret.status_code == HTTP.OK:
                return HTTPResponse(ret.status_code, json.loads(ret.content))
            else:
                return HTTPResponse(ret.status_code, ret.text)
        except Exception as e:
            return HTTPResponse(HTTP.SERVER_ERROR, str(e))
