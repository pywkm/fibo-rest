import falcon

from api.exceptions import StatusNotFoundError
from api.logic import ApiLogic
from config import STATUS_ENDPOINT


class LogicDependentResource:
    def __init__(self, logic: ApiLogic):
        self._logic = logic


class SequenceResource(LogicDependentResource):
    def on_get(self, _req: falcon.Request, resp: falcon.Response, length: int) -> None:
        if length < 1 or length > self._logic.longest_sequence:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = {
                "message": (
                    "Fibonacci sequence length must be positive integer, "
                    f"but not bigger than {self._logic.longest_sequence}"
                ),
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
                "eta": str(dto.status.eta),  # type: ignore  # thinks status is None
            }


class StatusResource(LogicDependentResource):
    def on_get(self, _req: falcon.Request, resp: falcon.Response, length: int) -> None:
        if length < 1 or length > self._logic.longest_sequence:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = {
                "message": (
                    "Fibonacci sequence length must be positive integer, "
                    f"but not bigger than {self._logic.longest_sequence}"
                ),
            }
            return
        try:
            status = self._logic.get_request_status(length)
            resp.status = falcon.HTTP_OK
            resp.body = {
                "eta": str(status.eta),
                "numbersCalculated": status.calculated_numbers,
                "numbersRequired": status.length,
            }
        except StatusNotFoundError:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.body = {
                "message": f"Calculation for sequence:{length} wasn't requested yet",
            }
