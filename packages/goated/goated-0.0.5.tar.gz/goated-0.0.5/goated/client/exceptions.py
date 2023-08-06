class NoTokenProvided(Exception):
    def __init__(self,):
        self.message = f'No authentication token was provided.'
        super().__init__(self.message)

class GoatedApiException(Exception):
    def __init__(self, response):
        self.message = f"The server returned an error. \n {response} "
        super().__init__(self.message)
