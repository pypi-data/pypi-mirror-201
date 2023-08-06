from typing import Callable, Optional
import requests


class HTTPSession(object):
    def __init__(self, base_path, common_headers):
        self.base_path = base_path
        self.common_headers = common_headers

    def __getattr__(self, item: str) -> Callable[[str, Optional[dict], Optional[dict]], dict]:
        request_method = getattr(requests, item.lower())

        def modal(location: str, body: dict = None, headers: dict = None) -> dict:
            args = dict()
            args["url"] = self.base_path + location
            if body is not None:
                args["json"] = body
            if headers is None:
                headers = dict()
            args["headers"] = {**self.common_headers, **headers}

            return request_method(**args).json()

        return modal
