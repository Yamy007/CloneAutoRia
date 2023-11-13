from rest_framework.response import Response
from rest_framework.views import exception_handler

from core.enum.error_enum import ErrorEnum
from core.exceptions.jwt_exception import JWTException


def error_handler(exc: Exception, context: dict) -> Response:
    handlers = {
        "JWTException": _jwt_validation_error,
        "BlockException": _block_exception_error,
        "PremiumException": _prem_exception_error,
        "ViewException": _view_exception_error,
    }

    response = exception_handler(exc, context)
    exc_class = exc.__class__.__name__

    if exc_class in handlers:
        return handlers[exc_class](exc, context)

    return response


def _jwt_validation_error(exc: JWTException, context: dict) -> Response:
    return Response(*ErrorEnum.JWT.value)


def _block_exception_error(exc, context: dict) -> Response:
    return Response(*ErrorEnum.BLOCK.value)


def _prem_exception_error(exc, context: dict) -> Response:
    return Response(*ErrorEnum.PREM.value)


def _view_exception_error(exc, context: dict) -> Response:
    return Response(*ErrorEnum.VIEW.value)
