# from django.shortcuts import render
from django.db.models import Q, Count, Sum, Case, When, IntegerField
from .serializers import (
    InvoicesSerializer,
    CustomersSerializer,
    CustomersFieldSerializer,
    CustomersTableSerializer,
    LatestInvoicesSerializer,
    RevenueSerializer,
    
    )
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from .models import (Invoices, Customers, Revenue,)
from rest_framework.viewsets import ModelViewSet
from .pagination import InvoicesPagination
# Create your views here.

class InvoiceViewSet(ModelViewSet):
    queryset = Invoices.objects.select_related("customer")
    serializer_class = InvoicesSerializer
    pagination_class = InvoicesPagination
    search_fields = ["customer__name", "customer__email", "status", "amount", "date"]
    ordering_fields = ["date", "amount"]
    @action(detail=True, methods=["get"])
    def edit_data(self, request, pk):
        invoice = self.get_object()
        serializer = InvoicesSerializer
        return(serializer.data)

class CustomerViewSet(ModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = CustomersSerializer
    # pagination_class = CustomersPagination
    @action(detail=False, methods=["get"])
    def fields(self, request):
        customers = Customers.objects.order_by("name") 
        serializer = CustomersFieldSerializer(customers, many=True)
        return Response(serializer.data)
    @action(detail=False, methods=["get"])
    def filtered(self, request):
        query = request.GET.get("search", "")
        customers = Customers.objects.all() 
        if query:
            customers = customers.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query)
            )

        customers = customers.annotate(
            total_invoices = Count("invoices"),
            total_pending =Sum(
                Case(
                When(invoices__status="pending", then="invoices__amount"),
                default=0,
                output_field=IntegerField(),
                    )
                            ),
        
            total_paid = Sum(
                Case(
                    When(invoices__status="paid", then="invoices__amount"),
                    default=0,
                    output_field = IntegerField(),
                )
            ))
        customers = customers.order_by("name")
        serializer = CustomersTableSerializer(customers, many=True)
        return Response(serializer.data)


              


@api_view(["GET"])
def dashboard_cards(request):
    number_of_customers = Customers.objects.count()
    number_of_Invoices = Invoices.objects.count()
    invoice_status = Invoices.objects.aggregate(
        paid=Sum(
            Case(
                When(status="paid", then="amount"),
                default=0,
                output_field=IntegerField(),
            )
        ),
        pending=Sum(
            Case(
                When(status="pending", then="amount"),
                defualt =0,
                output_field=IntegerField(),
            )
        )
    )
    return Response({
        "numberOfCustomers":number_of_customers,
        "numberOfInvoices":number_of_Invoices,
        "totalPaidInvoices": invoice_status["paid"] or 0,
        "totalPendingInvoices": invoice_status["pending"] or 0,
        })


@api_view(["GET"])
def latest_invoices(request):
    invoices = (Invoices.objects
                .select_related("customer")
                .order_by("-date")[:5])
    serializer = LatestInvoicesSerializer
    return(serializer.data)


@api_view(["GET"])
def revenues_list(request):
    revenue = Revenue.objects.all()
    serializer = RevenueSerializer(revenue, many=True)
    return Response(serializer.data)
# @api_view(["GET"])sdd
# def invoices_view(request):
#     query = request.GET.get("query", "")
    
#     invoices = Invoices.objects.select_related("customer")
#     if query:
#         invoices = invoices.filter(
#             Q(customer__name__icontains=query)
#             | Q(customer__email__icontains=query)
#             | Q(status__icontains=query)
#             | Q(amount__icontains=query)
#             | Q(date__icontains=query)
#         )
#     serializer = InvoicesSerializer(invoices, many=True)

#     return Response(serializer.data)

# @api_view(["GET"])
# def customers_view(request):
#     customers = Customers.objects.all()
#     serializer = CustomersSerializer(customers, many=True)
#     return Response(serializer.data)

