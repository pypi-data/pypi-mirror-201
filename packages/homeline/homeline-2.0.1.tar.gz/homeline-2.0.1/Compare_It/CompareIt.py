from multiprocessing import AuthenticationError
from .const import *
from .compare_it_model import CompareItModel
import time
import json
import aiohttp

class CompareIt:
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._access_token: str = None
        self._model = CompareItModel()
        
    @property
    def access_token(self):
        return self._access_token
    
    @access_token.setter
    def access_token(self, value):
        self._access_token = 'Bearer ' +value

    async def async_login(self):
        uri = await self.async_set_uri('user/login')
        body = {"username": self._username, "password": self._password}
        headers =  {"Content-Type":"application/json"}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(uri, data=json.dumps(body), headers=headers) as response:
                    at = await response.json()
                    self.access_token = at['at']
        except AuthenticationError as e:
            print(e)
        
    async def async_get_all_entities(self):
        uri = 'view/overview'
        return await self.async_get_cached(uri)

    async def async_get_entity(self, uuid):
        uri = 'object/' + uuid
        return await self.async_get_internal(uri)
        
    async def async_set_entity(self, uuid, value) -> bool:
        uri = 'object/' + uuid
        if self.access_token is None:
            await self.async_login()
            return await self.async_set_entity(uuid, value)
        try:
            body = {"target": value}
            headers = await self.async_get_headers()
            uri = await self.async_set_uri(uri)
            async with aiohttp.ClientSession() as session:
                async with session.put(uri, data=json.dumps(body), headers = headers):
                    return True
        except Exception as e:
            print(e)
            return False

    async def async_get_cached(self, uri) -> str:
        uri = await self.async_set_uri(uri)
        if uri in self._model.cachedresponse.keys():
            response_object: dict = self._model.cachedresponse.get(uri) 
            if time.time() - response_object.get(DATETIME) < CALLTIMEOUT:
                return response_object.get(RESPONSE)
        return await self.async_get_internal(uri)
        
    async def async_get_internal(self, uri):
        if self.access_token is None:
            await self.async_login()
            return await self.async_get_internal(uri)
        headers = await self.async_get_headers()
        async with aiohttp.ClientSession() as session:
            async with session.get(uri, headers = headers) as response:
                try:
                    ret = await response.json()
                    self._model.cachedresponse[uri] = {
                        RESPONSE : ret,
                        DATETIME: time.time()
                    }
                    return ret
                except:
                    return 'Error!'
    
    async def async_set_uri(self, uri) -> str:
        return self._model.endpoint + uri

    def async_get_headers(self) -> dict:
        return {"Content-Type":"application/json", "Authorization": self.access_token}



