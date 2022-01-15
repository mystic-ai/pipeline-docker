from fastapi.exceptions import HTTPException


class PermissionNotGranted(HTTPException):
    """Exception raised for lack of permission

    Attributes:
    """

    def __init__(
        self,
        message="Token doesn't have permission to execute function",
    ):
        self.message = message
        super().__init__(detail=self.message, status_code=403)
