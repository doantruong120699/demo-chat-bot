from drf_yasg import openapi
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "limit"
    max_page_size = 100
    page_query_param = "page"

    def get_paginated_response_schema(self, schema):
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING, example="List of users has been fetched."
                ),
                "status_code": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                "data": {
                    "items": schema,
                    "meta": {
                        "pagination": {
                            "page": openapi.Schema(
                                type=openapi.TYPE_INTEGER, example=2
                            ),
                            "limit": openapi.Schema(
                                type=openapi.TYPE_INTEGER, example=10
                            ),
                            "total_pages": openapi.Schema(
                                type=openapi.TYPE_INTEGER, example=5
                            ),
                            "total_items": openapi.Schema(
                                type=openapi.TYPE_INTEGER, example=49
                            ),
                        }
                    },
                },
            },
        )

    def get_paginated_response(self, data, message="Data has been fetched."):
        return Response(
            {
                "message": message,
                "status_code": 200,
                "data": {
                    "items": data,
                    "meta": {
                        "pagination": {
                            "page": self.page.number,
                            "limit": self.page_size,
                            "total_pages": self.page.paginator.num_pages,
                            "total_items": self.page.paginator.count,
                        }
                    },
                },
            }
        )

    def get_paginated_meta_response(self):
        return Response(
            {
                "pagination": {
                    "page": self.page.number,
                    "limit": self.page_size,
                    "total_pages": self.page.paginator.num_pages,
                    "total_items": self.page.paginator.count,
                }
            }
        )
