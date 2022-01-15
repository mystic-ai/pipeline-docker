from fastapi.exceptions import HTTPException


class TokenNotProvided(HTTPException):
    """Exception raised for lack of token

    Attributes:

        function_name -- Name of the function attempted to execute
    """

    def __init__(
        self,
        message="Token not provided",
    ):
        super().__init__(detail=message, status_code=401)
