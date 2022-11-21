from ecom_project.library import *
from .models import *
from .serializers import *

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
       serializer=UserProfileSerializer(request.user)
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


from django.shortcuts import render

class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format=None):
     if request.method == "POST":
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset Successfully'},status=status.HTTP_200_OK)
        return Response({errors:serializer.errors},status=status.HTTP_400_BAD_REQUEST)
     return render(request,'resetpassword.html',{'msg':123})


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

from django.shortcuts import render

# Create your views here.
# def home(request):
# 	context ={}
# 	context['form']= ResetPasswordForm()
# 	return render(request, "resetpassword.html", context)

from django.views.decorators.csrf import csrf_exempt
import requests
import json
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import viewsets

class SendPasswordResetEmailViewSet(viewsets.ViewSet):
    renderer_classes=[UserRenderer]
    def test(self, request, format=None):
      global tokens
      if request.method == "POST":
        email = request.data.get('email')
        print("email is", email)
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email = email)
            uid = urlsafe_base64_encode(force_bytes(user.id))#Encoding is the process of converting data into a format required for a number of information processing needs
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = BASE_URL+'/reset-password/'+uid+'/'+token+'/' #password reset link
            tokens = uid, token
            print('Password Reset Link', link)
            body = 'Click Following Link to Reset Your Password '+link
            data = {
                'subject':'Reset Your Password',
                'body':body,
                'to_email':user.email 
            }
            Util.send_email(data)
            return Response("link sent")
        # else:
        #     raise serializers.ValidationError('You are not a Registered User')
      return tokens

from rest_framework import viewsets

class FormView(APIView):
 def testform(self, request, format=None):
    template_name = 'resetpassword.html'
    fn=request.POST.get('pwd')
    ln=request.POST.get('pwd2')
    return render(request, 'resetpassword.html', {'data':"hii"})

    
