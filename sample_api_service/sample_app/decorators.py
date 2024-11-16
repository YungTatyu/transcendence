from functools import wraps
import jwt
import requests
from django.http import JsonResponse
from django.conf import settings

AUTH_SERVER_PUBLIC_KEY_URL = "http://auth:8000/api/public-key/"

def jwt_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JsonResponse({"error": "Authorization header missing"}, status=401)
        
        parts = auth_header.split(" ")
        if len(parts) != 2 or parts[0] != "Bearer":
            return JsonResponse({"error": "Invalid Authorization header format"}, status=401)
        
        token = parts[1]

        try:
            response = requests.get(AUTH_SERVER_PUBLIC_KEY_URL)
            PUBLIC_KEY = response.json().get("public_key")
            decoded_token = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
            request.user_id = decoded_token["user_id"]
            return func(request, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)
    
    return wrapper