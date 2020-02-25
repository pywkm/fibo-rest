import falcon
from api.middlewares import ContentEncodingMiddleware
from api.resources import RestResource

app = falcon.API(  # pylint: disable=invalid-name
    middleware=[ContentEncodingMiddleware()]
)

app.add_route("/rest", RestResource())
