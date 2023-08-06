from .exceptions import *
import requests
import json

class BaseClient():

    """
    The Base Client handles user authentication and connection to the Goated API.
    A connection can be authenticated using either:
    - An account email and password via BaseClient.create_with_login()
    - An authentication token via BaseClient.create_with_token()
    """

    def __init__(
        self,
        url: str,
        token: str = None,
        api_key: str = None,
        api_secret: str = None
    ):
        self._url = url if url[-1] == '/' else url + '/'
        self._token = token
        self._api_key = api_key
        self._api_secret = api_secret
        if self._token or (self._api_key and self._api_secret):
            self._generate_header()
        else:
            self._header = None

    @classmethod
    def create_with_login(
        cls,
        url: str,
        email: str,
        password: str
    ):
        '''
        Creates a BaseClient connection when provided with a valid Goated API URL, email and password.
        '''
        client = cls(
            url = url
        )
        client.login(
            email = email,
            password = password
        )
        return client

    @classmethod
    def create_with_token(
        cls,
        url: str,
        token: str,
    ):
        '''
        Creates a BaseClient connection when provided with a valid Goated API URL and valid authentication token (returned from the auth/login endpoint).
        '''
        return cls(
            url = url,
            token = token
        )

    @classmethod
    def create_with_api_key(
        cls,
        url: str,
        api_key: str,
        api_secret: str
    ):
        '''
        Creates a BaseClient connection when provided with a valid Goated API URL and valid API Key and API Secret.
        '''
        return cls(
            url = url,
            api_key = api_key,
            api_secret = api_secret
        )

    def _generate_header(
        self,
    ):
        if self._token:
            self._header = {
                'Authorization': 'Token ' + self._token
            }
        elif self._api_key and self._api_secret:
            self._header = {
                'GOATED-API-KEY': self._api_key,
                'GOATED-API-SECRET': self._api_secret
            }
        else:
            raise Exception()

    def _get_objects(
        self,
        endpoint: str,
        filters: dict,
        get_all_paginated: bool = True
    ):
        '''
        Gets a list of objects from the API, including iterating through pagination until all items are obtained.
        '''
        objects = []
        response = self._send_get(
            endpoint=endpoint,
            params = filters
        )
        objects += response.get('results')
        if response.get('next') is not None and get_all_paginated:
            while response.get('next'):
                response = self._send_get(
                    endpoint=response.get('next'),
                )
                objects += response.get('results')
        return objects

    def _get_object(
        self,
        endpoint: str,
    ):
        '''
        Gets a single object from the API.
        '''
        response = self._send_get(
            endpoint=endpoint,
        )

        return response

    def login(
        self,
        email: str,
        password: str,
    ):
        '''
        Attempts to login via the Goated Authentication API.
        '''
        response = self._send_post(
            endpoint = "auth/login/",
            data = {
                'email': email,
                'password': password
            }
        )   
        self._token = response.get('key')
        self._generate_header()


    def _send_get(
        self,
        endpoint: str,
        data: dict = {},
        params: dict = {}
    ):  
        '''
        Assembles and executes an authenticated GET request.
        '''
        if str(self._url) in endpoint:
            endpoint = endpoint.replace(str(self._url), '')
        response = requests.get(
            self._url + endpoint,
            json = data,
            headers= self._header,
            params = params
        )
        # print(response)
        if response.status_code not in [200, 201, 202]:
            raise GoatedApiException(response)
        json_data = json.loads(response.text)
        if json_data.get('success') == True:
            return json_data.get('data')
        else:
            raise GoatedApiException(json_data)

    def _send_post(
        self,
        endpoint: str,
        data: str = {},
        params: dict = {}
    ):
        '''
        Assembles and executes an authenticated POST request.
        '''
        if str(self._url) in endpoint:
            endpoint = endpoint.replace(str(self._url), '')
        response = requests.post(
            self._url + endpoint,
            json = data,
            headers= self._header,
            params = params
        )
        if response.status_code not in [200, 201, 202]:
            raise GoatedApiException(response)
        json_data = json.loads(response.text)
        if json_data.get('success') == True:
            return json_data.get('data')
        else:
            raise GoatedApiException(json_data)
        

    def _send_patch(
        self,
        endpoint: str,
        data: str = {},
        params: dict = {}
    ):
        '''
        Assembles and executes an authenticated PATCH request.
        '''
        if str(self._url) in endpoint:
            endpoint = endpoint.replace(str(self._url), '')
        response = requests.post(
            self._url + endpoint,
            json = data,
            headers= self._header,
            params = params
        )
        if response.status_code not in [200, 201, 202]:
            raise GoatedApiException(response)
        json_data = json.loads(response.text)
        if json_data.get('success') == True:
            return json_data.get('data')
        else:
            raise GoatedApiException(json_data)
        