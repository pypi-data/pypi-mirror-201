from netsuite import swagger_client


class RestClient:
    def __init__(self, netsuite):
        self.netsuite = netsuite
        self.configuration = swagger_client.Configuration()
        self.configuration.token = netsuite.storage.get_token(netsuite.app_name)
        self.configuration.token_refresh_hook = self.refresh_token
        self.configuration.app_name = netsuite.netsuite_app_name
        self.configuration.host = f"https://{self.configuration.app_name}.suitetalk.api.netsuite.com/services/rest/record/v1"
        self.api_client = swagger_client.ApiClient(configuration=self.configuration)
        self.contact_api = swagger_client.ContactApi(api_client=self.api_client)
        self.customer_api = swagger_client.CustomerApi(api_client=self.api_client)
        self.message_api = swagger_client.MessageApi(api_client=self.api_client)


    def refresh_token(self):
        self.configuration.token = self.netsuite.get_token()
        return self.configuration.token

class QueryClient:
    def __init__(self, netsuite):
        self.netsuite = netsuite
        self.configuration = swagger_client.Configuration()
        self.configuration.token = netsuite.storage.get_token(netsuite.app_name)
        self.configuration.token_refresh_hook = self.refresh_token
        self.configuration.app_name = netsuite.netsuite_app_name
        self.configuration.host = f"https://{self.configuration.app_name}.suitetalk.api.netsuite.com/services/rest/query/v1/suiteql"
        self.query_api_client = swagger_client.ApiClient(configuration=self.configuration)
        self.query_api = swagger_client.QueryApi(api_client=self.query_api_client)

    def refresh_token(self):
        self.configuration.token = self.netsuite.get_token()
        return self.configuration.token



