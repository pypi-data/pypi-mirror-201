import json
from ..core.httprequest import HttpRequest
from ..core.httpresponse import HttpResponse
from ..application import Application
from ...http.types import Next

def json_body_parser(app:Application, req:HttpRequest, res:HttpResponse, next:Next) -> None:
    '''
    Configures "json" request type. If identifies a valid json in the request body, it sets
    the dict property of the current HttpRequest instance with the json content.
    '''
    if req.contentType in ['application/json', 'text/json']:
        try:
            req.data = json.loads(req.body.strip())
        except:
            res.status(400, 'Bad Request').write("Can't decode json body")
    next()