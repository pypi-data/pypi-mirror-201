import json
import pathlib
import jwt
from datetime import datetime, timedelta
from pathlib import Path
import requests
from netsuite.NetsuiteToken import NetsuiteToken
from netsuite.swagger_client.rest_client import RestClient, QueryClient
from netsuite.swagger_client.restlet_client import RestletClient
from netsuite.settings import APISettings
from netsuite.storages import BaseStorage, JSONStorage


class Netsuite:
    app_name: str = None
    storage: BaseStorage = None
    api_settings: APISettings
    rest_client = None
    query_client = None
    restlet_client = None

    def __init__(self, config: dict = None, config_file: Path = None):
        if config and config_file:
            raise ValueError("You can only load settings from one source")
        if config_file:
            with open(config_file, 'r') as f:
                config = json.load(f)
        if config is None and config_file is None:
            try:
                with open(pathlib.Path(APISettings().defaults.get("CREDENTIALS_PATH")), 'r') as f:
                    config = json.load(f)
            except Exception as e:
                raise Exception("No Configuration Present. Try Generating one.")

        self.api_settings = APISettings(config)
        if not self.api_settings.CLIENT_ID:
            raise Exception("Missing Client Id")
        if not self.api_settings.NETSUITE_APP_NAME:
            raise Exception("Missing Netsuite App Name")
        if not self.api_settings.NETSUITE_KEY_FILE:
            raise Exception("Missing Netsuite Certificate path.")
        if not self.api_settings.CERT_ID:
            raise Exception("Missing Netsuite Certificate ID.")

        self.app_name = self.api_settings.APP_NAME
        self.netsuite_app_name = self.api_settings.NETSUITE_APP_NAME
        self.netsuite_key_path = self.api_settings.NETSUITE_KEY_FILE
        self.netsuite_cert_id = self.api_settings.CERT_ID
        # self.field_map = None
        # if self.api_settings.NETSUITE_FIELD_MAP:
        #     self.field_map = self.api_settings.NETSUITE_FIELD_MAP

        self.storage = self.api_settings.STORAGE_CLASS()
        if isinstance(self.api_settings.STORAGE_CLASS(), JSONStorage):
            if not self.api_settings.JSON_STORAGE_PATH:
                raise Exception("JSON_STORAGE_PATH must be defined for JSONStorage")
            self.storage.storage_path = self.api_settings.JSON_STORAGE_PATH
        self.rest_url = f"https://{self.api_settings.NETSUITE_APP_NAME}.suitetalk.api.netsuite.com/services/rest" \
                        f"/record/v1/ "
        self.access_token_url = f"https://{self.api_settings.NETSUITE_APP_NAME}.suitetalk.api.netsuite.com/services/rest/auth/oauth2/v1/token",

    @property
    def REST_CLIENT(self):
        if not self.rest_client:
            self.rest_client = RestClient(self)
        return self.rest_client

    @property
    def QUERY_CLIENT(self):
        if not self.query_client:
            self.query_client = QueryClient(self)
            # if self.token.access_token is not None:
                # self.get_customer_categories()
                # self.get_status_dict()
        return self.query_client

    @property
    def RESTLET_CLIENT(self):
        if not self.restlet_client:
            self.restlet_client = RestletClient(self)
        return self.restlet_client

    @property
    def token(self) -> NetsuiteToken:
        return self.storage.get_token(self.app_name)

    def save_token(self, token):
        self.storage.save_token(self.app_name, token)

    def get_jwt(self):
        private_key = ""
        with open(self.netsuite_key_path, "rb") as pemfile:
            private_key = pemfile.read()
        payload = {
            "iss": f"{self.api_settings.CLIENT_ID}",
            "scope": "restlets, rest_webservices",
            "aud": f"{self.access_token_url}",
            "exp": (datetime.now() + timedelta(seconds=3600)).timestamp(),
            "iat": datetime.now().timestamp()
        }

        headers = {
            "typ": "JWT",
            "alg": "RS256",
            "kid": f"{self.netsuite_cert_id}"
        }
        jwt_token = jwt.encode(payload=payload, key=private_key, algorithm='RS256', headers=headers)

        return jwt_token

    def request_access_token(self):
        json_web_token = self.get_jwt()
        data = {
            'grant_type': 'client_credentials',
            'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
            'client_assertion': f'{json_web_token}'
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        url = f"https://{self.api_settings.NETSUITE_APP_NAME}.suitetalk.api.netsuite.com/services/rest/auth/oauth2/v1/token"
        response = requests.post(url, data=data, headers=headers)
        token = NetsuiteToken(**response.json())
        self.save_token(token)
        # if token.access_token is not None:
        #     self.get_customer_categories()
        #     self.get_status_dict()
        return self.token

    def change_app(self, app_name):
        self.app_name = app_name
        if not self.token.access_token:
            raise Exception(f"{app_name} does not have a token in storage, please authenticate")
        # self.rest_v1 = REST_V1(self)
        self.rest_client = RestClient(self)

    def get_token(self):
        if not self.token.is_expired:
            return self.token
        else:
            return self.request_access_token()

    # def get_status_dict(self):
    #     if self.token.access_token is None:
    #         return None
    #     if self.status_dict is None:
    #         query = "SELECT * FROM EntityStatus WHERE inactive = 'F'"
    #         statuses = self.QUERY_CLIENT.query_api.execute_query(query=query)
    #         status_dict = {}
    #         for status in statuses:
    #             status_dict[f"{status.get('entitytype').upper()}-{status.get('name').upper()}"] = status.get('key')
    #         self.status_dict = status_dict
    #
    #     return self.status_dict
    #
    # def get_customer_categories(self):
    #     if self.token.access_token is None:
    #         return None
    #     if self.categories is None:
    #         query = "SELECT * FROM customercategory WHERE isinactive = 'F'"
    #         categories = self.QUERY_CLIENT.query_api.execute_query(query=query)
    #         category_dict = {}
    #         for category in categories:
    #             category_dict[f"{category.get('name').upper()}"] = category.get('id')
    #             self.categories = category_dict
    #     return self.categories
