import time,os,inspect,datetime
from typing import Any,Dict

from fastapi import (FastAPI,
                     UploadFile,
                     File,Header, 
                     Depends,
                     HTTPException,
                     Request,
                     Response,
                     WebSocket,
                     WebSocketDisconnect, 
                     Cookie,
                     status as StateCodes)
 
from .controller import create_controller,controller as api,   register_controllers_to_app 
from .controller_utils import  TEMPLATE_PATH_KEY, VER_KEY,get_docs  
from .config import config,ROOT_PATH,_log
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse,JSONResponse,ORJSONResponse
from . import midware
from . import auth


__is_debug=False

class MvcApp(FastAPI):
    def __init__(self,  **kwargs):
        self._authObj:auth.AuthenticationBackend_ = None 
        self._user_auth_url=""
        self._public_auth_url=""
        super().__init__(**kwargs)
    @property
    def authObj(self)->auth.AuthenticationBackend_:
        return self._authObj
    @authObj.setter
    def authObj(self,value:auth.AuthenticationBackend_):
        self._authObj = value
    pass

 
__app = MvcApp( ) 

__app_views_dirs = {} 
__all_controller__ = []

application = __app

def __init_auth(app,auth_type:str):
    __type_casbin_adapter = config.get("auth").get("casbin_adapter","file")
    casbin_adapter =  auth._adapters[__type_casbin_adapter] if __type_casbin_adapter in auth._adapters else None
    if not casbin_adapter:
        raise f"Not support {__type_casbin_adapter} ,Adapter config error in auth.casbin_adapter"
    
    auth_class = auth._auth_types[auth_type] if auth_type in auth._auth_types else None
    if not auth_class:
        raise f"{auth_type} auth type not support"
    __adapter_uri = config.get("auth").get("adapter_uri",'./configs/casbin-adapter.csv') 
    __auth_key = config.get("auth").get(f"{auth_type}_key","")
    kwargs = {'secret_key':__auth_key} 
    return auth.init(app=app, backend = auth_class,**kwargs)


