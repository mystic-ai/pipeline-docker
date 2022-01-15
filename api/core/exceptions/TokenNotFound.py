from fastapi.exceptions import HTTPException


class TokenNotFound(HTTPException):
    """Exception raised for token not being found
    Attributes:
        token -- Token attempting to execute a function
    """

    def __init__(
        self,
        token,
        message="Token not found",
    ):
        self.token = token
        self.message = message
        super().__init__(
            detail={"message": self.message, "token": self.token}, status_code=403
        )
