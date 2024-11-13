from django.shortcuts import render
import jwt
import requests
from django.http import JsonResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .decorators import jwt_required

@jwt_required
def get(request):
    return JsonResponse({"message": "Authenticated", "user_id": request.user_id})
