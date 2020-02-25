import falcon
from api.logic import ApiLogic
from api.middlewares import ContentEncodingMiddleware
from api.resources import SequenceResource, StatusResource
from api.storage.memory import MemoryStorage

app = falcon.API(middleware=[ContentEncodingMiddleware()])

storage = MemoryStorage()
logic = ApiLogic(storage)

app.add_route("/api/fibo/{length:int}", SequenceResource(logic))
app.add_route("/api/fibo/{length:int}/status", StatusResource(logic))
