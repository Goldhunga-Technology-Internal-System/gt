from typing import Any

from fastapi import Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from starlette.status import HTTP_204_NO_CONTENT


class CustomSuccessResponseSchema[T](BaseModel):
    """
    Custom Error Response Schema for every api
    """

    success: bool
    data: T | list[T] | None
    message: str


class CustomErrorResponseSchema[T](BaseModel):
    """
    Custom Error Response Schema for every api
    """

    success: bool
    errors: T | list[T] | None
    error: str


class CustomResponse:
    """
    list of customer Response methods
    """

    @staticmethod
    def success(
        data: Any = None,
        message: str = "Successful",
        status_code: int = status.HTTP_200_OK,
    ):
        """
        On sucess it returns the success=True with data and message
        """
        if status_code == HTTP_204_NO_CONTENT:
            return Response(status_code=status_code)
        if ":" in message:
            message = message.split(":")[1]
        content = {"success": True, "message": message, "data": jsonable_encoder(data)}
        return JSONResponse(status_code=status_code, content=content)

    @staticmethod
    def error(
        errors: Any | None = None,
        error: str | None = "Unsuccessful",
        status_code: int | None = status.HTTP_400_BAD_REQUEST,
    ):
        """
        On error it returns the success=False and with data and message
        """
        content = {"success": False, "error": error, "errors": jsonable_encoder(errors)}
        return JSONResponse(
            status_code=status_code or status.HTTP_400_BAD_REQUEST, content=content
        )

    @staticmethod
    def redirect(url: str, status_code: int = status.HTTP_302_FOUND):
        """
        On redirect it returns the success=True with data and message
        """
        return RedirectResponse(
            status_code=status_code,
            url=url,
        )
