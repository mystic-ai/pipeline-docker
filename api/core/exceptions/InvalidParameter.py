from fastapi.exceptions import HTTPException


class InvalidParameter(HTTPException):
    """Exception raised for lack of permission

    Attributes:
        parameter_name -- Name of the parameter attempted
    """

    def __init__(
        self,
        parameter_name,
        message="Invalid parameter given",
    ):
        self.message = message
        self.parameter_name = parameter_name
        super().__init__(
            detail={"message": message, "parameter": self.parameter_name},
            status_code=400,
        )
