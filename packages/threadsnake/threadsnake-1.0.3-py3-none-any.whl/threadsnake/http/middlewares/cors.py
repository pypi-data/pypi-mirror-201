from ..core.httprequest import HttpRequest
from ..core.httpresponse import HttpResponse
from ..application import Application
from ...http.types import Next

def cors(app: Application, req: HttpRequest, res: HttpResponse, next:Next) -> None:
    '''Configures CORS.'''
    res.set_header('Access-Control-Allow-Origin', "*")
    next()