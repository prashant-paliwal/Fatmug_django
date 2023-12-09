from django.test import TestCase

from django.urls import reverse
from django.contrib.auth.models import User
from purchase_order.models import PurchaseOrder
from rest_framework.test import APIClient
from vendor_profile.models import Vendor

class OrderEndPointTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='prashantpaliwal211@gmail.com', password='Password@123')
        self.v_id = Vendor.objects.create(name='name', contact_details='contact_details', address='address', vendor_code='vendor_code',)
        self.po = PurchaseOrder.objects.create(po_number='123', vendor=self.v_id, items='{"id": 1, "name":"product"}', delivery_date='2023-12-08', quantity='4', status='pending')
        self.token = self.get_auth_token()
        self.client = APIClient()

    def get_auth_token(self):
        url = reverse('login')
        data = {'username': 'prashantpaliwal211@gmail.com', 'password': 'Password@123'}
        response = self.client.post(url, data)
        token = response.data.get('token')
        return f'Token {token}'

    def test_post_po(self):
        url = reverse('order')
        v_id = Vendor.objects.all().last().id
        data = {'po_number':'1234', 'vendor': v_id, 'items':'{"id": 1, "name":"product"}', 'delivery_date':'2023-12-08', 'quantity':'4', 'status':'pending' }

        response = self.client.post(url, data=data, headers={'Authorization': self.token}, format='json')
        self.assertEqual(response.status_code, 200)

    def test_get_po(self):
        # Re
        url = reverse('order')
        response = self.client.get(url, headers={'Authorization': self.token})
        self.assertEqual(response.status_code, 200)

        po_id=PurchaseOrder.objects.all().last().id
        url = f'/api/purchase_orders/{po_id}/'
        response = self.client.get(url, headers={'Authorization': self.token})
        self.assertEqual(response.status_code, 200)   

    def test_put_po_by_pk(self):
        data = {'delivery_date':'2023-12-10', 'status':'completed', 'quality_rating':"4"}
        po_id = PurchaseOrder.objects.all().last().id
        url = f'/api/purchase_orders/{po_id}/'
        response = self.client.put(url, headers={'Authorization': self.token}, data=data, format='json')
        self.assertEqual(response.status_code, 200)