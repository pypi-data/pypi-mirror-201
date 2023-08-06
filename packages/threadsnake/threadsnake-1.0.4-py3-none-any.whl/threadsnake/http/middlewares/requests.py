from typing import List
from ..core.httprequest import HttpRequest
from ..core.httpresponse import HttpResponse
from ..application import Application
from ...http.types import CallbackMutator, Callback, RequestPredicate

def validates_request(predicate:RequestPredicate, onFailMessage:str = None, onFailStatus:int = 400) -> CallbackMutator:
    '''
    Generalizes request validation using a "predicate" function wich receives the current HttpRequestInstance
    and returns a boolean. If the result is false, the client receives an "onFailStatus" status code and an
    "onFailMessage" message. Otherwise the pipeline executes normally.
    '''
    def mutator(middleware:Callback) -> Callback:
        def callback(app:Application, req:HttpRequest, res: HttpResponse) -> None:
            if predicate(req):
                middleware(app, req, res)
            else:
                res.end(onFailMessage or "Bad Request", onFailStatus)
        return callback
    return mutator

def accepts(contentTypes:List[str]) -> CallbackMutator:
    '''
    Validates the HttpRequest content-type against the list of "contentTypes", with are the allowed ones. 
    Returns an UnsuportedMediaType status code if the content-type is not in the list. Otherwise the 
    pipeline executes normally. Delegates to "validates_request".
    '''
    return validates_request(lambda r: r.contentType in contentTypes, onFailStatus=415)

def accepts_json(callback:Callback) -> Callback:
    '''Especialization of accepts wich just allows json requests.'''
    return accepts(['application/json', 'text/json'])(callback)

def requires_parameters(parameters:List[str]) -> CallbackMutator:
    def predicate(req:HttpRequest) -> bool:
        receivedParameters:List[str] = [i for i in req.params]
        return len([i for i in parameters if i not in receivedParameters]) == 0
    message:str = 'Required parameters: ' + ', '.join(parameters)
    return validates_request(predicate, message)