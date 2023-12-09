from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Vendor
from .serializers import *
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import check_password


def getobject(model, pk):
    return get_object_or_404(model, id=pk)

def get_response(flag, msg, data=[], code=200):
    response_code = status.HTTP_200_OK if code == 200 else status.HTTP_400_BAD_REQUEST
    return Response({'status':flag, 'message': msg, 'data':data}, status=response_code)


class LoginView(ObtainAuthToken):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        if not authenticate(username=request.data.get('username'),password=request.data.get('password')):
            return Response({'status':False, 'message':'username or password incorrect!'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = self.serializer_class(data={"username":request.data.get('username'),"password":request.data.get('password')},context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        u = User.objects.get(id=user.pk)
        user_obj = UserSerializer(u, many=False).data
        return Response({'status':True, 'message':'Login Successfull', 'token': token.key,'user': user_obj})

class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            u = User.objects.get(id=serializer.data.get('id'))
            u.set_password(request.data.get('password'))
            u.save()
            return Response({'status':True, 'message':'Signup successfull', 'data':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'status':False, 'message':'Signup Failed', 'data': serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class VendorProfileView(APIView):
    def _getobject(self, pk):
        return get_object_or_404(Vendor, id=pk)

    def _get_response(self, flag, msg, data=[], code=200):
        response_code = status.HTTP_200_OK if code == 200 else status.HTTP_400_BAD_REQUEST
        return Response({'status':flag, 'message': msg, 'data':data}, status=response_code)
        
    def get(self, request, vendor_id=None):
        qs = self._getobject(vendor_id) if vendor_id else Vendor.objects.all()
        data = VendorSerializer(qs, many=vendor_id is None).data
        return self._get_response(True, 'Vendor data fetched successfully', data)

    def post(self, request):
        serializer = VendorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return self._get_response(True, 'Vendor profile created', serializer.data)

        return self._get_response(False, 'Something went wrong', serializer.errors, 400)

    def put(self, request, vendor_id=None):
        qs = self._getobject(vendor_id)
        serializer = VendorSerializer(qs, request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return self._get_response(True, 'Data updated successfully', serializer.data)
        
        return self._get_response(False, 'Something went wrong', serializer.errors, 400)

    def delete(self, request, vendor_id=None):
        qs = self._getobject(vendor_id)
        qs.delete()
        return self._get_response(True, 'Vendor deleted successfully', code=200)


class VendorPerformanceView(APIView):
    def get(self,request, vendor_id=None):
        qs = getobject(model=Vendor, pk=vendor_id)
        return get_response(True, 'Data fetched successfully', VenderPerformanceSerializer(qs,many=False).data)