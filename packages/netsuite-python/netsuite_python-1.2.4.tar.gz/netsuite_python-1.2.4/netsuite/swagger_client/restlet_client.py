from netsuite import swagger_client


class RestletClient:
    def __init__(self, netsuite):
        self.netsuite = netsuite
        self.configuration = swagger_client.Configuration()
        self.configuration.token = netsuite.storage.get_token(netsuite.app_name)
        self.configuration.token_refresh_hook = self.refresh_token
        self.configuration.app_name = netsuite.netsuite_app_name
        self.configuration.host = f"https://{self.configuration.app_name}.restlets.api.netsuite.com/app/site/hosting/restlet.nl"
        self.api_client = swagger_client.ApiClient(configuration=self.configuration)
        self.restlet_api = swagger_client.RestletApi(api_client=self.api_client)

        # self.contact_api = swagger_client.ContactApi(api_client=self.api_client)
        # self.customer_api = swagger_client.CustomerApi(api_client=self.api_client)
        # self.message_api = swagger_client.MessageApi(api_client=self.api_client)


    def refresh_token(self):
        self.configuration.token = self.netsuite.get_token()
        return self.configuration.token