from rest_framework.exceptions import APIException


class NoContentException(APIException):
    status_code = 204
    default_detail = "No content available for this resource"
