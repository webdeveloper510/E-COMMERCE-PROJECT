from distutils import errors
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from account_app.renderer import UserRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.core.mail import send_mail
from .models import *
from .serializers import *

from django.utils.encoding import smart_str,force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

#Creating tokens manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
 renderer_classes=[UserRenderer]
 def post(self,request,format=None):
    serializer=UserRegistrationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user=serializer.save()
        user_id = serializer.data['id']
        return Response({'msg':'Registation successful', "user_id": user_id},status=status.HTTP_201_CREATED)
    return Response({errors:serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            print(user)
            if user is not None:
             token= get_tokens_for_user(user)
             return Response({'token':token,'msg':'Login successful','status':'status.HTTP_200_OK'})

            else:
             return Response({'errors':{'non_field_errors':['email or password is not valid']},'status':'status.HTTP_404_NOT_FOUND'})

class UserProfileView(APIView):
     renderer_classes=[UserRenderer]
     permission_classes=[IsAuthenticated]
     def post(self,request,format=None):
       print(request.headers)
       serializer=UseProfileSerializer(request.user)
       print(request.user)
       return Response(serializer.data,status=status.HTTP_201_CREATED)

class UserChangePasswordView(generics.UpdateAPIView):
    
    serializer_class = UserChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."], "status":"status.HTTP_400_BAD_REQUEST"})
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# changed password email view      
class SendChangePasswordEmailView(APIView):
    renderer_classes=[UserRenderer]
    def post(self, request, format=None):
     serializer = SendChangePasswordEmailSerializer(data=request.data)
     if serializer.is_valid(raise_exception=True):
      return Response({'msg':'You have changed your password','status':'status.HTTP_200_OK'})
     return Response({errors:serializer.errors},status=status.HTTP_400_BAD_REQUEST)
           

class SendPasswordResetEmailView(APIView):
    renderer_classes=[UserRenderer]
    def post(self, request, format=None):
     serializer = SendPasswordResetEmailSerializer(data=request.data)
     if serializer.is_valid(raise_exception=True):
       return Response({'msg':'Password Reset link send. Please check your Email','status':'status.HTTP_200_OK'})
     return Response({errors:serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    if serializer.is_valid(raise_exception=True):
        return Response({'msg':'Password Reset Successfully'},status=status.HTTP_200_OK)
    return Response({errors:serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class UpdateProfileView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = "pk"
    serializer_class = UpdateUserSerializer

    def get_queryset(self):
       data = User.objects.all()
       return data

    def update(self, request, *args, **kwargs):
       partial = kwargs.pop('partial', False)
       instance = self.get_object()
       serializer = self.get_serializer(instance, data=request.data, partial=partial)
       serializer.is_valid(raise_exception=True)
       self.perform_update(serializer)
       result = {
        "message": "Your Profile is successfully Updated",
        "details": serializer.data,
        "status": status.HTTP_200_OK,
       }
       return Response(result)

class LogoutUser(APIView):
  renderer_classes = [UserRenderer]
  permission_classes=[IsAuthenticated]
  def post(self, request, format=None):
    #serializer = LogoutUserSerializer(data=request.data)
    #serializer.is_valid(raise_exception=True)
    return Response({'msg':'Logout Successfully'},status=status.HTTP_200_OK)