def api_router(path:str="", version:str="",**allargs):  
    '''
    :param path :special path format ,ex. '/{controller}/{version}'
    :param version :str like 'v1.0' ,'2.0'..
    '''
    if not 'auth' in allargs:
        allargs['auth'] = 'public'

    caller_frame = inspect.currentframe().f_back
    caller_file = caller_frame.f_code.co_filename
    relative_path = caller_file.replace(ROOT_PATH,"")
    if relative_path.count(os.sep)>2:
        app_dir = os.path.dirname(os.path.dirname(relative_path)).replace(os.sep,"")
    else:
        app_dir = "app"
    app_dir = os.path.join(ROOT_PATH,app_dir)

    def format_path(p,v):
        if p and  '{controller}' not in p :
            p += '/{controller}' 
            p += '/{version}' if v else ''
        if v and not path:
            p = "/{controller}/{version}"
        return p
    path = format_path(path,version) 
    _controllerBase = create_controller(path,version)  
        
    __all_controller__.append(_controllerBase)
    
    def _wapper(targetController):  
        
        class puppetController( targetController ,_controllerBase ): 
            '''puppet class inherited by the User defined controller class '''
            def __init__(self,**kwags) -> None: 
                
                super().__init__()
            def _user_logout(self,msg='your are successed logout!'):
                """see .core.py"""
                self.flash  = msg
                if  hasattr(application,'authObj'):
                    application.authObj.clear_userinfo(request=self.request)
                accept_header = self.request.headers.get("Accept")    
                if accept_header == "application/json":
                    return {'status':'success','msg':msg}
                else:
                    return self.redirect('/')
            def _verity_successed(self,user,redirect_url='/', msg="User authentication successed!"):
                '''call by targetController''' 
                 
                self.flash  = msg
                accept_header = self._request.headers.get("Accept")
                if  hasattr(application,'authObj'):
                    access_token = application.authObj.create_access_token(user,request=self.request)
                
                    if accept_header == "application/json":
                        return {'status':'success','msg':msg,'token':str(access_token)}
                     
                else:  
                    if accept_header == "application/json":
                        return {'status':'success','msg':msg }
                 
                return RedirectResponse(redirect_url,status_code=StateCodes.HTTP_303_SEE_OTHER)
            def _verity_error(self,msg="User authentication failed!"):
                '''call by targetController'''
                 
                self.flash  = msg 
                url =  self.request.headers.get("Referer") or '/'
                accept_header = self.request.headers.get("Accept")
                if accept_header == "application/json":
                    return JSONResponse(content={'status':StateCodes.HTTP_200_OK,'msg':msg})
                return RedirectResponse(url,status_code=StateCodes.HTTP_303_SEE_OTHER),None
            
            @classmethod
            async def _auth__(cls,request:Request,response:Response,**kwargs):
                '''called by .controller_util.py->route_method'''
                if not hasattr(application,'authObj'):
                    return True,None
                auth_type = kwargs['auth_type'] 
                kwargs['session'] = request.session # cls._session
                ret,user = await application.authObj.authenticate(request,response,**kwargs)
                def add_redirect_param(url: str, redirect_url: str) -> str:
                    if "?" in url:
                        return url + "&redirect=" + redirect_url
                    else:
                        return url + "?redirect=" + redirect_url
                accept_header = request.headers.get("Accept")
                
                #
                if not ret and not user: 
                    if accept_header == "application/json":
                        return  ORJSONResponse(content={"message": "401 UNAUTHORIZED!"},
                                                   status_code=StateCodes.HTTP_401_UNAUTHORIZED),None
                    _auth_url = getattr(application,f"_{auth_type}_auth_url") if hasattr(application,f"_{auth_type}_auth_url") else None

                    if _auth_url: 
                        if 'flash' not in request.session:
                            request.session['flash']=''
                        request.session['flash']  = "you are not authenticated,please login!"  
                        _auth_url = add_redirect_param(_auth_url,str(request.url))
                        return RedirectResponse(_auth_url,status_code=StateCodes.HTTP_303_SEE_OTHER),None
                    else:  
                        return RedirectResponse('/',status_code=StateCodes.HTTP_303_SEE_OTHER),None
                else:
                    return ret,user

        setattr(puppetController,"__auth__",allargs['auth'])         
        setattr(puppetController,"__name__",targetController.__name__)  
        setattr(puppetController,"__controller_name__",targetController.__name__.lower().replace("controller",""))  
        
        setattr(puppetController,"__version__",version)  
        setattr(puppetController,"__location__",relative_path)  
        setattr(puppetController,"__appdir__",app_dir)  

        setattr(puppetController,"__controler_url__",targetController.__name__.lower().replace("controller",""))  
        #for generate url_for function
        _view_url_path:str = "/" + os.path.basename(app_dir) + '_views'  
         
        setattr(puppetController,"__view_url__",_view_url_path) 

        #add app dir sub views to StaticFiles
        if not app_dir in __app_views_dirs: #ensure  load it once
            __app_views_dirs[app_dir] = os.path.join(app_dir,"views")
            #path match static files
            _static_path = _view_url_path              
            __app.mount(_static_path,  StaticFiles(directory=__app_views_dirs[app_dir]), name=os.path.basename(app_dir))
 
        return puppetController 
    return _wapper #: @puppetController 


def get_wrapped_endpoint(func):
    ret = func
    while hasattr(ret,'__wrapped__'):
        ret = getattr(ret,'__wrapped__')
    return ret

def generate_mvc_app(isDebug):
    if not len(__all_controller__)>0:
        raise "must use @api_route to define a controller class"
    all_routers = []
    all_routers_map = {}
    for ctrl in __all_controller__:
        all_routers.append(register_controllers_to_app(__app, ctrl))
    for router in all_routers:
        for r in router.routes:
            funcname = str(r.endpoint).split('<function ')[1].split(" at ")[0] 
            end_point_abs = get_wrapped_endpoint(r.endpoint)
            auth_type = getattr(end_point_abs,'__auth__') if hasattr(end_point_abs,'__auth__') else 'None'
            doc_map =  get_docs(r.description) if hasattr(r,'description') else {}
            if hasattr(r,'methods'):
                methods = r.methods
            else:
                methods = r.name
            if isDebug:  
                _log.debug('{:20}-->{:50}-->{}'.format(str(methods),r.path,funcname) )
            all_routers_map[funcname] = {'path':r.path,'methods':methods,'doc':doc_map,'auth':auth_type}
    application.routers_map = all_routers_map  
    midware.init(app=application,debug=isDebug)
    
    auth_type = config.get("auth",None)
    if auth_type:
        auth_type=auth_type.get("type" )
        if auth_type:
            application.authObj = __init_auth(__app,auth_type)
    return application

def run(app,*args,**kwargs): 
    import uvicorn
    global __is_debug
    host =  "host" in kwargs  and kwargs["host"]  or '0.0.0.0' 
    port = "port" in kwargs  and kwargs["port"] or 8000  
    __is_debug = "debug" in kwargs and kwargs["debug"]   
     
    uvicorn.run(app, host=host, port=port)