from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='signup'),

	path('vendors/', VendorProfileView.as_view(), name='vendor'),
	path('vendors/<int:vendor_id>/', VendorProfileView.as_view(), name='vendor_by_id'),
	
	path('vendors/<int:vendor_id>/performance', VendorPerformanceView.as_view(), name='performance_evaluation')
			
]