from fastapi.exceptions import HTTPException


class RequestFailed(HTTPException):
    """Exception raised for request failing

    Attributes:
    """

    def __init__(
        self,
        message="Request failed",
    ):
        self.message = message
        super().__init__(detail=self.message, status_code=400)
