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

import importlib
import importlib.util
import os
import sys
from types import ModuleType
from typing import List, Tuple
from uuid import uuid4
import __main__

from ..application import Application
from ..router import Router

ConfiguredRoute = Tuple[str, List[Router]]

def import_module(path:str) -> ModuleType:
    if not path.endswith('.py'):
        path += '.py'    
    moduleName:str = os.path.basename(path) + str(uuid4()).replace('-', '')
    spec = importlib.util.spec_from_file_location(moduleName, path)
    module:ModuleType = importlib.util.module_from_spec(spec)
    sys.modules[moduleName] = module
    spec.loader.exec_module(module)
    return module

def routes_to(app:Application, path:str, root:str):
    baseFolder:str = os.path.dirname(__main__.__file__)
    fullSearchPath = os.sep.join([baseFolder, path.replace('/', os.sep)])
    module:ModuleType = import_module(fullSearchPath)
    for property in dir(module):
        router = getattr(module, property)
        if isinstance(router, Router):
            app.use_router(router, root)

def routes_to_folder(app:Application, path:str):
    location:str = os.path.dirname(os.path.abspath(__main__.__file__))
    fullSearchPath = os.sep.join([location, path])
    fullSearchPath = fullSearchPath.replace('/', os.sep).replace('\\', os.sep)
    files = [
        [path, result[0][len(fullSearchPath)+1:].replace('\\', '/'), file[:-3]] 
        for result in os.walk(fullSearchPath) for file in result[2]
        if file.endswith('.py')
    ]
    routes = [
        [
            '/'.join([j for j in i if len(j) > 0]),
            '/'.join([j for j in i[1:] if len(j) > 0])
        ]
        for i in files
    ]
    for route in routes:
        path, root = route
        routes_to(app, path, root)

##def get_routers(moduleName:str) -> List[Router]:
##    routers:List[Router] = []
##    module:ModuleType = importlib.import_module(moduleName)
##    for property in dir(module):
##        if isinstance(getattr(module, property), Router):
##            routers.append(getattr(module, property))
##    return routers
##
##def load_router(path:str) -> ConfiguredRoute:
##    if not path.endswith('.py'):
##        return
##    path = path[:-3]
##    pathParts:List[str] = [i for i in path.replace(os.sep, '.').split('.') if len(i) > 0]
##    module:str = '.'.join(pathParts)
##    path:str = '/'.join(pathParts[1:])
##    return path, get_routers(module)
##
##def get_files(folder:str) -> List[str]:
##    filo = [os.sep.join([j[0], i]) for j in os.walk(folder) for i in j[2]]
##    print(folder, filo)
##    input('')
##
##def load_routes(path:str) -> List[ConfiguredRoute]:
##    baseFolder:str = os.path.dirname(__main__.__file__)
##    fullSearchPath = os.sep.join([baseFolder, path])
##    get_files(fullSearchPath)
##    base:str = os.path.abspath(os.curdir)
##    print(f"{baseFolder} on {base}")
##    configuredRoutes: List[ConfiguredRoute] = []
##    modules:List[str] = [i for i in os.listdir(fullSearchPath) if i.endswith('.py')]
##    input(modules)
##    for module in modules:
##        configuredRoutes.append(load_router(os.sep.join([path, module])))
##    return configuredRoutes
##        
##def configure_routes(app:Application, path:str) -> None:
##    for configuredRoute in load_routes(path):
##        for router in configuredRoute[1]:
##            app.use_router(router, configuredRoute[0])