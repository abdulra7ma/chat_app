from rest_framework import pagination


class APICustomPagination(pagination.LimitOffsetPagination):
    max_limit = 20
    default_limit = 5
