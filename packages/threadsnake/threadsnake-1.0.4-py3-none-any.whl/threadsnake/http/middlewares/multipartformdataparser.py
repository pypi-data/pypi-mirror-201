##    Threadsnake. A tiny experimental server-side express-like library.
##    Copyright (C) 2022  Erick Fernando Mora Ramirez
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <https://www.gnu.org/licenses/>.
##
##    mailto:erickfernandomoraramirez@gmail.com

import os
from time import time
from typing import Callable, Dict, List
from uuid import uuid4

from ...http.core.common import map_dictionary
from ...http.types import Middleware, Next
from ..core.httprequest import HttpRequest
from ..core.httpresponse import HttpResponse
from ..application import Application


def save_as_binary(tempFolder:str, data:str):
    tempFileName:str = os.sep.join([tempFolder, str(uuid4()).replace('-', '')+'.tmp'])
    if not os.path.isdir(tempFolder):
        os.mkdir(tempFolder)
    with open(tempFileName,'wb') as f:
        f.write(data.encode('latin-1'))
    return tempFileName

def get_chunked(req:HttpRequest) -> str:
    body:str = req.body
    if 'chunked' in req.headers.get('Transfer-Encoding', '') and '\r\n' in body:
        res = ''
        chunk_i = 1
        while chunk_i > 0:
            split = body.split('\r\n', maxsplit=1)
            chunk, body = split if len(split) == 2 else [split[0], '']
            chunk_i = int(chunk, 16)
            res += body[:chunk_i]
            body = body[chunk_i+2:]
        body = res
    return body

def build_file_decoder(files:Dict[str, float], folder:str, duration:int):
    def decode_body_parameter(parameter:str, req:HttpRequest):
        header, value = parameter.split('\r\n\r\n', maxsplit=1)
        header = header.replace('\r\n', '; ').replace(': ', '=').replace('"', '')
        headerDict = map_dictionary(header, ';', '=')
        if 'filename' in headerDict:
            filename:str = headerDict['filename']
            tempFileLocation:str = save_as_binary(folder, value)
            req.files[filename] = tempFileLocation
            files[tempFileLocation] = time() + duration
        elif 'name' in headerDict:
            req.params[headerDict['name']] = value
    return decode_body_parameter

def remove_old_files(files:Dict[str, float]) -> None:
    removedFiles:List[str] = []
    for file in files:
        if files[file] < time():
            try:
                os.remove(file)
                removedFiles.append(file)
            except:
                print(f'error removing file: {file}')
    for file in removedFiles:
        del files[file]

def multipart_form_data_parser(tempFolder:str = None, filesDurationSec:int = 30) -> Middleware:
    files:Dict[str, float] = {}
    tempFolder = tempFolder or os.sep.join(['.', 'temp'])
    decoder:Callable[[str, HttpRequest], None] = None
    decoder = build_file_decoder(files, tempFolder, filesDurationSec)
    def middleware(app:Application, req:HttpRequest, res:HttpResponse, next:Next) -> None:
        if 'multipart/form-data' in req.contentType:
            boundary:str = ''
            req.contentType, boundary = [i.strip() for i in req.contentType.split(';', 1)]
            boundary = boundary.strip().replace('boundary=', '--').replace('"', '')
            body:str = get_chunked(req)
            bodyParameters:List[str] = [i.strip() for i in body.split(boundary)]
            for param in bodyParameters:
                if param == '--' or len(param) == 0:
                    continue
                decoder(param, req)
        remove_old_files(files)
        next()
    return middleware
