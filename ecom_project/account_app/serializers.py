from tokenize import TokenError
from account_app.utils import Util
from unittest.util import _MAX_LENGTH
from wsgiref.validate import validator
from rest_framework import serializers
from account_app.models import User
from django.utils.encoding import smart_str,force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator



class UserRegistrationSerializer(serializers.ModelSerializer):
 password2=serializers.CharField(style={'input_type':'password'},write_only=True)
 class Meta:
    model=User
<<<<<<< HEAD
    fields=['id','First_name','Last_name','address','contact_number','alternative_contact_number','email','password','password2']
=======

    fields=['id','email','is_verified','password','password2','First_name','Last_name','address','contact_number','alternative_contact_number']

>>>>>>> 4f3611108582a09a769829a9512efd2cf461b586
    extra_kwargs={
     
        'First_name': {'error_messages': {'required': "Firstname is required",'blank':'please provide a firstname'}},
        'Last_name': {'error_messages': {'required': "Lastname is required",'blank':'please provide a lastname'}},
        'address': {'error_messages': {'required': "Address is required",'blank':'please provide your complete address'}},
        'contact_number': {'error_messages': {'required': "Your contact number is required",'blank':'please provide your contact number'}},
        'email': {'error_messages': {'required': "email is required",'blank':'please provide a email'}},
        'password': {'error_messages': {'required': "password is required",'blank':'please Enter a email'}},
        'password2': {'error_messages': {'required': "confirm password is required",'blank':'Confirm password could not blank'}},
       }

    #validating password and confirm password
 def validate(self, attrs):
   password=attrs.get('password')
   password2=attrs.get('password2')
   if password!=password2:
    raise serializers.ValidationError('password and confirm password doesnot match')

   return attrs

 def create(self, validated_data):
   return User.objects.create_user(** validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=250)
    class Meta:
     model=User
     fields=['email','password']
     extra_kwargs={
        'email': {'error_messages': {'required': "email is required",'blank':'please provide a email'}},
        'password': {'error_messages': {'required': "password is required",'blank':'please Enter a email'}}
        
    }
class UseProfileSerializer(serializers.ModelSerializer):
  class Meta:
     model=User
     fields=['id','First_name','Last_name','email']

class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

#change password email 
class SendChangePasswordEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email = email)
      uid = urlsafe_base64_encode(force_bytes(user.id))#Encoding is the process of converting data into a format required for a number of information processing needs
      print('Encoded UID', uid)
      #token = PasswordResetTokenGenerator().make_token(user)
      #print('Password Reset Token', token)
      #link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token #password reset link
      #print('Password Reset Link', link)
      # Send EMail
      body = 'You recently changed the password associated with your account'
      data = {
        'subject':'Your password has been changed',
        'body':body,
        'to_email':user.email
      }
      Util.send_email(data)
      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')





<<<<<<< HEAD
=======

>>>>>>> 4f3611108582a09a769829a9512efd2cf461b586
class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email = email)
      uid = urlsafe_base64_encode(force_bytes(user.id))#Encoding is the process of converting data into a format required for a number of information processing needs
      print('Encoded UID', uid)
      token = PasswordResetTokenGenerator().make_token(user)
      print('Password Reset Token', token)
      link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token #password reset link
      print('Password Reset Link', link)
      # Send EMail
      body = 'Click Following Link to Reset Your Password '+link
      data = {
        'subject':'Reset Your Password',
        'body':body,
        'to_email':user.email
      }
      Util.send_email(data)
      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')


class UserPasswordResetSerializer(serializers.Serializer):
   password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
   password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
   class Meta:
    fields = ['password', 'password2']

   def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
         raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))#convert encoded Data into origional string
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
        PasswordResetTokenGenerator().check_token(user, token)
        raise serializers.ValidationError('Token is not Valid or Expired')

class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ('First_name', 'Last_name', 'email','address','contact_number','alternative_contact_number')
        extra_kwargs = {
            'First_name': {'required': True},
            'Last_name': {'required': True},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value
    
    def update(self, instance, validated_data):
        instance.First_name = validated_data['First_name']
        instance.Last_name = validated_data['Last_name']
        instance.email = validated_data['email']

        instance.save()

        return instance

<<<<<<< HEAD
class LogoutUserSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
      self.token = attrs['refresh']
      return attrs

    def save(self, **kwargs):
      try:
        refresh_token = (self.token).blacklist()
      except TokenError:
        self.fail('bad token')

=======


>>>>>>> 4f3611108582a09a769829a9512efd2cf461b586
