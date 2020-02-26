import falcon

from api.config import STATUS_ENDPOINT
from api.exceptions import StatusNotFoundError
from api.logic import ApiLogic


class LogicDependentResource:
    def __init__(self, logic: ApiLogic):
        self._logic = logic


class SequenceResource(LogicDependentResource):
    def on_get(self, _req, resp, length):
        if length < 1:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = {
                "message": "Fibonacci sequence length must be positive integer",
            }
            return
        dto = self._logic.get_sequence_with_status(length)
        if dto.sequence:
            resp.status = falcon.HTTP_OK
            resp.body = {
                "sequence": dto.sequence,
            }
        else:
            resp.status = falcon.HTTP_ACCEPTED
            resp.body = {
                "sequence": None,
                "statusUri": STATUS_ENDPOINT.format(length),
                "estimatedTime": str(dto.status.eta),
            }


class StatusResource(LogicDependentResource):
    def on_get(self, _req, resp, length):
        if length < 1:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = {
                "message": "Fibonacci sequence length must be positive integer",
            }
            return
        try:
            status = self._logic.get_request_status(length)
            resp.status = falcon.HTTP_OK
            resp.body = {
                "estimatedTime": str(status.eta),
                "numbersCalculated": status.calculated_numbers,
                "numbersRequired": status.length,
            }
        except StatusNotFoundError:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.body = {
                "message": f"Calculation for {length} wasn't requested yet",
            }
