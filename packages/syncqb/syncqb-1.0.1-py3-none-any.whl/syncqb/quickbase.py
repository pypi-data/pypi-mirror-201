from .qb_errors import *

class QuickbaseClient:
    def __init__(self, credentials, timeout=90, database=None):
        self.username = credentials.get('username')
        self.password = credentials.get('password')
        self.realmhost = credentials.get('realmhost')
        self.base_url = credentials.get('base_url')
        self.user_token = credentials.get('user_token')
        self.timeout = timeout
        self.database = database

        if not self.base_url:
            raise QBAuthError('missing base_url')
        if not self.realmhost:
            self.realmhost = self.base_url.split('https://')[1]