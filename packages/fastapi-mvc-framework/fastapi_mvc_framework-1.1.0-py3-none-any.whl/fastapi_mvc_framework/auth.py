import base64
import binascii

import casbin
from casbin.enforcer import Enforcer
import uvicorn
from fastapi import FastAPI,Request,Response
from starlette.authentication import AuthenticationBackend, AuthenticationError, SimpleUser, AuthCredentials,BaseUser
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import BaseUser,SimpleUser,UnauthenticatedUser
from casbin.persist.adapters import FileAdapter
from casbin.persist.adapter import Adapter
# from .midware_casbin import CasbinMiddleware
 
from .config import config
import jwt
from datetime import datetime, timedelta
from typing import Optional, Tuple, Union,Dict

_session_name:str = ""

class CasbinAuth:
    def __init__(self,enforcer:Enforcer,session_name="user") -> None:
        global _session_name
        self.enforcer = enforcer
        self.__session_name = _session_name = session_name
        pass
    def _auth(self,request:Request,username:str):
        path = request.url.path
        method = request.method   
        user = request.user.display_name if request.user.is_authenticated else 'anonymous'

        return self.enforcer.enforce(user, path, method)
    def __get_token_from_header(self, authorization: str, prefix: str) -> str:
        """Parses the Authorization header and returns only the token"""
        try:
            scheme, token = authorization.split()
        except ValueError as e:
            raise AuthenticationError('Could not separate Authorization scheme and token') from e 
        if scheme.lower() != prefix.lower():
            raise AuthenticationError(f'Authorization scheme {scheme} is not supported')
        return token
    def get_user_from_request(self,request:Request,prefix:str="Bearer",is_jwt:bool=False,**kwargs) : 
        userobj = request.session.get(self.__session_name)
        payload = None
        if userobj:
            if not isinstance(userobj,str):
                if hasattr(userobj,"username"):
                    userobj=getattr(userobj,"username")
        if not userobj or is_jwt:   
            auth = request.headers["Authorization"] if 'Authorization' in request.headers else None
            if auth:
                scheme, credentials = auth.split()
                
                if not is_jwt: #not userobj?
                    decoded = base64.b64decode(credentials).decode("ascii")
                    username, _, password = decoded.partition(":")
                    return username,password,None
                else:
                    token = self.__get_token_from_header(authorization=auth, prefix=prefix)
                    username_field = kwargs['username_field']
                    del kwargs['username_field']
                    try:
                        payload = jwt.decode(token,**kwargs)
                    except jwt.InvalidTokenError as e:
                        raise AuthenticationError(str(e)) from e
                    return  payload[username_field],token,payload
            elif userobj:
                return userobj,"",None
        else:
            return userobj,"",None
        return "","",None
    
class BasicAuth(AuthenticationBackend):
    def __init__(self,**kwargs) -> None:
        super().__init__()
     
    
    async def authenticate(self, request:Request,response,**kwargs):
        username,password,_ = _casbin_auth.get_user_from_request(request=request)
        if not username:
            return False,None
        user = SimpleUser(username)
        request.scope['user'] = user
        auth_type:str = kwargs.get("auth_type")
        if not auth_type or auth_type.lower()=='public': 
            return True,  user
        result = _casbin_auth._auth(request=request,username=username)
        return result, user

        return AuthCredentials(["authenticated"]), SimpleUser(username)
    
    def create_access_token(self,  username,**kwargs):
        global _session_name
        request:Request = kwargs['request'] if 'request' in kwargs else None
        if request:
            request.session[_session_name] = username
        return None
        
class JWTUser(BaseUser):
    def __init__(self, username: str, token: str, payload: dict) -> None:
        self.username = username
        self.token = token
        self.payload = payload

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.username


class JWTAuthenticationBackend(AuthenticationBackend):

    def __init__(self,
                 secret_key: str,
                 algorithm: str = 'HS256',
                 prefix: str = 'Bearer',
                 username_field: str = 'username',
                 audience: Optional[str] = None,
                 options: Optional[dict] = None) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.prefix = prefix
        self.username_field = username_field
        self.audience = audience
        self.options = options or dict()
    
     
    
    async def authenticate(self, request,response,**kwargs) -> Union[None, Tuple[AuthCredentials, BaseUser]]:
        args = {'username_field':self.username_field, 'key':self.secret_key, 'algorithms': self.algorithm , 'audience':self.audience ,
                                            'options':self.options }
        username,token,payload = _casbin_auth.get_user_from_request(request=request,
                                                                 prefix=self.prefix, 
                                                                 is_jwt=True,**args)
        if not username:
            return False,None
        user = SimpleUser(username)
        request.scope['user'] = user
        auth_type:str = kwargs.get("auth_type")
        if not auth_type or auth_type.lower()=='public': 
            return True,SimpleUser(username)    
        
        if  payload:
            result = _casbin_auth._auth(request=request,username=payload[self.username_field])
            return result, JWTUser(username=payload[self.username_field], token=token,
                                                        payload=payload) 
        return False,None
 
    def create_access_token(self,  user , expires_delta: timedelta = None,**kwargs)  :
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            authCfg = config.get('auth')
            if authCfg:
                expires_delta = int(authCfg.get('expires_delta',60))
            else:
                expires_delta = 60
            expire = datetime.utcnow() + timedelta(
                minutes=expires_delta
            )
        to_encode = {"exp": expire, "username": user }
        
        return jwt.encode(to_encode, self.secret_key ,self.algorithm )

_casbin_auth:CasbinAuth = None

def init(app:FastAPI,backend:AuthenticationBackend,adapter:Adapter=None,**kwagrs)->AuthenticationBackend:
    """
        kwargs:secret_key=KEY
    """
    __session_name = config.get("auth").get("session_name",'user')
    global _casbin_auth
    cfg = config.get("auth")
    model_file = cfg.get("auth_model",'./configs/casbin-model.conf')    
    if not adapter:
        adapter_file = cfg.get("auth_adapter",'./configs/casbin-adapter.csv') 
        adapter = FileAdapter(adapter_file)   
    enforcer = casbin.Enforcer(model_file, adapter)
    _casbin_auth = CasbinAuth(enforcer=enforcer,session_name=__session_name)
    authObj = backend(**kwagrs)
    return authObj
    app.add_middleware(CasbinMiddleware, enforcer=enforcer)
    app.add_middleware(AuthenticationMiddleware, backend=backend(**kwagrs))

def reload_adapter(app:FastAPI,adapter:Adapter=None):
    cfg = config.get("auth")
    model_file = cfg.get("auth_model",'./configs/casbin-model.conf')    
    if not adapter:
        adapter_file = cfg.get("auth_adapter",'./configs/casbin-adapter.csv')    
        adapter = FileAdapter(adapter_file)   
    enforcer = casbin.Enforcer(model_file, adapter) 
    app.router.current_casbin_instance = enforcer

_auth_types = {'basic':BasicAuth,'jwt':JWTAuthenticationBackend}
_adapters = {'file':FileAdapter,}