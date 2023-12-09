from django.test import TestCase

from django.urls import reverse
from django.contrib.auth.models import User
from purchase_order.models import PurchaseOrder
from rest_framework.test import APIClient
from vendor_profile.models import Vendor

class VendorProfileEndPointTests(TestCase):
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

    def test_post_vendor(self):
        url = reverse('vendor')
        data = {'name':'Prashant Paliwal', 'contact_details':'9759525301', 'address':'Noida', 'vendor_code':'80934',}
        response = self.client.post(url, data, headers={'Authorization': self.token})
        self.assertEqual(response.status_code, 200)

    def test_get_vender(self):
        v_id = Vendor.objects.all().last().id
        url = f'/api/vendors/{v_id}/'
        response = self.client.get(url, headers={'Authorization': self.token})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(url, headers={'Authorization': self.token})
        self.assertEqual(response.status_code, 200)

    def test_put_vendor(self):
        data = {'name':'Prashant Paliwal', 'contact_details':'9759525301', 'address':'Noida', 'vendor_code':'80934',}
        v_id = Vendor.objects.all().last().id
        url = f'/api/vendors/{v_id}/'
        response = self.client.put(url, data=data, headers={'Authorization': self.token}, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_vendor(self):
        v_id = Vendor.objects.all().last().id
        url = f'/api/vendors/{v_id}/'
        response = self.client.delete(url, headers={'Authorization': self.token})
        self.assertEqual(response.status_code, 200)

    def test_get_performance(self):
        v_id = Vendor.objects.all().last().id
        url = f'/api/vendors/{v_id}/performance'
        response = self.client.get(url, headers={'Authorization': self.token})
        self.assertEqual(response.status_code, 200)