from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from pharmacy.serializers import PharmacyRegistrationSerializer,PharmacyProfileSerializer,ResetPasswordSerializerPharma,MedicineSerializer,OfferSerializer
from django.contrib.auth import authenticate
from pharmacy.renders import PharmacyRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
import jwt, datetime
from rest_framework.exceptions import AuthenticationFailed
from pharmacy.models import Pharmacy,Medicine,Offers
#from rest_framework.renderers import JSONRenderer, YAMLRenderer
# Create your views here.

def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

#PharmacyRegisterView
class PharmacyRegistrationView(APIView):
   renderer_classes=[PharmacyRenderer]
   def post(self, request, format=None):
    serializer = PharmacyRegistrationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        pharmacy = serializer.save()
        return Response({'msg':'Registration Of Pharmacy Successfully'}, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 



#login Pharmacy View
class PharmacyLoginView(APIView):
  def post(self, request):
    if 'email' not in request.data and 'password' not in request.data:
      return Response({"errors": {"email": ["this field is required"], "password": ["this field is required"]}}, status=status.HTTP_400_BAD_REQUEST)
    
    elif 'email' not in request.data:
      return Response({"errors": {"email": ["this field is required"]}}, status=status.HTTP_400_BAD_REQUEST)
    
    elif 'password' not in request.data:
      return Response({"errors": {"password": ["this field is required"]}}, status=status.HTTP_400_BAD_REQUEST)
    
    email = request.data['email']
    password = request.data['password']

    pharmacy = Pharmacy.objects.filter(email=email).first()

    if pharmacy is None:
        raise AuthenticationFailed('Pharmacy Account not found!')

    if not pharmacy.check_password(password):
        raise AuthenticationFailed('Incorrect password!')

    payload = {
        'id': pharmacy.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, 'secret', algorithm='HS256')

    response = Response()

    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
        'token': token,
        'login': True
    }
    return response

# pharmacy profile
class PharmacyProfileView(APIView):
  renderer_classes = [PharmacyRenderer]
  # permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    token = request.COOKIES.get('jwt')
    if not token:
      raise AuthenticationFailed('Authentication credentials were not provided.')
    try:
      payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('Authentication credentials were not provided.')
    
    user = Pharmacy.objects.filter(id=payload['id']).first()
    if not user:
      raise AuthenticationFailed('User Account not found!')
    serializer = PharmacyProfileSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

#changePassword for pharmacy
class RestPasswordView(APIView):
  renderer_classes = [PharmacyRenderer]
  # permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    # serializer = ResetPasswordSerializer(data=request.data, context={'user':request.user})
    if 'old_password' not in request.data and 'new_password' not in request.data:
      return Response({"errors": {"old_password": ["this field is required"], "new_password": ["this field is required"]}}, status=status.HTTP_400_BAD_REQUEST)
    
    elif 'old_password' not in request.data:
      return Response({"errors": {"old_password": ["this field is required"]}}, status=status.HTTP_400_BAD_REQUEST)
    
    elif 'new_password' not in request.data:
      return Response({"errors": {"new_password": ["this field is required"]}}, status=status.HTTP_400_BAD_REQUEST)
    
    old_password = request.data['old_password']
    new_password = request.data['new_password']
    token = request.COOKIES.get('jwt')
    if not token:
      raise AuthenticationFailed('Authentication credentials were not provided.')
    try:
      payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('Authentication credentials were not provided.')
    
    user = Pharmacy.objects.filter(id=payload['id']).first()
    if not user:
      raise AuthenticationFailed('User Account not found!')
    
    flag = user.check_password(old_password)

    if not flag:
      return Response({"errors": {"old_password": ["this field is invalid"]}}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    return Response({"success":True, "message": "Password is Rest Successfully"}, status=status.HTTP_200_OK)
  



#Crud Opertaion For Medicine APIView
class MedicineDetailes(APIView):
   #serializer_class=MedicineSerializer
   def get(self,request):
      obj=Medicine.objects.all()
      serializer=MedicineSerializer(obj,many=True)
      return Response(serializer.data,status=status.HTTP_200_OK)
   
   def post(self,request):
      serializer=MedicineSerializer(data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data,status=status.HTTP_201_CREATED)
      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#For Get&Put&Patch&Delete On object
class MedicineInfo(APIView):
   def get(self,request,id):
      try:
         obj=Medicine.objects.get(id=id)
      except Medicine.DoesNotExist:
         msg={"msg":"This Medicine Type Not Found"} 
         return Response(msg,status=status.HTTP_404_NOT_FOUND)
      serializer =MedicineSerializer(obj)
      return Response(serializer.data,status=status.HTTP_200_OK)

   def put(self,request,id):
      try:
         obj=Medicine.objects.get(id=id)
      except Medicine.DoesNotExist:
         msg={"msg":"Not Found "}
         return Response(msg,status=status.HTTP_404_NOT_FOUND)
      serializer =MedicineSerializer(obj,data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data,status=status.HTTP_205_RESET_CONTENT)
      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
   
   def patch(self,request,id):
      try:
         obj=Medicine.objects.get(id=id)
      except Medicine.DoesNotExist:
         msg={"msg":"Not Found "}
         return Response(msg,status=status.HTTP_404_NOT_FOUND)
      serializer =MedicineSerializer(obj,data=request.data,partial=True)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data,status=status.HTTP_205_RESET_CONTENT)
      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
   
   def delete(self,request,id):
      try:
         obj=Medicine.objects.get(id=id)
      except Medicine.DoesNotExist:
         msg={"msg":"Not Found"}
         return Response(msg,status=status.HTTP_404_NOT_FOUND)
      obj.delete()
      return Response({"msg":"deleted"},status=status.HTTP_204_NO_CONTENT)
   




#Crud Opertions for for Offers
class OffersDetailes(APIView):
   #serializer_class=MedicineSerializer
   def get(self,request):
      obj=Offers.objects.all()
      serializer=OfferSerializer(obj,many=True)
      return Response(serializer.data,status=status.HTTP_200_OK)
   
   def post(self,request):
      serializer=OfferSerializer(data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data,status=status.HTTP_201_CREATED)
      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
   
   #For Get&Put&Patch&Delete On object
class OfferInfo(APIView):
    def get(self,request,id):
        try:
          obj=Offers.objects.get(id=id)
        except Offers.DoesNotExist:
          msg={"msg":"This Offer Post Not Found"} 
          return Response(msg,status=status.HTTP_404_NOT_FOUND)
        serializer =OfferSerializer(obj)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,id):
        try:
          obj=Offers.objects.get(id=id)
        except Offers.DoesNotExist:
          msg={"msg":"Not Found "}
          return Response(msg,status=status.HTTP_404_NOT_FOUND)
        serializer =OfferSerializer(obj,data=request.data)
        if serializer.is_valid():
          serializer.save()
          return Response(serializer.data,status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,id):
        try:
          obj=Offers.objects.get(id=id)
        except Offers.DoesNotExist:
          msg={"msg":"Not Found "}
          return Response(msg,status=status.HTTP_404_NOT_FOUND)
        serializer =OfferSerializer(obj,data=request.data,partial=True)
        if serializer.is_valid():
          serializer.save()
          return Response(serializer.data,status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        try:
          obj=Offers.objects.get(id=id)
        except Offers.DoesNotExist:
          msg={"msg":"Not Found"}
          return Response(msg,status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response({"msg":"deleted"},status=status.HTTP_204_NO_CONTENT)
  

   


