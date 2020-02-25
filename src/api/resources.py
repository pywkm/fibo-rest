from datetime import datetime


class RestResource:
    @staticmethod
    def on_get(_req, resp):
        resp.body = {
            "result": "It works!",
            "timestamp": str(datetime.utcnow()),
        }
