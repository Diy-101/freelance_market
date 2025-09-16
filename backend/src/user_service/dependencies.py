from . import PyJWTService
from .services import MainUserService


def get_pyjwt_service():
    return PyJWTService()


def get_main_service():
    return MainUserService()
