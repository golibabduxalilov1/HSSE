from rest_framework.exceptions import APIException
from rest_framework import status


class CustomAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Xatolik yuz berdi'
    default_code = 'error'


class PermissionDenied(CustomAPIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Ushbu amalni bajarish uchun sizda ruxsat yo'q"
    default_code = 'permission_denied'


class NotFound(CustomAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Resurs topilmadi'
    default_code = 'not_found'


class ValidationError(CustomAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Ma'lumotlarni tekshirishda xatolik"
    default_code = 'validation_error'


class AlreadyExists(CustomAPIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Resurs allaqachon mavjud'
    default_code = 'already_exists'