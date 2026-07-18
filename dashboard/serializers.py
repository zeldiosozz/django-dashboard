from rest_framework import serializers
from .models import (
    Invoices,
    Customers,
    Revenue,
      
	)
class InvoicesSerializer(serializers.ModelSerializer):
	name = serializers.CharField(source="customer.name", read_only=True)
	email = serializers.CharField(source="customer.email", read_only=True)
	image_url = serializers.CharField(source = "customer.image_url", read_only=True)
	class Meta:
		model = Invoices
		fields = [
			"id",
            "customer",
			"amount",
			"status",
			"date",
			"name",
			"email",
			"image_url",
		]
		read_only_fields=["id"]


class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = "__all__"
class CustomersFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ["id", "name"]
class CustomersTableSerializer(serializers.ModelSerializer):
		total_invoices = serializers.IntegerField()
		total_pending = serializers.IntegerField()
		total_paid = serializers.IntegerField()
		class Meta:
			model = Customers
			fields = [
			"id",
			"name",
			"email",
			"image_url",
            "total_invoices",
            "total_pending",
            "total_paid",
		]


class LatestInvoicesSerializer(serializers.ModelSerializer):
        name = serializers.CharField(source="customer.name")
        email = serializers.CharField(source="customer.email")
        image_url = serializers.CharField(source="customer.image_url")
        class Meta:
             model = Invoices
             fields = ["id", "amount", "name", "email", "image_url"]

class RevenueSerializer(serializers.ModelSerializer):
      class Meta:
            model = Revenue
            fields = "__all__"