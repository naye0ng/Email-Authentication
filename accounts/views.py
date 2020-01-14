from django.shortcuts import render
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from django.http import JsonResponse

from .serializers import MessageSerializer
from .models import User

# Create your views here.
def sign_up(request) :
    # [1] POST : 회원가입
    
    pass

def email(request) :
    # [1] POST : 메일보내기
    if request.method == 'POST' :
        email = request.POST.get('email')
        # TODO : 이메일 값을 기준으로 암복호화 진행하자
        status = EmailMessage('제목', '내용', to=[email]).send()
        if status == 1 :
            return json_response('{}로 인증 코드를 발송했습니다.'.format(email))
        return json_response('잘못된 이메일입니다.')

    # [2] GET : 메일 중복확인
    email = is_email_exist(request.GET.get('email'))
    if not email :
        return json_response('사용 가능한 이메일입니다. 버튼을 눌러 이메일을 인증하세요.')
    return json_response('이미 사용중인 이메일입니다. 다른 이메일을 입력해주세요.')
    
    
# email을 보낸 인증코드가 일치한다면
def activate(request) :
    # [1] POST : 복호화하여 회원가입 폼 제공
    pass



def is_email_exist(email):
    try:
        return User.objects.get(email=email)
    except ObjectDoesNotExist:
        return ''

def json_response(message) :
    return JsonResponse({'message':message}, json_dumps_params = {'ensure_ascii': True})

# [로그인 jwt참고] https://dlwodus.tistory.com/373