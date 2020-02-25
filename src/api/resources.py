import falcon
from api.exceptions import StatusNotFoundError
from api.logic import ApiLogic


class SequenceResource:
    def __init__(self, logic: ApiLogic):
        self._logic = logic

    def on_get(self, _req, resp, length):
        sequence, status = self._logic.get_sequence(length)
        if sequence:
            resp.status = falcon.HTTP_OK
            resp.body = sequence
        else:
            resp.status = falcon.HTTP_ACCEPTED
            resp.body = {
                "statusUri": f"/api/fibo/{length}/status",
                "estimatedTime": str(status.eta),
            }


class StatusResource:
    def __init__(self, logic: ApiLogic):
        self._logic = logic

    def on_get(self, _req, resp, length):
        try:
            status = self._logic.get_status(length)
            resp.status = falcon.HTTP_OK
            resp.body = {
                "estimatedTime": str(status.eta),
                "numbersCalculated": 15,
                "numbersRequired": status.length,
            }
        except StatusNotFoundError:
            raise falcon.HTTPNotFound()
