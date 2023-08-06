import os,time,typing
from fastapi import FastAPI, HTTPException,exceptions,Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse,FileResponse,Response
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import traceback
from .config import _log,config
from .midware_session import SessionMiddleware,FileStorage,MemoryStorage,RedisStorage,SessionStorage,_SESSION_STORAGES


def init(app :FastAPI,debug:bool = False):
    async def on_startup():
        pass
    app.router.on_startup = [on_startup]
    # if debug:
        # from fastapi_utils.timing import add_timing_middleware 
         
        # add_timing_middleware(app, record=_log.info, prefix="app", exclude="untimed")

    #session midware
    _session_cfg:typing.Dict = config.get("session")
    _session_options = {}
    if _session_cfg:
        _storageType=_session_cfg.get("type","")
        if _storageType!="":
            if _storageType=='file':
                _session_options["storage"] = _SESSION_STORAGES[_storageType](dir=_session_cfg.get("dir","./sessions"))
            else:
                _session_options["storage"] = _SESSION_STORAGES[_storageType]()
            
        _session_options['secret_key'] = _session_cfg.get("secret_key","") 
    app.add_middleware(SessionMiddleware,**_session_options)

    @app.exception_handler(StarletteHTTPException)
    async def custom_http_exception_handler(request, e:StarletteHTTPException):
        content = "<h1>404 Not Found(URL Exception)</h1>"
        content += '<h3>please check url</h3>'
        if debug:
            content += '<p>' + str(e.detail) + '</p>'
        return HTMLResponse(content=content, status_code=404)
        _log.error(f"OMG! An HTTP error!: {repr(exc)}")
        return await http_exception_handler(request, exc)#by default handler

    @app.exception_handler(Exception)
    async def validation_exception_handler(request, e:Exception):
        content = "<h1>500 Internal Server Error</h1>"
        if debug: 
            exc_traceback = e.__traceback__ 
            # show traceback the last files and location
            tb_summary = traceback.extract_tb(exc_traceback) 
            content += '<p>'
            for filename, line, func, text in tb_summary: 
                content += (f"{filename}:{line} in {func}</br>") 
            content += '</p>'
            content += '<p>Error description:' + str(e.args)  + '</p>'
        return HTMLResponse(content=content, status_code=500)


    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        _log.error(f"OMG! The client sent invalid data!: {exc}")
        return await request_validation_exception_handler(request, exc)

    
    public_dir =  os.path.abspath(config.get("public_dir" ) )
    if not os.path.exists(public_dir):
        os.mkdir(public_dir)

    app.mount('/public',  StaticFiles(directory=public_dir), name='public')

    @app.get("/favicon.ico")
    def _get_favicon():
        if os.path.exists("./public/favicon.ico"): 
            return FileResponse("./public/favicon.ico")
        else:
            return Response(content = None,status_code= 404)
    @app.middleware("http")
    async def preprocess_request(request: Request, call_next):
        _log.debug(f"dispatch on preprocess_request")
        if debug:
            start_time = time.time() 
        #pre call to controller method
        response:Response = await call_next(request)

        if debug:
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)  
        return response 
    
    