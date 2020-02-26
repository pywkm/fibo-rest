import falcon

from api.config import SEQUENCE_ENDPOINT, STATUS_ENDPOINT
from api.logic import ApiLogic
from api.messaging import Broker, RabbitMqBroker
from api.middlewares import ContentEncodingMiddleware
from api.resources import SequenceResource, StatusResource
from api.storage.abstract import Storage
from api.storage.db import DbStorage


def create_app(storage: Storage, broker: Broker) -> falcon.API:
    app = falcon.API(middleware=[ContentEncodingMiddleware()])
    logic = ApiLogic(storage, broker)

    app.add_route(SEQUENCE_ENDPOINT.format("{length:int}"), SequenceResource(logic))
    app.add_route(STATUS_ENDPOINT.format("{length:int}"), StatusResource(logic))

    return app


def get_app():
    storage = DbStorage()
    broker = RabbitMqBroker()
    return create_app(storage, broker)
