from lxml import etree, html

class QBError(Exception):
    def __init__(self, message, response=None):
        self.message = message
        self.response = response
    def __str__(self):
        details = self._get_details(self.response)
        
        if details:
            return f"{self.message}, Response details: {details}"
        return self.message
    
    def _get_details(self, response):
        if response is None:
            return None
        content_type = response.headers.get('content-type')
        if 'application/json' in content_type:
            return response.json()
        else:
            try:
                tree = html.fromstring(response.content)
                title = tree.findtext('.//title')
                return title
            except Exception as e:
                pass
        
        return None
    
class QBAuthError(QBError):
    def __init__(self, message):
        super().__init__(message)

class QBConnectionError(QBError):
    def __init__(self, message):
        super().__init__(message)

class QBResponseError(QBError):
    def __init__(self, message, response=None):
        super().__init__(message, response)

class QuickbaseError(QBError):
    def __init__(self, message, response=None):
        super().__init__(message, response)
    