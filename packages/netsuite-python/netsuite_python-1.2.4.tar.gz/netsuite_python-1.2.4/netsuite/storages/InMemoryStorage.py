from netsuite.NetsuiteToken import NetsuiteToken
from netsuite.storages import BaseStorage


class InMemoryStorage(BaseStorage):
    tokens: dict = {}

    def __init__(self):
        super().__init__()

    def get_token(self, app) -> NetsuiteToken:
        try:
            if app in self.tokens:
                return self.tokens[app]
        except Exception as e:
            pass
        return NetsuiteToken()

    def save_token(self, app: str, token: NetsuiteToken) -> bool:
        try:
            self.tokens[app] = token
            return True
        except Exception as e:
            pass
        return False
