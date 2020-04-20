class HTTPResponse:

    def __init__(self, status_code: int, content):
        self._status_code = status_code
        self._content = content

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def content(self):
        return self._content

    @property
    def is_ok(self) -> bool:
        return self._status_code < 300

    @staticmethod
    def from_dict(dict_response: dict):
        if isinstance(dict_response, dict) and \
            'status_code' in dict_response and \
                'content' in dict_response:
            return HTTPResponse(dict_response['status_code'], dict_response['content'])

        return None
