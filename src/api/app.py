import falcon

from api.config import SEQUENCE_ENDPOINT, STATUS_ENDPOINT
from api.logic import ApiLogic
from api.middlewares import ContentEncodingMiddleware
from api.resources import SequenceResource, StatusResource
from api.storage.abstract import Storage
from api.storage.memory import MemoryStorage


def create_app(storage: Storage) -> falcon.API:
    app = falcon.API(middleware=[ContentEncodingMiddleware()])
    logic = ApiLogic(storage)

    app.add_route(SEQUENCE_ENDPOINT.format("{length:int}"), SequenceResource(logic))
    app.add_route(STATUS_ENDPOINT.format("{length:int}"), StatusResource(logic))

    return app


def get_app():
    storage = MemoryStorage({0: 0, 1: 1, 2: 1, 3: 2, 4: 3, 5: 5})
    return create_app(storage)
