import falcon
from api.config import SEQUENCE_ENDPOINT, STATUS_ENDPOINT
from api.logic import ApiLogic
from api.middlewares import ContentEncodingMiddleware
from api.resources import SequenceResource, StatusResource
from api.storage.memory import MemoryStorage

app = falcon.API(middleware=[ContentEncodingMiddleware()])

storage = MemoryStorage({0: 0, 1: 1, 2: 1, 3: 2, 4: 3, 5: 5})
logic = ApiLogic(storage)

app.add_route(SEQUENCE_ENDPOINT.format("{length:int}"), SequenceResource(logic))
app.add_route(STATUS_ENDPOINT.format("{length:int}"), StatusResource(logic))
