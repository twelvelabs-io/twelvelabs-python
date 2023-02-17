class APIError(Exception):
    def __init__(self, message, code, docs_url=None):
        self.message = message
        self.code = code
        self.docs_url = docs_url

        super().__init__(f"{message} ({code})")
