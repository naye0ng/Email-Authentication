import jwt
import datetime
from django.conf import settings
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def login(request) :
    if request.method == 'POST' :
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password :
            user = authenticate(request,email=email, password=password)
            if user is not None :
                access_token = create_token(email, 1)
                refresh_token = create_token(email, 24)
                content = {
                    'access_token': access_token.decode(),
                    'refresh_token': refresh_token.decode(),
                    }
                return JsonResponse(content)

    return JsonResponse({'message': '로그인에 실패했습니다.'}, status=401)

@csrf_exempt
def validate(request) :
    access_token = request.META.get('HTTP_AUTHORIZATION')
    if validate_token(access_token) :
        return JsonResponse({'message': '유효한 사용자입니다.'})
    return JsonResponse({'message': '유효하지 않은 사용자입니다.'}, status=401)

@csrf_exempt
def refresh(request) :
    refresh_token = request.META.get('HTTP_AUTHORIZATION')
    validate_user = validate_token(refresh_token)
    if validate_user :
        access_token = create_token(validate_user['email'], 1)
        return JsonResponse({'access_token': access_token.decode()})
    return JsonResponse({'message': '유효하지 않은 토큰입니다.'}, status=401)

def create_token(email, time) :
    encoded = jwt.encode(
        {'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=time), 'email': email}, 
        settings.SECRET_KEY, algorithm='HS256')
    return encoded

def validate_token(token) :
    try:
        validate_user = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    else:
        return validate_user
    