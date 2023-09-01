class APIRequestException(Exception):
    """Raised when the API request fails."""

    def __init__(self, status_code=None, endpoint=None, api_message=None, *args):
        super().__init__(*args)
        self.status_code = status_code
        self.endpoint = endpoint
        self.api_message = api_message

    def __str__(self):
        message = "API Request Failed"

        if self.status_code is not None:
            message += f" with status code {self.status_code}"

        if self.endpoint is not None:
            message += f" for endpoint {self.endpoint}"

        if self.api_message is not None:
            message += f": {self.api_message}"
        else:
            message += "."

        return message
