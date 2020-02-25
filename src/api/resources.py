import falcon
from api.exceptions import StatusNotFoundError
from api.storage.abstract import Storage


class SequenceResource:
    def __init__(self, storage: Storage):
        self._storage = storage

    def on_get(self, _req, resp, length):
        sequence = self._storage.get_sequence(length)
        if sequence:
            resp.status = falcon.HTTP_OK
            resp.body = sequence
        else:
            status = self._storage.get_status(length)
            resp.status = falcon.HTTP_ACCEPTED
            resp.body = {
                "statusUri": f"/api/fibo/{length}/status",
                "estimatedTime": str(status.eta),
            }


class StatusResource:
    def __init__(self, storage: Storage):
        self._storage = storage

    def on_get(self, _req, resp, length):
        try:
            status = self._storage.get_status(length)
            resp.status = falcon.HTTP_OK
            resp.body = {
                "estimatedTime": str(status.eta),
                "numbersCalculated": 15,
                "numbersRequired": status.length,
            }
        except StatusNotFoundError:
            raise falcon.HTTPNotFound()
