import os
from datetime import datetime
from json import dumps, loads

from mappa.tools.request import HTTP, HTTPResponse


class MockHTTP(HTTP):

    def __init__(self, cache, gzipped=False):
        self._posts = {
            "/api/escotistas/login": {
                "id": "pJdEEYXocGxXFUHysRFh55oe60zAak50gS4U69kXRFN7atgOBgGEl1nhwY4yyoAO",
                "ttl": 1209600,
                "created": datetime.utcnow().isoformat(),
                "userId": 50442
            }
        }
        file_mocks = os.path.join('tests', 'mocks', 'request_mocks.json')
        if not os.path.isfile(file_mocks):
            raise FileNotFoundError(file_mocks)

        with open(file_mocks) as f:
            self._gets = loads(f.read())

        super().__init__(cache, gzipped=gzipped)

    def get(self, url: str, params: dict = None, description: str = None, no_cache: bool = False, max_age: int = 172800) -> HTTPResponse:
        return HTTPResponse(200, self._gets[url])

    def post(self, url: str, params: dict) -> HTTPResponse:
        return HTTPResponse(200, self._posts[url])
