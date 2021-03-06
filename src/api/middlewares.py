import json
from typing import Any

import falcon


class JSONEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:  # pylint: disable=method-hidden,arguments-differ
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        return super().default(obj)


class ContentEncodingMiddleware:
    def process_response(
        self, req: falcon.Request, resp: falcon.Response, _resource: Any, req_succeeded: bool
    ) -> None:
        if not req_succeeded:
            return
        if req.client_accepts_json:
            resp.set_header("Content-Type", "application/json")
            resp.body = json.dumps(resp.body, cls=JSONEncoder)
