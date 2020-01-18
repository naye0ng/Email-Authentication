from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode

from .tokens import account_activation_token
from .models import User

@csrf_exempt
def authentiaction(request) :
    
    # [1] POST : 로그인 요청
    if request.method == 'POST' :
        if request.POST.get('password1') and request.POST.get('password1') == request.POST.get('password2') :
            email = request.POST.get('email')
            if is_email_exist(email) :
                # 기존에 등록된 이메일이 존재한다면, 활성화를 체크하여 중복 이메일 판단
                if User.objects.get(email=email).is_active :
                    return json_response('이미 사용중인 이메일입니다. 다른 이메일을 입력해주세요.')
            else :
                # 유저를 DB에 저장하기
                user = User.objects.create_user(
                    email=email,
                    password=request.POST.get('password1')
                )
                user.save()
    
            # token 생성하고 메일 보내기
            user = User.objects.get(email=email)
            uid64 = urlsafe_base64_encode(force_bytes(user.pk)).encode().decode()
            token = account_activation_token.make_token(user)
            url = request.build_absolute_uri()

            # 1분동안 redis에 uid와 token 저장하기
            cache.set(uid64, token, timeout=60) 
            
            email_title = '회원가입 인증 메일입니다.'
            email_msg = url+'?token='+token+'&uid64='+uid64
            return send_email(email, email_title, email_msg)
        return json_response('회원가입에 실패했습니다.')

    # [2] GET : 이메일 인증 및 계정 활성화
    uid64 = request.GET.get('uid64')
    uid = force_text(urlsafe_base64_decode(uid64))
    token = request.GET.get('token')
    user = User.objects.get(pk=uid)
    if user and account_activation_token.check_token(user,token) and cache.get(uid64) :
        user.is_active = True
        user.save()

        # 인증 완료 front 페이지로 리다이렉트
        return redirect(to='http://www.naver.com')
    # 인증 실패 front 페이지로 리다이렉트
    return json_response('유효하지 않은 인증입니다. 다시 진행하세요')

def is_email_exist(email):
    try:
        return User.objects.get(email=email)
    except ObjectDoesNotExist:
        return False

def send_email(email, title, content) :
    status = EmailMessage(title, content, to=[email]).send()
    if status == 1 :
        return json_response('{}로 인증 코드를 발송했습니다.'.format(email))
    return json_response('이메일 발송에 실패했습니다.')


def json_response(message) :
    return JsonResponse({'message':message}, json_dumps_params = {'ensure_ascii': True})
