import falcon
from api.middlewares import ContentEncodingMiddleware
from api.resources import SequenceResource, StatusResource
from api.storage.memory import MemoryStorage

app = falcon.API(middleware=[ContentEncodingMiddleware()])

storage = MemoryStorage()

app.add_route("/api/fibo/{length:int}", SequenceResource(storage))
app.add_route("/api/fibo/{length:int}/status", StatusResource(storage))
