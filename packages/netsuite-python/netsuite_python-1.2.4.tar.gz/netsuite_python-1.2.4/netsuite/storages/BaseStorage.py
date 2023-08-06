from netsuite.Netsuite import NetsuiteToken


class BaseStorage:
    app: str = None

    def __init__(self):
        pass

    def get_token(self, app) -> NetsuiteToken:
        raise NotImplementedError()

    def save_token(self, app: str, token: NetsuiteToken) -> bool:
        raise NotImplementedError()
