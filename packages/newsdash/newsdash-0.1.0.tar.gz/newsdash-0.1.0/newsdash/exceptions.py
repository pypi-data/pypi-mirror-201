class HTTPException(Exception):
    """
    Exception class for News API errors.
    """

    def __init__(
        self, message, status_code=None, error_code=None, request=None, response=None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.request = request
        self.response = response
        super().__init__(self.message)

    def __str__(self):
        msg = f"NewsAPIException: {self.message}"
        if self.status_code is not None:
            msg += f" (HTTP {self.status_code})"
        if self.error_code is not None:
            msg += f", Error Code: {self.error_code}"
        if self.request is not None:
            msg += f", Request: {self.request}"
        if self.response is not None:
            msg += f", Response: {self.response}"
        return msg

    @classmethod
    def from_response(cls, response):
        """
        Create an instance of the exception from a News API error response in JSON format.
        """
        status_code = response.get("status")
        error_code = response.get("code")
        message = response.get("message")
        request = response.get("request")
        return cls(
            message=message,
            status_code=status_code,
            error_code=error_code,
            request=request,
            response=response,
        )
