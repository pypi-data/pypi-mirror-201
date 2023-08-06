from time import time

from ..core.httprequest import HttpRequest
from ..core.httpresponse import HttpResponse
from ..application import Application
from ...http.types import Next

def time_measure(app:Application, req:HttpRequest, res:HttpResponse, next:Next) -> None:
    '''
    Ideally measures the time than all pipeline takes to execute.
    '''
    startTime = time()
    next()
    interval = (time() - startTime) * 1000
    res.headers['RTT'] = str(interval)