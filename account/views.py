from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from account.serializers import *
from django.contrib.auth import authenticate
from account.renders import UserRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
import jwt, datetime
from rest_framework.exceptions import AuthenticationFailed
from account.models import User
#from rest_framework.renderers import JSONRenderer, YAMLRenderer
# Create your views here.

def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }


def isLogin(request):
  token = request.META.get('HTTP_AUTHORIZATION')
  if not token:
    raise AuthenticationFailed({'success':False,'message':'Authentication credentials were not provided.'})
  try:
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])

  except jwt.ExpiredSignatureError:
    raise AuthenticationFailed({'success':False,'message':'Token Is Expired'})

  except jwt.exceptions.DecodeError:
    raise AuthenticationFailed({'success':False,'message':'Invalid token'})

  user = User.objects.filter(id=payload['id']).first()
  if not user:
    raise AuthenticationFailed({'success':False,'message':'User Account not found!'})

  return user




class UserRegistrationView(APIView):
  renderer_classes=[UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    if 'email' in request.data:
      ExitUser=User.objects.filter(email=request.data['email']).first()
      if ExitUser:
        return Response({"success":False,"message":"User with this email already exist"},status=status.HTTP_400_BAD_REQUEST)
    if serializer.is_valid(raise_exception=False):
        user = serializer.save()
        return Response({"success":True, 'message':'Registration Successfully'}, status=status.HTTP_201_CREATED)
    # print(serializer.errors)
    return Response({'message':serializer.errors,'success':False}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
  def post(self, request):
    serializer = UserLoginSerializer(data=request.data)

    if 'email' not in request.data and 'password' not in request.data:
      return Response({"success":False,"message": "email field and password field are required"}, status=status.HTTP_400_BAD_REQUEST)

    elif 'email' not in request.data:
      return Response({"success":False,"message": "email field is required"}, status=status.HTTP_400_BAD_REQUEST)

    elif 'password' not in request.data:
      return Response({"success":False,"message": "password field is required"}, status=status.HTTP_400_BAD_REQUEST)

    email = request.data['email']
    password = request.data['password']
    user = User.objects.filter(email=email).first()

    if user is None:
      return Response({'success':False,'message':'User Account not found!'},status=status.HTTP_401_UNAUTHORIZED)

    if not user.check_password(password):
      return Response({"success":False,"message":"Incorrect Password"}, status=status.HTTP_400_BAD_REQUEST)

    payload = {
      'id': user.id,
      'exp': datetime.datetime.utcnow() + datetime.timedelta(days=3),
      'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, 'secret', algorithm='HS256')

    response = Response()

    # response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
        'token': token,
        'success': True,
    }
    return response


class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  # permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    user=isLogin(request)
    serializer = UserProfileSerializer(user)
    return Response({'success':True,'data':serializer.data}, status=status.HTTP_200_OK)




  def put(self,request,format=None):
    user=isLogin(request)
    serializer= UserProfileSerializer(user,data=request.data)
    if serializer.is_valid(raise_exception=True):
        pharmacy = serializer.save()
        return Response({'message':'profile updated Successfully',"success":True}, status=status.HTTP_201_CREATED)
    # print(serializer.errors)
    return Response({'success':False,'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class RestPasswordView(APIView):
  renderer_classes = [UserRenderer]
  # permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    user=isLogin(request)
    # serializer = ResetPasswordSerializer(data=request.data, context={'user':request.user})
    if 'old_password' not in request.data and 'new_password' not in request.data:
      return Response({"success":False,"message": " old_password field new_password are  required"}, status=status.HTTP_400_BAD_REQUEST)

    elif 'old_password' not in request.data:
      return Response({"success":False,"message": "old_password field is required"}, status=status.HTTP_400_BAD_REQUEST)

    elif 'new_password' not in request.data:
      return Response({"success":False,"message": "new_password field is required"}, status=status.HTTP_400_BAD_REQUEST)

    old_password = request.data['old_password']
    new_password = request.data['new_password']

    flag = user.check_password(old_password)

    if not flag:
      return Response({"success":False,"message":  "old_password field is invalid"}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    return Response({"success":True, "message": "Password is Rest Successfully"}, status=status.HTTP_200_OK)

#ForgetPassword For User
class ForgetPasswordView(APIView):
  renderer_classes=[UserRenderer]
  def put(self,request,formt=None):
       if 'email' not in request.data:
        return Response({"success":False,"message": "email field is required"}, status=status.HTTP_400_BAD_REQUEST)

       elif 'new_password' not in request.data:
        return Response({"success":False,"message": "new_password field is required"}, status=status.HTTP_400_BAD_REQUEST)

       email = request.data['email']
       new_password = request.data['new_password']
       user = User.objects.filter(email=email).first()
       if not user:
        raise AuthenticationFailed({"success":False,"message":'User Account not found!'})
       user.set_password(new_password)
       user.save()
       return Response({"success":True, "message": "Password is changed Successfully"}, status=status.HTTP_200_OK)


class LogOutView(APIView):
   def post(self, request, format=None):
    user = isLogin(request)
    response_data = {"message": "LogOut Successfully !", "success":True}
    response = Response(response_data)
    response.delete_cookie('jwt')
    return response


class AdminView(generics.ListCreateAPIView):
  queryset = User.objects.all()
  serializer_class = AdminSerializer
