from distutils import errors
from msilib.schema import Class
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account_app.serializers import UseProfileSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserRegistrationSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from account_app.renderer import UserRenderer
from rest_framework.permissions import IsAuthenticated

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
        token= get_tokens_for_user(user)
        return Response({'token':token,'msg':'Registation successful'},status=status.HTTP_201_CREATED)
    return Response({errors:serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
             token= get_tokens_for_user(user)
             return Response({'token':token,'msg':'Login successful'},status=status.HTTP_200_OK)

            else:
             return Response({'errors':{'non_field_errors':['email or password is not valid']}},status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
     renderer_classes=[UserRenderer]
     permission_classes=[IsAuthenticated]
     def get(self,request,format=None):
       serializer=UseProfileSerializer(request.user)
       return Response(serializer.data,status=status.HTTP_201_CREATED)

class UserChangePasswordView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
      serializer=UserChangePasswordSerializer(data=request.data,context={'user':request.user})
      if serializer.is_valid(raise_exception=True):
        return Response({'msg':'Password Change Successfully'},status=status.HTTP_200_OK)
      return Response({errors:serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class SendPasswordResetEmailView(APIView):
    renderer_classes=[UserRenderer]
    def post(self, request, format=None):
     serializer = SendPasswordResetEmailSerializer(data=request.data)
     if serializer.is_valid(raise_exception=True):
      return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)
     return Response({errors:serializer.errors},status=status.HTTP_400_BAD_REQUEST)
      
     

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    if serializer.is_valid(raise_exception=True):
        return Response({'msg':'Password Reset Successfully'},status=status.HTTP_200_OK)
    return Response({errors:serializer.errors},status=status.HTTP_400_BAD_REQUEST)