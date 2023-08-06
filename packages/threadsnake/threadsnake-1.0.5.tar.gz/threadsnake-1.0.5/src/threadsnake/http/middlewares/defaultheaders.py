import time
from typing import Dict
from ..core.httprequest import HttpRequest
from ..core.httpresponse import HttpResponse
from ..application import Application
from ...http.types import Next, Middleware, DictProvider

def default_headers(headersProvider: DictProvider) -> Middleware:
    '''
    Sets response default headers. Those headers are determined by the result of the function "headersProvider"
    on every request.
    '''
    def middleware(app: Application, req: HttpRequest, res: HttpResponse, next:Next) -> None:
        headers = headersProvider()
        for h in headers:
            res.headers[h] = headers[h]
        next()
    return middleware

since = time.time()
requestNumber = 0

def build_default_headers(baseHeaders: Dict[str, str] = None) -> DictProvider:
    '''
    Provides a standar function for building default headers.
    '''
    def provider() -> Dict[str, str]:
        global requestNumber
        requestNumber += 1
        headers = baseHeaders or {}
        headers.update({
            "Date": time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(time.time())),
            "Active-Since": str(since),
            "Epoch": str(time.time()),
            "Powered-By": "Threadsnake beta",
            "Request-Count": requestNumber
        })
        return headers
    return provider