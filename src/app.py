# app.py
import falcon

from api.resources import (
    RestResource,
)
from api.middlewares import (
    ContentEncodingMiddleware,
)

app = falcon.API(middleware=[
    ContentEncodingMiddleware(),
])

app.add_route('/rest', RestResource())
