 
from fastapi import FastAPI,UploadFile,File,Header, Depends,HTTPException,Request,Response, status as StateCodes
from fastapi.responses import RedirectResponse,HTMLResponse,PlainTextResponse
from .view import _View
 
from .config import config,ROOT_PATH,_log
import os,uuid
from hashlib import md5
from typing import Dict
from logging import Logger
import inspect
 

__session_config = config.get('session') 
_session_key = "session_id"
if __session_config:
    _session_key = __session_config.get("key","session_id")
# _sessionManager = SessionManager(storage=_SESSION_STORAGES[__session_config['type']](__session_config['dir'],__session_config['secretkey']))



class BaseController:
    
    def __init__(self) -> None:
        
        
        _log.debug('__init__ on BaseController')
    @property
    def log(self)->Logger:
        return _log
    @property 
    def cookies(self)->Dict[str,str]: 
        return self._cookies 
    
    @property
    def request(self)->Request :
        return self._request
    # @request.setter
    # def request(self,value):
    #     self.__request = value
    @property
    def response(self)->Response :
        return self._response
    # @response.setter
    # def response(self,value):
    #     self.__response = value
    @property
    def session(self)->Dict:
        return self._session  
    @classmethod
    def redirect(self,url,flash:str="",statu_code=StateCodes.HTTP_303_SEE_OTHER):
        self._session['flash'] = {"url" : flash }
        return RedirectResponse(url,status_code=statu_code)
    
    def _verity_successed(self,user,msg="User authentication successed!"):
        """see .core.py"""
        pass
        
    
    def _verity_error(self,msg="User authentication failed!"):
        """see .core.py"""
        pass

    def check_redirect_back(self):
        flash = self.session.get('flash')
        flash = flash['url'] if flash else ""
        return self.redirect(url=flash) if flash else self.redirect("/")

     
    # @property
    def view(self,content:str="",view_path:str="", format:str="html", context: dict={},local2context:bool=True,**kwargs): 
        def url_for(url:str="",type:str="static",**kws):
            url_path :str = self.__view_url__ 
            url = url.strip()
            if type!='static' or kws: #url route
                if kws:
                    url_path = ""
                    pairs = []
                    if 'app' in kws and kws['app'].strip():
                        pairs.append(kws['app'].strip())
                    if 'controller' in kws  and kws['controller'].strip():
                        pairs.append(kws['controller'].strip())
                    if 'version' in kws  and kws['version'].strip():
                        pairs.append(kws['version'].strip())
                    if 'action' in kws  and kws['action'].strip():
                        pairs.append(kws['action'].strip())
                    elif url :
                        pairs.append(url)
                    url_path = "/"+"/".join(pairs)
                    return url_path
                    pass
                else:
                        
                    url_path = self.__template_path__.replace('{controller}',self.__controller_name__).replace("{version}",self.__version__)
                    return url_path + "/" + url.strip()
            else:
                url_path += '/' + self.__controller_name__
                if self.__version__:
                    url_path += '/' + self.__version__
                return url_path + "/"  + url.strip()
            
        if content:
            if format=='html':
                return HTMLResponse(content,**kwargs)
            elif format=='text':
                return PlainTextResponse(content,**kwargs)
            else:
                return Response(content=content,**kwargs)
        def get_path(caller_frame,view_path:str="",context:dict={},local2context:bool=True ):
            # caller_file = caller_frame.f_code.co_filename
            # caller_lineno = caller_frame.f_lineno
            caller_function_name = caller_frame.f_code.co_name
            caller_locals = caller_frame.f_locals
            caller_class = caller_locals.get("self", None).__class__
            caller_classname:str = caller_class.__name__
            caller_classname = caller_classname.replace("Controller","").lower()
            #caller_file = os.path.basename(caller.filename) 
            if local2context and not context:
                del caller_locals['self']
                context.update(caller_locals)
            if not view_path:
                if self.__version__:
                    version_path = f"{self.__version__}/"
                else:
                    version_path = ""
                view_path = f"{caller_classname}/{version_path}{caller_function_name}.html" 
            return view_path,context
            
        caller_frame = inspect.currentframe().f_back
        view_path,context = get_path(caller_frame)
        context['flash'] = self.session.get('flash',{})
        template_path = os.path.join(self.__appdir__,"views")
        viewobj = _View(self._request,self._response, tmpl_path=template_path) 
        viewobj._templates.env.globals["url_for"] = url_for 
        return viewobj(view_path,context,**kwargs)
    
    async def getUploadFile(self,file:File):  
        
        if config.get("upload"):
            updir = config.get("upload")['dir'] or "uploads"
        else:
            updir = 'uploads'
        _save_dir = os.path.join(ROOT_PATH,updir) 
        if not os.path.exists(_save_dir):
            os.mkdir(_save_dir) 
        data = await file.read()
        ext = file.filename.split(".")[-1]
        md5_name = md5(data).hexdigest()
        if ext:
            md5_name+="."+ext
        save_file = os.path.join(_save_dir, md5_name) 
        if not os.path.exists(save_file): 
            f = open(save_file, 'wb') 
            f.write(data)
            f.close()
        return save_file
    async def _constructor(base_controller_class,request:Request,response:Response):  
        # if not hasattr(request,'params') and request.method!='GET' :
        #     request.params = await request.json()
        # if not hasattr(request,'params'):
        #     request.params = {}
        #     if request.query_params:
        #         request.params = dict(request.query_params)
        if not _session_key in request.cookies or not request.cookies[_session_key]:
            request.cookies[_session_key] = str(uuid.uuid4())

        request.state.keep_flash = False
        base_controller_class._request:Request = request
        base_controller_class._response:Response = response 
        base_controller_class._cookies:Dict[str,str] = request.cookies.copy()
        # base_controller_class._session = await  _sessionManager.initSession(request,response )
        base_controller_class._session = request.session
        
         
    async def _deconstructor(base_controller_class,new_response:Response):  
        def process_cookies(response:Response, cookies,old_cookies):
            for key in cookies: 
                if   key != _session_key: 
                    response.set_cookie(key,cookies[key])
            for key in old_cookies:
                if not key in cookies and key != _session_key:
                    response.set_cookie(key=key,value="",max_age=0)   
            response.set_cookie(key=_session_key,
                                value=base_controller_class._request.cookies[_session_key],
                                max_age = 14 * 24 * 60 * 60,  # 14 days, in seconds
                                path  = "/",
                                samesite  = "lax",
                                httponly  = False ) 
        process_cookies(new_response,base_controller_class._cookies,base_controller_class._request.cookies)
        # await _sessionManager.process(session =  base_controller_class._session,response = new_response,request=base_controller_class._request)
        flash:Dict =  base_controller_class._session.get("flash")
        if flash and not base_controller_class._request.state.keep_flash:
            base_controller_class._session['flash'] = {}
            url = flash.get("url") 
            if url: 
                return base_controller_class.redirect(url)
        
         