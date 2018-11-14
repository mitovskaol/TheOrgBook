from collections import OrderedDict
import logging

from django.core.paginator import Paginator
from rest_framework.pagination import BasePagination, PageNumberPagination
from rest_framework.response import Response

LOGGER = logging.getLogger(__name__)


class EnhancedPageNumberPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("total", self.page.paginator.count),
                    ("page_size", self.page_size),
                    ("page", self.page.number),
                    ("first_index", self.page.start_index()),
                    ("last_index", self.page.end_index()),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )


class NullDjangoPaginator(Paginator):
    @property
    def count(self):
        return None

class ResultLimitPagination(BasePagination):
    django_paginator_class = NullDjangoPaginator
    result_limit = 10

    def paginate_queryset(self, queryset, request, view=None):
        return list(queryset[:self.result_limit])

    def get_paginated_response(self, data):
        LOGGER.info("data: %s", data)
        count = len(data)
        return Response(
            OrderedDict(
                [
                    ("total", count),
                    ("first_index", 1),
                    ("last_index", count),
                    ("results", data),
                ]
            )
        )
