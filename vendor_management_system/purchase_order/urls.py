from django.urls import path
from . import views

urlpatterns = [
	path('purchase_orders/', views.OrderAPIView.as_view(), name='order'),
	path('purchase_orders/<int:po_id>/', views.OrderAPIView.as_view(), name='po_by_id'),
	
	path('purchase_orders/<int:po_id>/acknowledgment', views.AcknowledgePOView.as_view(), name='acknowledgment'),
			
]