import falcon
from api.config import STATUS_ENDPOINT
from api.exceptions import StatusNotFoundError
from api.logic import ApiLogic


class LogicDependentResource:
    def __init__(self, logic: ApiLogic):
        self._logic = logic


class SequenceResource(LogicDependentResource):
    def on_get(self, _req, resp, length):
        sequence, status = self._logic.get_sequence_status(length)
        if sequence:
            resp.status = falcon.HTTP_OK
            resp.body = {
                "sequence": sequence,
            }
        else:
            resp.status = falcon.HTTP_ACCEPTED
            resp.body = {
                "sequence": None,
                "statusUri": STATUS_ENDPOINT.format(length),
                "estimatedTime": str(status.eta),
            }


class StatusResource(LogicDependentResource):
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
            resp.status = falcon.HTTP_NOT_FOUND
            resp.body = {
                "message": f"Calculation for {length} wasn't requested yet",
            }
