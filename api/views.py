from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from myapp.models import Vendor, PurchaseOrder
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from .serializers import VendorSerializer, POSerializer, AckSerializer, QualityRateSerializer
from .metrics import PerformanceMetrics

def handle_not_found_error(resource_name):
    return Response({"message": f"No {resource_name} found with specified ID"}, status=status.HTTP_404_NOT_FOUND)

def handle_internal_server_error(exception):
    return Response({"message": str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_vendor_or_404(vendor_id):
    return get_object_or_404(Vendor, id=vendor_id)

def get_order_or_404(order_id):
    return get_object_or_404(PurchaseOrder, id=order_id)

class VendorViewCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            serializer = VendorSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return handle_internal_server_error(e)

class VendorDetailsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, vendor_id):
        try: 
            vendor = get_vendor_or_404(vendor_id)
            serializer = VendorSerializer(vendor)
            return Response(serializer.data)
        except Exception as e:
            return handle_not_found_error("Vendor")

    def put(self, request, vendor_id):
        try: 
            vendor = get_vendor_or_404(vendor_id)
            serializer = VendorSerializer(vendor, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return handle_internal_server_error(e)
    
    def delete(self, request, vendor_id):
        try:
            vendor = get_vendor_or_404(vendor_id)
            vendor.delete()
            return Response({"message": "Vendor deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return handle_internal_server_error(e)

class POViewCreateAPI(APIView): 
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vendor_id = request.query_params.get('vendor_id')
        if vendor_id is not None:
            try:
                vendor = Vendor.objects.get(id=vendor_id)
            except Vendor.DoesNotExist:
                return handle_not_found_error("Vendor")
            orders = PurchaseOrder.objects.filter(vendor=vendor)
        else:
            orders = PurchaseOrder.objects.all()

         # Serialize queryset to JSON
        serializer = POSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            serializer = POSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({"message": "Vendor ID must be provided. ('vendor' : id)"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return handle_internal_server_error(e)

class PODetailsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, po_id):
        try: 
            order = get_order_or_404(po_id)
            serializer = POSerializer(order)
            return Response(serializer.data)
        except Exception as e:
            return handle_not_found_error("Purchase Order")
    
    def put(self, request, po_id):
        try: 
            order = get_order_or_404(po_id)
            serializer = POSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return handle_internal_server_error(e)
    
    def delete(self, request, po_id):
        try:
            order = get_order_or_404(po_id)
            order.delete()
            return Response({"message": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return handle_internal_server_error(e)

class PerformanceMetricsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, vendor_id):
        try:
            vendor = get_vendor_or_404(vendor_id)
            metrics = PerformanceMetrics()
            data = metrics.get_all_metrics(vendor.id)
            return Response(data, status=status.HTTP_200_OK)  
        except Exception as e:
            return handle_internal_server_error(e)

class VendorAcknowledge(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, po_id):
        try: 
            order = get_order_or_404(po_id)
            serializer = AckSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                PerformanceMetrics().update_vendor_fields(order.vendor)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return handle_internal_server_error(e)
        
class QualityRating(APIView):
    
    def post(self, request, po_id):
        try:
            order = get_order_or_404(po_id)
            serializer = QualityRateSerializer(order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                PerformanceMetrics().update_vendor_fields(order.vendor)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return handle_internal_server_error(e)
