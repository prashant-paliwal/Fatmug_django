from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer
from vendor_profile.models import Vendor

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from datetime import datetime
from django.db.models import Avg, Value, F, ExpressionWrapper, fields

from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.db.models.functions import Coalesce

class OrderAPIView(APIView):
    def _getobject(self, pk):
        return get_object_or_404(PurchaseOrder, id=pk)

    def _get_response(self, flag, msg, data=[], code=200):
        response_code = status.HTTP_200_OK if code == 200 else status.HTTP_400_BAD_REQUEST
        return Response({'status':flag, 'message': msg, 'data':data}, status=response_code)
        
    def get(self,request, po_id=None):
        if po_id:
            qs = self._getobject(po_id) # Get Purchase order object by id
        else:
            vendor_id = request.GET.get('vendor_id')
            if vendor_id:
                vendor = get_object_or_404(Vendor, id=vendor_id)
                qs = PurchaseOrder.objects.filter(vendor=vendor) # Filter Purchase order object by vendor id
            else:
                qs = PurchaseOrder.objects.all().order_by('-id')
        
        data = PurchaseOrderSerializer(qs, many=po_id is None).data
        return self._get_response(True, 'Order data fetched successfully', data)

    def post(self,request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return self._get_response(True,'Order created successfull',serializer.data)

        return self._get_response(False,'Something went wrong', serializer.errors, 400)

    def put(self,request, po_id=None):
        qs = self._getobject(po_id)
        serializer = PurchaseOrderSerializer(qs,request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return self._get_response(True, 'Data updated successfully', PurchaseOrderSerializer(qs).data)

        return self._get_response(False, 'Something went wrong', serializer.errors, 400)

    def delete(self,request, po_id=None):
        qs = self._getobject(po_id)
        qs.delete()
        
        return self._get_response(True, 'Order deleted successfully', code=200)


#Signal user after PurchaseOrder save

@receiver(post_save, sender=PurchaseOrder)
def po_post_save(sender, instance, created, **kwargs):
    if not created:
        if instance.status=='completed':
            vendor = instance.vendor
            qs = PurchaseOrder.objects.filter(vendor=vendor, status="completed")

            # Update On Time Delivery Rate
            on_time_po = qs.filter(actual_delivery_date__lte=F('delivery_date')).count() # On time order count
            total_po_delivered = qs.count()  # Total order count
            
            try: 
                on_time_delivery_rate = on_time_po/total_po_delivered
                vendor.on_time_delivery_rate = on_time_delivery_rate
                vendor.save()
            except ZeroDivisionError:
                pass

            # Updated quality_rating_avg 
            if instance.quality_rating:
                # Find avg using coalesce handing null value
                vendor.quality_rating_avg = qs.aggregate(avg_rating=Avg(Coalesce('quality_rating', Value(0.0))))['avg_rating']
                vendor.save()

        # Update fulfilment rate and run on any po status change
        successfully_fullified = qs.count()
        total_po_issued = PurchaseOrder.objects.filter(vendor=instance.vendor).count()

        try:
            fulfillment_rate = successfully_fullified/total_po_issued
        except ZeroDivisionError as e:
            return e

class AcknowledgePOView(APIView):
    def post(self, request, po_id=None):
        po = get_object_or_404(PurchaseOrder, id=po_id)
        po.acknowledgment_date = datetime.now()
        po.save()

        # Calculate average response time
        qs = PurchaseOrder.objects.filter(vendor=po.vendor)
        time_difference = qs.annotate(time_difference=ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=fields.DurationField()))
        average_rsp_time = time_difference.aggregate(Avg('time_difference'))['time_difference__avg']
        
        po.vendor.average_response_time = average_rsp_time.total_seconds() # Save average response time in seconds
        po.vendor.save()

        return Response({'status':True, 'message':'Order acknowledgment successfull', 'data': PurchaseOrderSerializer(po,many=False).data},status=status.HTTP_200_OK)