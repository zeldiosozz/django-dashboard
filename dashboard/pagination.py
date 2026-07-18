from rest_framework.pagination import PageNumberPagination

class InvoicesPagination(PageNumberPagination):
    page_size=6
# class CustomersPagination(PageNumberPagination):
#     page_size=6