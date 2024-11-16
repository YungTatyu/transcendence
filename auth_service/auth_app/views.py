import jwt
import datetime
import json
from django.conf import settings
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

# TODO csrf_exempt
@csrf_exempt
def generate_jwt(request):

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"detail": "Invalid JSON"}, status=400)

    username = data.get('username')
    password = data.get('password')

    user = authenticate(request, username=username, password=password)
    if not user:
        return JsonResponse({"detail": "Invalid credentials"}, status=403)

    payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "iat": datetime.datetime.utcnow(),
    }

    try:
        with open(settings.JWT_PRIVATE_KEY_PATH, 'r') as f:
            private_key = f.read()

        token = jwt.encode(payload, private_key, algorithm='RS256')

        return JsonResponse({"access_token": token})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def get_public_key(request):
    try:
        with open(settings.JWT_PUBLIC_KEY_PATH, 'r') as f:
            public_key = f.read()
        return JsonResponse({"public_key": public_key})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)