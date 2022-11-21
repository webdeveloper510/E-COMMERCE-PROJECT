from django.conf import settings
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives, message
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str,force_bytes, DjangoUnicodeDecodeError
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate

from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from account_app.renderer import UserRenderer
from account_app.utils import Util
from xhtml2pdf import pisa
from time import gmtime, strftime
import ast
from distutils import errors
import stripe
from base64 import b64encode
import base64
import requests
import json
from weasyprint import HTML, CSS
import weasyprint
from io import StringIO
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
