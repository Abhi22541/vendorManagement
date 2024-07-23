from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import Vendor, PurchaseOrder
from rest_framework import serializers
from django.utils import timezone
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer

class VendorListCreateView(APIView):
    
    @swagger_auto_schema(
        request_body=VendorSerializer,
        responses={201: VendorSerializer},
        operation_description="Create a new vendor",
        operation_id="create_vendor"
    )
    def post(self, request, *args, **kwargs):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: VendorSerializer(many=True)},
        operation_description="List all vendors",
        operation_id="list_vendors"
    )
    def get(self, request, *args, **kwargs):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

class VendorDetailView(APIView):
    
    @swagger_auto_schema(
        responses={200: VendorSerializer},
        operation_description="Retrieve details of a specific vendor",
        operation_id="retrieve_vendor"
    )
    def get(self, request, vendor_id, *args, **kwargs):
        try:
            vendor = Vendor.objects.get(id=vendor_id)
            serializer = VendorSerializer(vendor)
            return Response(serializer.data)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=VendorSerializer,
        responses={200: VendorSerializer},
        operation_description="Update a vendor's details",
        operation_id="update_vendor"
    )
    def put(self, request, vendor_id, *args, **kwargs):
        try:
            vendor = Vendor.objects.get(id=vendor_id)
            serializer = VendorSerializer(vendor, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        responses={204: 'Vendor deleted successfully'},
        operation_description="Delete a vendor",
        operation_id="delete_vendor"
    )
    def delete(self, request, vendor_id, *args, **kwargs):
        try:
            vendor = Vendor.objects.get(id=vendor_id)
            print(vendor)
            vendor.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

class VendorPerformanceView(APIView):
    
    @swagger_auto_schema(
        responses={200: HistoricalPerformanceSerializer},
        operation_description="Retrieve a vendor's performance metrics",
        operation_id="retrieve_vendor_performance"
    )
    def get(self, request, vendor_id, *args, **kwargs):
        try:
            vendor = Vendor.objects.get(id=vendor_id)
            # Assuming performance metrics are calculated and stored in HistoricalPerformance model
            performance = vendor.historical_performances.last()
            serializer = HistoricalPerformanceSerializer(performance)
            return Response(serializer.data)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

class PurchaseOrderListCreateView(APIView):
    
    @swagger_auto_schema(
        request_body=PurchaseOrderSerializer,
        responses={201: PurchaseOrderSerializer},
        operation_description="Create a new purchase order",
        operation_id="create_purchase_order"
    )
    def post(self, request, *args, **kwargs):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: PurchaseOrderSerializer(many=True)},
        operation_description="List all purchase orders with optional filtering by vendor",
        operation_id="list_purchase_orders"
    )
    def get(self, request, *args, **kwargs):
        vendor_id = request.query_params.get('vendor')
        if vendor_id:
            purchase_orders = PurchaseOrder.objects.filter(vendor_id=vendor_id)
        else:
            purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

class PurchaseOrderDetailView(APIView):
    
    @swagger_auto_schema(
        responses={200: PurchaseOrderSerializer},
        operation_description="Retrieve details of a specific purchase order",
        operation_id="retrieve_purchase_order"
    )
    def get(self, request, po_id, *args, **kwargs):
        try:
            purchase_order = PurchaseOrder.objects.get(id=po_id)
            serializer = PurchaseOrderSerializer(purchase_order)
            return Response(serializer.data)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase Order not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=PurchaseOrderSerializer,
        responses={200: PurchaseOrderSerializer},
        operation_description="Update a purchase order",
        operation_id="update_purchase_order"
    )
    def put(self, request, po_id, *args, **kwargs):
        try:
            purchase_order = PurchaseOrder.objects.get(id=po_id)
            serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase Order not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        responses={204: 'Purchase Order deleted successfully'},
        operation_description="Delete a purchase order",
        operation_id="delete_purchase_order"
    )
    def delete(self, request, po_id, *args, **kwargs):
        try:
            purchase_order = PurchaseOrder.objects.get(id=po_id)
            purchase_order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase Order not found'}, status=status.HTTP_404_NOT_FOUND)

class AcknowledgePurchaseOrderView(APIView):
    
    @swagger_auto_schema(
        request_body=serializers.Serializer,  # Use an empty serializer if no body is needed
        responses={200: 'Acknowledgment successful'},
        operation_description="Acknowledge a purchase order",
        operation_id="acknowledge_purchase_order"
    )
    def post(self, request, po_id, *args, **kwargs):
        try:
            po = PurchaseOrder.objects.get(id=po_id)
            po.acknowledgment_date = timezone.now()
            po.save()
            return Response({'status': 'acknowledged'}, status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase Order not found'}, status=status.HTTP_404_NOT_FOUND)
