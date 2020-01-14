from django.shortcuts import render,redirect,HttpResponse
from rest_framework.decorators import api_view
from django.contrib.auth.models import User



from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.contrib import auth
from .models import User

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text



def sign_up(request) :
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            pass

# Create your views here.
def users(request) :
    # 회원가입
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:



            user = User.objects.create_user(
                email=request.POST["email"],
                username=request.POST["username"],
                password=request.POST["password1"])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('account/user_activate_email.html',                         {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                'token': account_activation_token.make_token(user),
            }) 
            mail_subject = "[SOT] 회원가입 인증 메일입니다."
            user_email = user.username
            email = EmailMessage(mail_subject, message, to=[user_email])
            email.send()
            return HttpResponse(
                '<div style="font-size: 40px; width: 100%; height:100%; display:flex; text-align:center; '
                'justify-content: center; align-items: center;">'
                '입력하신 이메일<span>로 인증 링크가 전송되었습니다.</span>'
                '</div>'
            )
            return redirect('account:home')
    return render(request, 'account/signup.html')

def activate(request, uid64, token):

    uid = force_text(urlsafe_base64_decode(uid64))
    user = User.objects.get(pk=uid)

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return True
        # return redirect('user:home')
    else:
        return HttpResponse('비정상적인 접근입니다.')


def user(request, user_id) :
    pass

# [이메일 인증] 
# https://swarf00.github.io/2018/12/14/logout.html
# https://naye0ng-url-shortener.herokuapp.com/e
