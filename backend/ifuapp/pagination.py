from rest_framework import pagination, response


class EnhancedPageNumberPagination(pagination.PageNumberPagination):
    """
    Add extra stats to response.
    """
    # page_size = 10000
    page_size_query_param = 'page_size'
    page_size = 30
    # max_page_size = 1000

    def get_paginated_response(self, data):
        # previous_page = None if not self.page.has_previous(
        # ) else self.page.previous_page_number()
        # next_page = None if not self.page.has_next() else self.page.next_page_number()
        return response.Response({
            'count': self.page.paginator.count,
            'page_size': self.get_page_size(self.request),
            'total_pages': self.page.paginator.num_pages,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
