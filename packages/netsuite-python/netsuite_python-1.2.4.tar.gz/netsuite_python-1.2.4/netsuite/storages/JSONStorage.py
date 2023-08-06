import json
from json import JSONDecodeError
from pathlib import Path

from netsuite.NetsuiteToken import NetsuiteToken
from netsuite.storages import BaseStorage


class JSONStorage(BaseStorage):
    def __init__(self, storage_path: Path = None):
        self.storage_path = storage_path
        super().__init__()

    def load_tokens(self) -> dict:
        tokens = {}
        try:
            with open(self.storage_path, "r") as f:
                tokens = json.load(f)
        except FileNotFoundError as e:
            with open(self.storage_path, "w") as f:
                json.dump(tokens, f, indent=4, ensure_ascii=True)
        except JSONDecodeError as e:
            with open(self.storage_path, "w") as f:
                json.dump(tokens, f, indent=4, ensure_ascii=True)
        return tokens

    def get_token(self, app) -> NetsuiteToken:
        tokens = self.load_tokens()
        try:
            if app in tokens:
                return NetsuiteToken(**tokens[app])
        except Exception as e:
            pass
        return NetsuiteToken()

    def save_token(self, app: str, token: NetsuiteToken) -> bool:
        try:
            tokens = self.load_tokens()
            tokens[app] = token.__dict__
            with open(self.storage_path, "w") as f:
                json.dump(tokens, f, indent=4, ensure_ascii=True)
            return True
        except Exception as e:
            pass
        return False

    def list_tokens_by_name(self):
        tokens = self.load_tokens()
        return list(tokens.keys())
