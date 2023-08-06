from multiprocessing import AuthenticationError
from .const import *
from .compare_it_model import CompareItModel
import time
import requests
import json

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

    def login(self):
        uri = 'user/login'
        body = {"username": self._username, "password": self._password}
        headers =  {"Content-Type":"application/json"}
        response = requests.post(self._set_uri(uri), data=json.dumps(body), headers=headers)
        if response.status_code == 200:
            self.access_token = response.json()['at']
        else:
            raise AuthenticationError(f"Unable to login with {self._username}")
        
    def get_all_entities(self):
        uri = 'view/overview'
        return self._get_cached(uri)

    def get_entity(self, uuid):
        uri = 'object/' + uuid
        return self._get_internal(uri)

    def set_entity(self, uuid, value) -> bool:
        uri = 'object/' + uuid
        if self.access_token is None:
            self.login()
            return self.set_entity(uuid, value)
        try:
            body = {"target": value}
            _ = requests.put(self._set_uri(uri), data=json.dumps(body), headers = self._get_headers())
            return True
        except Exception as e:
            print(e)
            return False

    def _get_cached(self, uri) -> str:
        if uri in self._model.cachedresponse.keys():
            response_object: dict = self._model.cachedresponse.get(uri) 
            if time.time() - response_object.get(DATETIME) < CALLTIMEOUT:
                return response_object.get(RESPONSE)
        return self._get_internal(uri)

    def _get_internal(self, uri):
        if self.access_token is None:
            self.login()
            return self._get_internal(uri)
        response = requests.get(self._set_uri(uri), headers = self._get_headers())    
        if response.status_code == 200:
            ret = json.dumps(response.json())
            self._model.cachedresponse[uri] = {
                RESPONSE : ret,
                DATETIME: time.time()
            }
            return ret
        else:
            return 'Error!'

    def _set_uri(self, uri) -> str:
        return self._model.endpoint + uri

    def _get_headers(self) -> dict:
        return {"Content-Type":"application/json", "Authorization": self.access_token}



