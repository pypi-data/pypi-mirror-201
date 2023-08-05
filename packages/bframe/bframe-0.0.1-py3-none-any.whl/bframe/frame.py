import inspect
import json
import threading
from typing import Any, Callable, Union

from bframe import __version__
from bframe.ctx import request
from bframe.http_server import (HTTP_METHOD, Request, Response,
                                       SimpleHTTPServer, SimpleRequestHandler)
from bframe.logger import Logger as Log
from bframe.logger import init_logger
from bframe.route import NoSetControllerException, Tree
from bframe.utils import to_bytes

MethodSenquenceAlias = Union[tuple, list]


class _Frame():

    version = "frame/%s" % __version__

    # http server
    Server: SimpleHTTPServer = None
    ServerLock: threading.Lock = threading.Lock()

    # 路由
    RouteMap: Tree = Tree()
    RouteMapLock: threading.Lock = threading.Lock()

    # 日志
    Logger: Log = init_logger(__name__)

    def __init__(self, name: str = None) -> None:
        self.app_name = name
        if name is None:
            self.app_name = __name__

    def add_route(self, url: str, func_or_class: Callable, method: MethodSenquenceAlias = None):
        raise NotImplemented

    def get(self, url: str):
        def wrapper(f):
            self.add_route(url, f, "GET")
            return f
        return wrapper

    def post(self, url: str):
        def wrapper(f):
            self.add_route(url, f, "POST")
            return f
        return wrapper

    def put(self, url: str):
        def wrapper(f):
            self.add_route(url, f, "PUT")
            return f
        return wrapper

    def delete(self, url: str):
        def wrapper(f):
            self.add_route(url, f, "DELETE")
            return f
        return wrapper

    def run(self, address: str = "127.0.0.1", port: int = 7256):
        self.Logger.info("run mode: no wsgi")
        try:
            if self.Server is None:
                with self.ServerLock:
                    self.Server = SimpleHTTPServer(server_address=(address, port),
                                                   RequestHandlerClass=SimpleRequestHandler,
                                                   application=self)
            self.Logger.info("start server http://%s:%s" % (address, port))
            self.Server.serve_forever()
        except KeyboardInterrupt:
            self.Logger.info("shutdown server")
            self.Server.shutdown()

    def dispatch(self, request: Request):
        raise NotImplemented

    def __call__(self, request: Request):
        return self.dispatch(request)


class Frame(_Frame):

    def route(self, url: str, method: MethodSenquenceAlias = None):
        def wrapper(f):
            self.add_route(url, f, method)
            return f
        return wrapper

    def add_route(self, url: str, func_or_class: Callable, method: MethodSenquenceAlias = None):
        def _add_class_handle(cls):
            meth = [method.lower()
                    for method in HTTP_METHOD if hasattr(cls, method.lower())]
            for m in meth:
                _url = "%s/%s" % (url, m.upper())
                self.RouteMap.add(_url, getattr(cls(), m))

        with self.RouteMapLock:
            _methods = method
            if _methods is None:
                _methods = ["GET"]
            if not isinstance(_methods, (tuple, list)):
                _methods = [_methods]

            if inspect.isclass(func_or_class):
                _add_class_handle(func_or_class)
                return
            for m in _methods:
                _url = "%s/%s" % (url, m.upper())
                self.RouteMap.add(_url, func_or_class)

    def match_handle(self, request: Request) -> Callable:
        url = "%s/%s" % (request.Path, request.Method)
        return self.RouteMap.find(url)

    def wrapper_response(self, resp: Any) -> Response:
        self.Logger.info("wrapper_response:", str(resp)[:20])
        if isinstance(resp, Response):
            resp.Body = to_bytes(resp.Body)
            return resp
        if isinstance(resp, (str, bytes)):
            return Response(code=200,
                            body=to_bytes(resp))
        if isinstance(resp, dict):
            return Response(code=200,
                            headers={"Content-Type": "application/json"},
                            body=to_bytes(json.dumps(resp)))

    def dispatch(self, r: Request):
        # self.Logger.info("thread:", threading.enumerate())
        try:
            request.push(r)
            handle = self.match_handle(r)
            response = self.wrapper_response(handle())
        except NoSetControllerException as e:
            self.Logger.debug(e.args)
            response = Response(code=404)
        except Exception as e:
            self.Logger.debug(e.args)
            raise Exception("execute handle error", e.args[0])
        finally:
            return response
